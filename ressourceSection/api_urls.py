from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from . import views

# Créer un routeur pour les viewsets
router = DefaultRouter()
router.register(r'annonces', views.AnnonceViewSet, basename='annonce')
router.register(r'enseignants', views.EnseignantViewSet, basename='enseignant')
router.register(r'concerner-annonces', views.ConcernerAnnonceViewSet, basename='concerner-annonce')
router.register(r'consulter-annonces', views.ConsulterAnnonceViewSet, basename='consulter-annonce')

app_name = 'api'

urlpatterns = [
    # Router pour les viewsets
    path('', include(router.urls)),
    
    # Authentification par token
    path('token-auth/', authtoken_views.obtain_auth_token, name='api_token_auth'),
]
