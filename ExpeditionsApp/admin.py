from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from ExpeditionsApp.models import Expedition
from OffresApp.models import Offre


class EnRetardFilter(admin.SimpleListFilter):
    title = 'en retard'
    parameter_name = 'en_retard'

    def lookups(self, request, model_admin):
        return [('oui', 'Oui'), ('non', 'Non')]

    def queryset(self, request, queryset):
        aujourd_hui = timezone.now().date()
        if self.value() == 'oui':
            return queryset.filter(statut='publiee', date_souhaitee__lt=aujourd_hui)
        if self.value() == 'non':
            return queryset.exclude(statut='publiee', date_souhaitee__lt=aujourd_hui)
        return queryset


class OffreInline(admin.StackedInline):
    model = Offre
    fk_name = 'expedition'
    extra = 0
    can_delete = False
    show_change_link = True
    readonly_fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'entreprise', 'ville_depart', 'ville_arrivee', 'statut', 'statut_colore', 'date_souhaitee')
    list_filter = ('statut', 'ville_depart', EnRetardFilter)
    search_fields = ('reference', 'entreprise__raison_social')
    list_editable = ('statut',)
    ordering = ('-created_at',)
    date_hierarchy = 'date_souhaitee'
    list_per_page = 25
    autocomplete_fields = ('entreprise',)
    readonly_fields = ('reference', 'statut_colore', 'created_at', 'updated_at')
    fieldsets = (
        ('Trajet', {'fields': ('ville_depart', 'ville_arrivee', 'date_souhaitee')}),
        ('Chargement', {'fields': ('entreprise', 'poids_kg', 'description')}),
        ('Suivi', {'fields': ('reference', 'statut', 'statut_colore', 'created_at', 'updated_at')}),
    )
    inlines = [OffreInline]
    actions = ['cloturer_expeditions']

    @admin.display(description='Badge')
    def statut_colore(self, obj):
        couleurs = {
            'publiee': '#F0AD4E',
            'attribuee': '#5BC0DE',
            'en_cours': '#0275D8',
            'livree': '#5CB85C',
            'annulee': '#D9534F',
        }
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#999'),
            obj.get_statut_display(),
        )

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def cloturer_expeditions(self, request, queryset):
        cloturees = 0
        ignorees = 0
        for expedition in queryset:
            if expedition.statut != 'en_cours':
                ignorees += 1
                continue
            expedition.statut = 'livree'
            expedition.full_clean()
            expedition.save()
            cloturees += 1
        self.message_user(
            request,
            f"{cloturees} expédition(s) clôturée(s), {ignorees} ignorée(s)."
        )


# Branding de l'admin
admin.site.site_header = "TransConnect — Administration"
admin.site.site_title = "TransConnect Admin"
admin.site.index_title = "Espace opérations TransConnect"