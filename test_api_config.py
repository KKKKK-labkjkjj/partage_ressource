#!/usr/bin/env python
"""
Script de test pour vérifier que l'API REST est bien configurée
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'partageRessource.settings')
sys.path.insert(0, r'd:\projet web\nouveau\partageRessource')

try:
    django.setup()
    print("✓ Django configuré avec succès")
    
    # Vérifier les imports
    from ressourceSection.serializers import AnnonceSerializer, EnseignantSerializer
    print("✓ Serializers importés avec succès")
    
    from ressourceSection.views import AnnonceViewSet, EnseignantViewSet
    print("✓ ViewSets importés avec succès")
    
    from ressourceSection import api_urls
    print("✓ URLs API importées avec succès")
    
    # Vérifier la configuration REST Framework
    from django.conf import settings
    if 'rest_framework' in settings.INSTALLED_APPS:
        print("✓ rest_framework installé dans INSTALLED_APPS")
    if 'rest_framework.authtoken' in settings.INSTALLED_APPS:
        print("✓ rest_framework.authtoken installé dans INSTALLED_APPS")
    
    print("\n✓ Tous les vérifications ont réussi !")
    print("\nProchaine étape : Exécutez 'python manage.py migrate'")
    
except Exception as e:
    print(f"✗ Erreur : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
