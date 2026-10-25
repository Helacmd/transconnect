from datetime import timedelta

from django.contrib import admin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import path
from django.utils import timezone

from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import Expedition
from .models import Offre


def controle_offres_orphelines():
    offres = (
        Offre.objects
        .filter(statut__in=['proposee', 'acceptee'])
        .exclude(expedition__statut__in=['publiee', 'attribuee'])
        .select_related('expedition', 'transporteur')
    )
    return {
        'titre': "1. Offres orphelines",
        'regle': "Une offre proposée ou acceptée doit porter sur une expédition publiée ou attribuée.",
        'colonnes': ['Offre', 'Expédition', 'Statut expédition', 'Transporteur', 'Statut offre'],
        'lignes': [
            (o.pk, o.expedition.reference, o.expedition.statut, o.transporteur.raison_sociale, o.statut)
            for o in offres
        ],
    }


def controle_expeditions_bloquees():
    limite = timezone.now() - timedelta(days=7)
    expeditions = Expedition.objects.filter(statut='publiee', created_at__lt=limite)
    return {
        'titre': "2. Expéditions bloquées",
        'regle': "Une expédition publiée depuis plus de 7 jours sans être attribuée est bloquée.",
        'colonnes': ['Expédition', 'Statut', 'Créée le'],
        'lignes': [(e.reference, e.statut, e.created_at.date()) for e in expeditions],
    }


def controle_transporteurs_sans_flotte():
    transporteurs = (
        Entreprise.objects
        .filter(type_entreprise='transporteur')
        .annotate(nb_vehicules=Count('vehicules'))
        .filter(nb_vehicules=0)
    )
    return {
        'titre': "3. Transporteurs sans flotte",
        'regle': "Une entreprise de type transporteur doit posséder au moins un véhicule.",
        'colonnes': ['Entreprise', 'Matricule fiscal'],
        'lignes': [(t.raison_sociale, t.matricule_fiscal) for t in transporteurs],
    }


def controle_doublons_proposition():
    doublons = (
        Offre.objects
        .filter(statut='proposee')
        .values('expedition', 'transporteur', 'expedition__reference', 'transporteur__raison_sociale')
        .annotate(nb=Count('id'))
        .filter(nb__gt=1)
    )
    return {
        'titre': "4. Doublons de proposition",
        'regle': "Une entreprise ne peut avoir qu'une seule offre proposée par expédition.",
        'colonnes': ['Expédition', 'Transporteur', "Nombre d'offres proposées"],
        'lignes': [
            (d['expedition__reference'], d['transporteur__raison_sociale'], d['nb'])
            for d in doublons
        ],
    }


def controle_attribution_incoherente():
    offres = (
        Offre.objects
        .filter(
            Q(statut='acceptee', expedition__statut='publiee')
            | Q(statut='proposee', expedition__statut__in=['attribuee', 'en_cours', 'livree'])
        )
        .select_related('expedition', 'transporteur')
    )
    return {
        'titre': "5. Attribution incohérente (contrôle ajouté)",
        'regle': "Une offre acceptée implique une expédition attribuée, et les autres offres proposées sur cette expédition doivent être refusées.",
        'colonnes': ['Offre', 'Expédition', 'Statut expédition', 'Transporteur', 'Statut offre'],
        'lignes': [
            (o.pk, o.expedition.reference, o.expedition.statut, o.transporteur.raison_sociale, o.statut)
            for o in offres
        ],
    }


def health_check_view(request):
    controles = [
        controle_offres_orphelines(),
        controle_expeditions_bloquees(),
        controle_transporteurs_sans_flotte(),
        controle_doublons_proposition(),
        controle_attribution_incoherente(),
    ]
    contexte = {
        **admin.site.each_context(request),
        'title': "Contrôle d'intégrité",
        'controles': controles,
        'total': sum(len(c['lignes']) for c in controles),
    }
    return render(request, 'admin/health_check.html', contexte)


# Surcharge de get_urls() sur le site admin
if not getattr(admin.site, '_health_check_installe', False):
    _get_urls_original = admin.site.get_urls

    def _get_urls_avec_health_check():
        urls_perso = [
            path('health-check/', admin.site.admin_view(health_check_view), name='health-check'),
        ]
        return urls_perso + _get_urls_original()

    admin.site.get_urls = _get_urls_avec_health_check
    admin.site._health_check_installe = True