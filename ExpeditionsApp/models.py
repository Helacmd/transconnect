from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.exceptions import ValidationError
from django.utils  import timezone
# Create your models here.
class Expedition(models.Model):
    #auto genere lid mais nous voulons cette forma EX_AA_NNNNN
    reference=models.CharField(max_length=20,unique=True,editable=False)
    
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
    def clean(self):
        #clean taamel controle ou tvalidi el validators gbal ma el user imess el data base
        super().clean()
        #recuperer lidentifiant de lentrprise
        #key en miniscule lhne chargeur hiya el key
        if self.entreprise_id and self.entrprise.type_entreprise != 'chargeur':
            #type dictionnaire bech neeref el erreur mnin jet
            raise ValidationError({'entrprise':'une expedition ne peut etre que par une entreprise de type chargeur'})

    entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='expidations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#_ indication que cest une fonction propre dans la classse
    @classmethod #decorateur tab3a el classe ou te5ou en parametre un objet methdoe fi west el class sinon je suis oblijet bech naadi self
    #instance bch nrecupere la requette sql mais self description lele classe kamla mayhemnich fel valeur aakess
    #self 
    #ki nheb nehki maa el base lazemni instance /creation d'un objet
    def _generate_reference(cls):
        #il existe +eurs methode d'extraction d'annee
        annee=timezone.now.strftime('%y')
        #dernier=cls.objects select sur .filter =where reference_startswith=f"EXP_{annee}_") order by 9lebna
        dernier=cls.objects.filter(reference_startswith=f"EXP_{annee}_").order_by('-reference').first()
        compteur=int(dernier.reference[-5:])+1 if dernier else 1
        if compteur>99999:
            raise ValidationError("limite exceeded")
        return f"EXP_{annee}_{compteur:05d}"
    def save(self,*args,**kwargs):
        if not self.reference:
            self.reference=self._generate_reference()
        self.full_clean()
        super().save(*args,**kwargs)
