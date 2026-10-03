from django.db import models
from EntreprisesApp.models import Entreprise
# Create your models here.
class Expedition(models.Model):
    reference=models.CharField(max_length=20,unique=True,)
    ville_depart=models.CharField(max_length=20)
    ville_arrivee=models.CharField(max_length=20)
    poids_kg=models.DecimalField(max_digits=6, decimal_places=3)
    date_souhaitee=models.DateField()
    description=models.TextField()
    STATUT_CHOICES=[('publiee',"Publiee"),
                                     ('attribuee','Attribuee'),('en_cours','En_cours'),
                                     ('livree','Livree'),('annulee','Anunulee')
    ]
    statut=models.CharField(max_length=10,default='publiee',choices=STATUT_CHOICES)
    entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='expidations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
