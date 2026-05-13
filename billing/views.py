from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Invoice
from django.db.models import Sum

def invoices(request):

    if request.method == 'POST':
        action = request.POST.get('action')
        invoice_id = request.POST.get('invoice_id')

        if action == 'mark_paid' and invoice_id:
            invoice = get_object_or_404(Invoice, id=invoice_id)
            invoice.mark_paid()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})

    invoices = Invoice.objects.all()

    pending_total = invoices.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'invoices': invoices,
        'total_invoices': invoices.count(),
        'pending_amount': f"{pending_total:.0f}",
        'pending_count': invoices.filter(status='pending').count(),
        'paid_count': invoices.filter(status='paid').count(),
    }

    return render(request, 'billing/invoice.html', context)