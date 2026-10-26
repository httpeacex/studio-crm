from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import ClientForm
from .models import Client


def visible_clients(user):
    queryset = Client.objects.select_related('owner')
    return queryset if user.is_staff else queryset.filter(owner=user)


@login_required
def clients(request):
    base = visible_clients(request.user)
    archived = request.GET.get('archived') == '1'
    queryset = base.filter(archived=archived)
    query = request.GET.get('q', '').strip()[:200]
    if query:
        queryset = queryset.filter(Q(name__icontains=query) | Q(company__icontains=query) | Q(email__icontains=query))
    contact = request.GET.get('contact', '')
    if contact == 'missing':
        queryset = queryset.filter(email='')
    else:
        contact = ''
    orderings = {'updated': ('-updated_at', '-pk'), 'name': ('name', 'pk'), 'created': ('-created_at', '-pk')}
    sort = request.GET.get('sort', 'updated')
    if sort not in orderings:
        sort = 'updated'
    queryset = queryset.order_by(*orderings[sort])
    return render(request, 'crm/clients.html', {
        'page': Paginator(queryset, 12).get_page(request.GET.get('page')),
        'query': query, 'archived': archived,
        'active_count': base.filter(archived=False).count(),
        'archive_count': base.filter(archived=True).count(),
        'missing_count': base.filter(archived=False, email='').count(),
        'sort': sort, 'contact': contact,
    })


@login_required
def client_detail(request, pk):
    customer = get_object_or_404(visible_clients(request.user), pk=pk)
    return render(request, 'crm/detail.html', {'customer': customer, 'archived': customer.archived})


@login_required
def client_form(request, pk=None):
    customer = get_object_or_404(visible_clients(request.user), pk=pk) if pk else None
    form = ClientForm(request.POST if request.method == 'POST' else None, instance=customer)
    if request.method == 'POST' and form.is_valid():
        customer = form.save(commit=False)
        if not customer.pk:
            customer.owner = request.user
        customer.save()
        messages.success(request, 'Клиент сохранён.')
        return redirect('client-detail', pk=customer.pk)
    return render(request, 'crm/form.html', {'form': form, 'customer': customer, 'archived': bool(customer and customer.archived)})


@login_required
@require_POST
def client_archive(request, pk):
    customer = get_object_or_404(visible_clients(request.user), pk=pk)
    customer.archived = True
    customer.save(update_fields=['archived', 'updated_at'])
    messages.success(request, 'Клиент перенесён в архив.')
    return redirect('clients')


@login_required
@require_POST
def client_restore(request, pk):
    customer = get_object_or_404(visible_clients(request.user), pk=pk)
    customer.archived = False
    customer.save(update_fields=['archived', 'updated_at'])
    messages.success(request, 'Клиент возвращён в активные.')
    return redirect('client-detail', pk=pk)
