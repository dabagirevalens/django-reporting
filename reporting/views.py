from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, Sum

from .models import Business, Job, LineItem, Invoice, Payment

# Create your views here.


def index(request):
    return HttpResponse("Hello, world.")


# return all customers or companies in the database
def businesses(request):
    min = ''
    max = ''

    if request.GET.get('min'):
        min = request.GET.get('min')
    if request.GET.get('max'):
        max = request.GET.get('max')

    businesses = Business.objects.all()

    # get all business's jobs and invoices and payments
    for business in businesses:
        business.jobs = Job.objects.filter(business=business)
        business.invoices = Invoice.objects.filter(business_id=business.id)

        business.payments = Payment.objects.filter(Q(payee=business) | Q(payer=business)).values(
            'payment_type', 'reference').annotate(Sum('amount'))

    # get all line items for each job in each business
    for business in businesses:

        amount = 0
        unpaid_amount = 0
        invoice_amount = 0

        for job in business.jobs:
            job.line_items = LineItem.objects.filter(job=job)

        for invoice in business.invoices:
            invoice.line_items = LineItem.objects.filter(invoice=invoice)

        #  total job line item amount and remaining to be invoiced
        for job in business.jobs:

            for line_item in job.line_items:
                amount += line_item.amount

                if (business.invoices.count() > 0):
                    for invoice in business.invoices:
                        if line_item.invoice_id == invoice.id & invoice.status == 'unpaid':
                            unpaid_amount += line_item.amount

        business.total_job_line_item_amount = amount
        business.total_job_line_item_upaid_invoice_amount = unpaid_amount

        # total invoice line item amount
        for invoice in business.invoices:

            if invoice.line_items.count() > 0:
                for line_item in invoice.line_items:
                    invoice_amount += line_item.amount

        business.total_invoice_line_item_amount = invoice_amount

    # filter businesses by total job line item amount remaining to be invoiced
    filtered_businesses = []
    if min != '' and max != '':
        for b in businesses:
            if b.total_job_line_item_amount >= float(min) and b.total_job_line_item_amount <= float(max):
                filtered_businesses.append(b)
    if min and max:
        businesses = filtered_businesses

    # sort all businesses by total job line item amount remaining to be invoiced in descending order
    businesses = sorted(
        businesses, key=lambda business: business.total_job_line_item_upaid_invoice_amount, reverse=True)

    return render(request, 'dashboard.html', {'businesses': businesses})
