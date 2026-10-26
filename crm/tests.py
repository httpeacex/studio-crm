from django.contrib.auth import get_user_model
from django.test import TestCase, Client as Browser


class ClientWorkflowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user('owner', password='test-password-123')
        self.other = get_user_model().objects.create_user('other', password='test-password-123')
        self.client.force_login(self.owner)

    def create_client(self, name='North Studio'):
        response = self.client.post('/clients/new/', {'name': name, 'email': 'hello@example.com', 'company': 'North', 'notes': 'First meeting'})
        self.assertEqual(response.status_code, 302)
        return response.url

    def test_guest_redirected_to_login(self):
        self.client.logout()
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_create_search_edit_archive(self):
        url = self.create_client()
        self.assertContains(self.client.get(url), 'North Studio')
        self.assertContains(self.client.get('/?q=North'), 'North Studio')
        self.assertNotContains(self.client.get('/?q=Absent'), 'North Studio')
        self.assertEqual(self.client.post(url + 'edit/', {'name': 'Updated Studio', 'email': 'new@example.com', 'company': '', 'notes': ''}).status_code, 302)
        self.assertContains(self.client.get(url), 'Updated Studio')
        self.assertEqual(self.client.post(url + 'archive/').status_code, 302)
        self.assertNotContains(self.client.get('/'), 'Updated Studio')
        self.assertContains(self.client.get('/?archived=1'), 'Updated Studio')

    def test_other_manager_cannot_read_edit_or_archive(self):
        url = self.create_client()
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get('/'), 'North Studio')
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(url + 'edit/', {'name': 'Stolen'}).status_code, 404)
        self.assertEqual(self.client.post(url + 'archive/').status_code, 404)

    def test_supervisor_can_read_team_clients(self):
        url = self.create_client()
        supervisor = get_user_model().objects.create_user('lead', is_staff=True)
        self.client.force_login(supervisor)
        self.assertContains(self.client.get(url), 'North Studio')

    def test_invalid_input_does_not_create_client(self):
        response = self.client.post('/clients/new/', {'name': ' ', 'email': 'bad-address'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_archive_requires_post(self):
        url = self.create_client()
        self.assertEqual(self.client.get(url + 'archive/').status_code, 405)

    def test_csrf_blocks_forged_create(self):
        browser = Browser(enforce_csrf_checks=True)
        browser.force_login(self.owner)
        self.assertEqual(browser.post('/clients/new/', {'name': 'Forged'}).status_code, 403)

    def test_notes_are_escaped(self):
        response = self.client.post('/clients/new/', {'name': '<script>alert(1)</script>', 'email': '', 'company': '', 'notes': ''})
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get(response.url), '&lt;script&gt;alert(1)&lt;/script&gt;')

    def test_sort_name_and_filter_missing_email(self):
        self.create_client('Alpha')
        self.create_client('Zeta')
        response = self.client.get('/?sort=name')
        self.assertEqual([item.name for item in response.context['page']], ['Alpha', 'Zeta'])
        self.client.post('/clients/new/', {'name': 'No email', 'email': ''})
        response = self.client.get('/?contact=missing')
        self.assertEqual([item.name for item in response.context['page']], ['No email'])

    def test_restore_archive_is_scoped_and_post_only(self):
        url = self.create_client()
        self.client.post(url + 'archive/')
        self.assertEqual(self.client.get(url + 'restore/').status_code, 405)
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(url + 'restore/').status_code, 404)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(url + 'restore/').status_code, 302)
        self.assertContains(self.client.get('/'), 'North Studio')

    def test_invalid_sort_falls_back_and_counts_are_scoped(self):
        self.create_client()
        self.client.force_login(self.other)
        response = self.client.get('/?sort=owner__password&contact=invalid')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sort'], 'updated')
        self.assertEqual(response.context['missing_count'], 0)
