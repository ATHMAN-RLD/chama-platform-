from django.shortcuts import render

# Create your views here.
from .models import Chama

def chama_list(request):
    chamas = Chama.objects.all()
    return render(request, 'groups/chama_list.html', {'chamas': chamas})  
