from django.db import models
from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import Expedition
from VehiculesApp.models import Vehicule
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.
class Offre(models.Model):
    prix=models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01,"Le prix doit etre strictement superieur a 0")])
    delai_jours=models.PositiveIntegerField(validators=[MinValueValidator(1,"Le delai doit etre >=1 jour")])
    STATUT_CHOICES=[
        ('proposee','Proposee'),
        ('acceptee','Acceptee'),
        ('refusee','Refusee'),
    ]
    statut=models.CharField(max_length=15, choices=STATUT_CHOICES, default='proposee')
    date_proposition=models.DateField(auto_now_add=True)
    expedition=models.ForeignKey(Expedition,on_delete=models.CASCADE, related_name='offres')
    transporteur=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='offres_proposees')
    vehicule=models.ForeignKey(Vehicule,on_delete=models.CASCADE,related_name='offres')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def clean(self):
        super().clean()
        if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError({'transporteur': "Une offre ne peut être créée que par une entreprise de type transporteur"})
        if self.vehicule_id and self.transporteur_id and self.vehicule.entreprise_id != self.transporteur_id:
            raise ValidationError({'vehicule': "Le véhicule doit appartenir à l'entreprise qui fait l'offre"})
        if not self.pk and self.expedition_id and self.expedition.statut != 'publiee':
            raise ValidationError({'expedition': "L'expédition n'est plus au statut publiée"})
        if self.statut == 'proposee' and self.expedition_id and self.transporteur_id:
            offres_doublons = Offre.objects.filter(expedition_id=self.expedition_id, transporteur_id=self.transporteur_id, statut='proposee')
            if self.pk:
                offres_doublons = offres_doublons.exclude(pk=self.pk)
            if offres_doublons.exists():
                raise ValidationError("Votre entreprise a déjà une offre proposée sur cette expédition")
        if not self.pk and self.vehicule_id and not self.vehicule.disponible:
            raise ValidationError({'vehicule': "Le véhicule sélectionné n'est pas disponible"})
        if self.vehicule_id and self.expedition_id:
            poids =float(self.expedition.poids_kg)
            v_type =self.vehicule.type_vehicule
            if v_type =='camionnette' and poids > 1500:
                raise ValidationError({'vehicule': "Le poids dépasse la capacité d'une camionnette"})
            elif v_type=='fourgon' and poids > 3500:
                raise ValidationError({'vehicule': "Le poids dépasse la capacité d'un fourgon"})
            elif v_type =='camion_porteur' and (poids < 3500 or poids > 19000):
                raise ValidationError({'vehicule': "Le poids ne correspond pas à la tranche d'un camion porteur"})
            elif v_type=='semi_remorque' and (poids < 19000 or poids > 26000):
                raise ValidationError({'vehicule': "Le poids ne correspond pas à la tranche d'un semi-remorque"})

    def save(self,*args,**kwargs):
        self.full_clean()
        devient_acceptee = False
        if self.statut == 'acceptee':
            if self.pk:
                ancienne_offre = Offre.objects.get(pk=self.pk)
                devient_acceptee = ancienne_offre.statut != 'acceptee'
            else:
                devient_acceptee = True
        super().save(*args, **kwargs)
        if devient_acceptee:
            self.expedition.statut = 'attribuee'
            self.expedition.save()
            Offre.objects.filter(expedition=self.expedition, statut='proposee').exclude(pk=self.pk).update(statut='refusee')