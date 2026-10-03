from django.db import models
from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import Expedition
from VehiculesApp.models import Vehicule

# Create your models here.
class Offre(models.Model):
    prix=models.DecimalField(max_digits=10, decimal_places=2)
    delai_jours=models.PositiveIntegerField()
    STATUT_CHOICES=[
        ('proposee', 'Proposee'),
        ('acceptee', 'Acceptee'),
        ('refusee', 'Refusee'),
        ('retiree', 'Retiree'),
    ]
    statut=models.CharField(max_length=15, choices=STATUT_CHOICES, default='proposee')
    date_proposition=models.DateField(auto_now_add=True)
    expedition=models.ForeignKey(Expedition,on_delete=models.CASCADE, related_name='offres')
    transporteur=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='offres_proposees')
    vehicule=models.ForeignKey(Vehicule,on_delete=models.CASCADE,related_name='offres')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)