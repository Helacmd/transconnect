from django.db import models
from EntreprisesApp.models import Entreprise
# Create your models here.
class Vehicule(models.Model):
    immatriculation=models.CharField(max_length=30,unique=True)
    type_vehicule=models.CharField(max_length=100,choices=[
        ('camionette', 'Camionette'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur','Camion_porteur'),
        ('semi_remorque','Semi_remorque')
        ])
    capacite_kg=models.PositiveIntegerField()
    disponibilite=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name="vehicules")