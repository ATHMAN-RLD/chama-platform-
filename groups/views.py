from django.shortcuts import render, redirect
from .models import Chama, Member, Contribution, Loan
from .forms import ChamaForm

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