from django.urls import path
from .views import home,afficher,listExpeditions,detail
from .models import Expedition
app_name='expedition'
urlpatterns =[
    path('',home,name='home'),
    #path('home/',home,name='home'),
    path('afficher/<str:name>',afficher,name='afficher'),
    path('list/',listExpeditions,name='list_expeditions')
    path('detail/<int:expedition_id>/',detail,nme='detail')
]