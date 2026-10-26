from django.http import HttpResponse
from django.shortcuts import render
from .models import Expedition
#dima objet request fi kol fonctionview(cest quoi le demande de user et cest quoi
#achaque fois on declare reponse

# Create your views here.
#chaque click aal lien is a request automatiquement
def home(request):
    return HttpResponse("welcome to the Expedition App!")
def afficher(request,name):
    #return HttpResponse(f"hello ,{name}!")
    return render (request,'expedition/afficher.html',{'name':name})
def listExpeditions(request):
    expeditions= Expedition.objects.all()
    return render(request,'expedition/list.html')
def detail(request,expedition_id):
    expedition= expedition.objects.get(id=expedition_id)
    return render(request,'expedition/detail.html',{'expedition':expedition})
