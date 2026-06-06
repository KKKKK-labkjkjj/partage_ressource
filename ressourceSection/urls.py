from django.urls import path
from . import views
urlpatterns = [
path('', views.connexion, name='connexion'),
path('accueil', views.accueil, name='accueil'),
path('acc_admin/', views.acc_admin, name='acc_admin'),
path("acc_res", views.acc_res, name="acc_res"),

path('gest_etu/', views.gest_etu, name='gest_etu'),
path('gest_prof/', views.gest_prof, name='gest_prof'),
path('gest_res/', views.gest_res, name='gest_res'),
path('gest_class/', views.gest_class, name='gest_class'),
            #enseignant
path('ajout_prof/', views.ajout_prof, name='ajout_prof'),
path('modifier_prof/<str:mailens>/', views.modifier_prof, name='modifier_prof'),
path('supprimer_prof/<str:mailens>/', views.supprimer_prof, name='supprimer_prof'),
path('acc_prof/', views.acc_prof, name='acc_prof'),
path('ajout_res/', views.ajout_res, name='ajout_res'),
path('ajout_class/', views.ajout_class, name='ajout_class'),
path('detail_enseignant/<str:mailens>/', views.detail_enseignant, name='detail_enseignant'),

            #etudiant
path('detail_etudiant/<str:email>/', views.detail_etudiant, name='detail_etudiant'),
path('supprimer_etudiant/<str:email>/', views.supprimer_etudiant, name='supprimer_etudiant'),
path('modifier_etudiant/<str:email>/', views.modifier_etudiant, name='modifier_etudiant'),
            #classe
path('modifier_class/<int:idclasse>/', views.modifier_class, name='modifier_class'),
path('supprimer_class/<int:idclasse>/', views.supprimer_class, name='supprimer_class'),
path('affecter_class/', views.affecter_class, name='affecter_class'),
path('affecter une classe/<str:mailesp>/', views.class_a_affecter, name='class_a_affecter'),
path('detail_class/<int:idclasse>/', views.detail_class, name='detail_class'),
            #responsable
path('modifier_res/<str:mailesp>/', views.modifier_res, name='modifier_res'),
path('supprimer_res/<str:mailesp>/', views.supprimer_res, name='supprimer_res'),




#path('detail_class/<int:idclasse>/', views.detail_class, name='detail_class'),
path('detail_class/', views.detail_class, name='detail_class'),
path('afficher_classe/<int:idclasse>/', views.afficher_classe, name='afficher_classe'),

path('inscription/', views.inscription, name='inscription'),
#___________________________________responsable________________________

path('gestion_etudiants/<str:mailesp>/', views.gest_res_etu, name='gest_res_etu'),
path('gestion_proffesseurs/<str:mailesp>/', views.gest_res_prof, name='gest_res_prof'),
path('gestion_classes/<int:idclasse>/', views.gest_res_class, name='gest_res_class'),
path('ajout_pr/', views.ajout_pr, name='ajout_pr'),
path('assigner_prof/<str:mailesp>/', views.assigner_prof, name='assigner_prof'),
path("supprimer_prof_res/<str:mailens>/", views.supprimer_prof_res, name="supprimer_prof_res"),
path("modifier_prof_res/<str:mailens>/", views.modifier_prof_res, name="modifier_prof_res"),
path('det_class_res/<int:idclasse>/', views.det_class_res, name='det_class_res'),
path('gestion_annonce/<str:mailesp>/', views.gest_res_annone, name='gest_res_annone'),
path('gestion_ressource/<str:mailesp>/', views.gest_res_ressource, name='gest_res_ressource'),
path('annonce+ressource/<str:mailesp>/', views.gest_annonce_et_ressource, name='gest_annonce_et_ressource'),


path('index/', views.index, name='index'),
]
