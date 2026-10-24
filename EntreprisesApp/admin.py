from django.contrib import admin
from .models import Entreprise, Utilisateur
from VehiculesApp.models import Vehicule


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'user_id')
    list_editable = ('role',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    readonly_fields = ('user_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Connexion', {'fields': ('username', 'password')}),
        ('Informations', {'fields': ('email', 'first_name', 'last_name', 'telephone', 'role')}),
        ('Suivi', {'fields': ('user_id', 'is_active', 'created_at', 'updated_at')}),
    )


class VehiculeInline(admin.TabularInline):
    model = Vehicule
    extra = 0
    fields = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible')


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_social', 'matricule_fiscal', 'type_entreprise', 'gerant', 'created_at')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_social', 'matricule_fiscal')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    autocomplete_fields = ('gerant',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identité', {'fields': ('raison_social', 'matricule_fiscal', 'type_entreprise')}),
        ('Coordonnées', {'fields': ('adress', 'gerant')}),
        ('Suivi', {'fields': ('created_at', 'updated_at')}),
    )
    inlines = [VehiculeInline]