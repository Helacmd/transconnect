from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,RegexValidator
from django.core.exceptions import ValidationError
def validate_email(value):
    if not value:
        raise ValidationError("l'adress email est obligatoire")#you can replace this with blank=False below
    if not value.endswith('@gmail.com'):
         raise ValidationError("Domaine invalid")
# Create your models here.
#notre propre classe utilisateur 121relation
class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, editable=False)
    email = models.EmailField(validators=[],unique = True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[
       ('chargeur', 'Chargeur'),
       ('transporteur', 'Transporteur'),
       ('administrateur', 'Administrateur')
       ],default="transporteur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#classe entreprise
class Entreprise(models.Model):
    raison_social = models.CharField(max_length=200,null=False,blank=False)
    matricule_fiscale_validator=RegexValidator(regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]\d{3}$',
                                               message="Format non conforme")
    matricule_fiscal = models.CharField(max_length=17,blank=False,unique=True,validators=[matricule_fiscale_validator])
    adress = models.TextField(validators=[MinLengthValidator(20,"l'adress doit contenir au min 2 caracteres")])
    type_entreprise = models.CharField(max_length=100,choices=[
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
        ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #les relations sont bidirectionnelles on peut acceder a les deux tabs selon 
    #limited-choice='chargeur' de preference dans les formulaires
    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')