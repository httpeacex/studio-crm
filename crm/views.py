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
    return render(request, 'crm/clients.html', {
        'page': Paginator(queryset, 12).get_page(request.GET.get('page')),
        'query': query, 'archived': archived,
        'active_count': base.filter(archived=False).count(),
        'archive_count': base.filter(archived=True).count(),
    })


@login_required
def client_detail(request, pk):
    return render(request, 'crm/detail.html', {'customer': get_object_or_404(visible_clients(request.user), pk=pk)})


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
    return render(request, 'crm/form.html', {'form': form, 'customer': customer})


@login_required
@require_POST
def client_archive(request, pk):
    customer = get_object_or_404(visible_clients(request.user), pk=pk)
    customer.archived = True
    customer.save(update_fields=['archived', 'updated_at'])
    messages.success(request, 'Клиент перенесён в архив.')
    return redirect('clients')
