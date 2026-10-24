from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
# Create your models here.
class Vehicule(models.Model):
    immatriculation=models.CharField(max_length=10,unique=True)
    type_vehicule=models.CharField(max_length=50,choices=[
        ('camionnette', 'Camionnette'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur','Camion_porteur'),
        ('semi_remorque','Semi_remorque')
        ])
    capacite_kg=models.PositiveIntegerField(validators=[MinValueValidator(1,"La capacité doit etre sup à 0 kg")])
    disponible=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name="vehicules")
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({'entreprise': "Un véhicule doit appartenir à une entreprise de type transporteur"})
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.immatriculation