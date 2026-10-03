##Entree le 03/10/2026
-outil ia utilisée:
-prompt:
-sortie obtenue(résumé):
-écarts identifiés vs cahier des charges:
-correction apportée et justification:
#reponse d'exercice hunt
les 4 anomalies sont: 
1/prix ici est de type charfield or que dans la cahier de charge il s'agit d'un nombre decimal
2/de meme pour le delai_jours il s'agit d'un nombre positive et non pas seuelemnt integer
3/dans la relation ManyToOne on a mis Entreprise sans avoir importer le model de l'application specifique ça doit etre " from VehiculesApp.models  import vehicule" ou bien ecrice de dans VehiculesApp.vehicule
4/de meme pour transpoteur " from EntreprisesApp.models  import Entreprise" ou bien ecrire EntreprisesApp.Entreprise