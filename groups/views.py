from django.shortcuts import render
from .models import Chama, Member

def chama_list(request):
    chamas = Chama.objects.all()
    return render(request, 'groups/chama_list.html', {'chamas': chamas})

def member_list(request):
    members = Member.objects.all()
    return render(request, 'groups/member_list.html', {'members': members})   