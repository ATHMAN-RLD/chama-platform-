from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Chama, Member, Membership, Contribution, Loan
from .forms import ChamaForm, RepaymentForm
from . import mpesa
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@login_required
def chama_list(request):
    chama = Chama.objects.first()

    member_count = 0
    total_contributions = 0
    active_loans_count = 0

    if chama:
        member_count = chama.memberships.count()
        total_contributions = Contribution.objects.filter(
            membership__chama=chama, status='confirmed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        active_loans_count = Loan.objects.filter(
            membership__chama=chama, status='active'
        ).count()

    context = {
        'chama': chama,
        'member_count': member_count,
        'total_contributions': total_contributions,
        'active_loans_count': active_loans_count,
    }
    return render(request, 'groups/chama_list.html', context)


@login_required
def member_list(request):
    members = Member.objects.all()
    return render(request, 'groups/member_list.html', {'members': members})


@login_required
def contribution_list(request):
    contributions = Contribution.objects.all()
    return render(request, 'groups/contribution_list.html', {'contributions': contributions})


@login_required
def loan_list(request):
    loans = Loan.objects.all()
    loan_data = []
    for loan in loans:
        total_repaid = loan.repayments.aggregate(Sum('amount'))['amount__sum'] or 0
        remaining = loan.amount - total_repaid
        loan_data.append({
            'loan': loan,
            'total_repaid': total_repaid,
            'remaining': remaining,
        })
    return render(request, 'groups/loan_list.html', {'loan_data': loan_data})


@login_required
def add_chama(request):
    if request.method == 'POST':
        form = ChamaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chama_list')
    else:
        form = ChamaForm()
    return render(request, 'groups/add_chama.html', {'form': form})


@login_required
def pay_contribution(request, membership_id):
    membership = Membership.objects.get(id=membership_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        contribution = Contribution.objects.create(
            membership=membership,
            amount=amount,
            payment_method='mpesa',
            status='pending'
        )
        response = mpesa.initiate_stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=f"Chama{membership.chama.id}",
            transaction_desc="Chama contribution"
        )
        if 'CheckoutRequestID' in response:
            contribution.checkout_request_id = response['CheckoutRequestID']
            contribution.save()
        return render(request, 'groups/payment_result.html', {'response': response, 'contribution': contribution})
    return render(request, 'groups/pay_contribution.html', {'membership': membership})


@login_required
def add_repayment(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    if request.method == 'POST':
        form = RepaymentForm(request.POST)
        if form.is_valid():
            repayment = form.save(commit=False)
            repayment.loan = loan
            repayment.save()
            return redirect('loan_list')
    else:
        form = RepaymentForm()
    return render(request, 'groups/add_repayment.html', {'form': form, 'loan': loan})


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    callback_data = data['Body']['stkCallback']
    checkout_request_id = callback_data['CheckoutRequestID']
    result_code = callback_data['ResultCode']

    try:
        contribution = Contribution.objects.get(checkout_request_id=checkout_request_id)
    except Contribution.DoesNotExist:
        contribution = None

    if contribution:
        if result_code == 0:
            items = callback_data['CallbackMetadata']['Item']
            receipt_number = None
            for item in items:
                if item['Name'] == 'MpesaReceiptNumber':
                    receipt_number = item['Value']
            contribution.status = 'confirmed'
            contribution.transaction_reference = receipt_number
            contribution.save()
        else:
            contribution.status = 'failed'
            contribution.save()

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'}) 