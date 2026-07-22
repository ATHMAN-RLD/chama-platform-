from django.shortcuts import render, redirect
from .models import Chama, Member, Membership, Contribution, Loan
from .forms import ChamaForm
from . import mpesa

def chama_list(request):
    chamas = Chama.objects.all()
    return render(request, 'groups/chama_list.html', {'chamas': chamas})

def member_list(request):
    members = Member.objects.all()
    return render(request, 'groups/member_list.html', {'members': members})

def contribution_list(request):
    contributions = Contribution.objects.all()
    return render(request, 'groups/contribution_list.html', {'contributions': contributions})

def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'groups/loan_list.html', {'loans': loans})
def add_chama(request):
    if request.method == 'POST':
        form = ChamaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chama_list')
    else:
        form = ChamaForm()
    return render(request, 'groups/add_chama.html', {'form': form})  
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

        return render(request, 'groups/payment_result.html', {'response': response, 'contribution': contribution})

    return render(request, 'groups/pay_contribution.html', {'membership': membership})     