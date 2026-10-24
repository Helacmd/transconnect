from django.contrib import admin
from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise')
    list_filter = ('type_vehicule', 'disponible')
    search_fields = ('immatriculation', 'entreprise__raison_social')
    list_editable = ('disponible',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    autocomplete_fields = ('entreprise',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identification', {'fields': ('immatriculation', 'type_vehicule', 'entreprise')}),
        ('Capacité', {'fields': ('capacite_kg', 'disponible')}),
        ('Suivi', {'fields': ('created_at', 'updated_at')}),
    )