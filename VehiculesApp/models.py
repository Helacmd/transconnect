from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.validators import MinValueValidator
# Create your models here.
class Vehicule(models.Model):
    immatriculation=models.CharField(max_length=10,unique=True)
    type_vehicule=models.CharField(max_length=50,choices=[
        ('camionette', 'Camionette'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur','Camion_porteur'),
        ('semi_remorque','Semi_remorque')
        ])
    capacite_kg=models.PositiveIntegerField(validators=[MinValueValidator(1,"La capacité doit etre sup à 0 kg")])
    disponibilite=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name="vehicules")