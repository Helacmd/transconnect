from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from EntreprisesApp.models import Entreprise


class Expedition(models.Model):
    # auto-généré, format EXP_AA_NNNNN (la pk reste l'id)
    reference = models.CharField(max_length=20, unique=True, editable=False)
    ville_depart = models.CharField(max_length=20)
    ville_arrivee = models.CharField(max_length=20)
    poids_kg = models.DecimalField(max_digits=8, decimal_places=3)
    date_souhaitee = models.DateField()
    description = models.TextField()
    STATUT_CHOICES = [
        ('publiee', 'Publiee'),
        ('attribuee', 'Attribuee'),
        ('en_cours', 'En_cours'),
        ('livree', 'Livree'),
        ('annulee', 'Annulee'),
    ]
    statut = models.CharField(max_length=10, default='publiee', choices=STATUT_CHOICES)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='expidations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({'entreprise': "Une expedition ne peut etre faite que par une entreprise de type chargeur"})

    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime('%y')
        dernier = cls.objects.filter(reference__startswith=f"EXP_{annee}_").order_by('-reference').first()
        compteur = int(dernier.reference[-5:]) + 1 if dernier else 1
        if compteur > 99999:
            raise ValidationError("limite exceeded")
        return f"EXP_{annee}_{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference}"