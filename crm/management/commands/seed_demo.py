import secrets
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from crm.models import Client


class Command(BaseCommand):
    help = 'Create fictional local demo data. Existing accounts are left unchanged.'

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Demo seeding is available only with DJANGO_DEBUG=1.')
        for username, lead in [('manager', False), ('director', True)]:
            user, created = get_user_model().objects.get_or_create(username=username, defaults={'is_staff': lead})
            if created:
                password = secrets.token_urlsafe(16)
                user.set_password(password)
                user.save()
                self.stdout.write(f'{username}: {password}')
            else:
                self.stdout.write(f'{username}: existing account, password unchanged')
        manager = get_user_model().objects.get(username='manager')
        samples = [('Анна Миронова', 'Forma Studio'), ('Марк Волков', 'North Coffee'), ('Алина Орлова', 'Botanica'), ('Денис Белов', 'Mono Architecture'), ('Ева Соколова', 'Linen & Light'), ('Артём Морозов', 'Point Digital')]
        for index, (name, company) in enumerate(samples):
            Client.objects.get_or_create(owner=manager, email=f'contact{index}@example.com', defaults={'name': name, 'company': company, 'notes': 'Вымышленный контакт для демонстрации. Обсудить задачи и сроки проекта.'})
        self.stdout.write(self.style.SUCCESS('Demo data ready. Store generated passwords locally.'))
