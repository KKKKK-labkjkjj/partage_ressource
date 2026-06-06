from rest_framework import serializers
from .models import annonce, enseignant, etudiant, consulterAnnonce, concernerAnnonce


class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = enseignant
        fields = ['mailens', 'nom', 'prenom', 'numero', 'specialite']
        read_only_fields = ['mailens']


class AnnonceSerializer(serializers.ModelSerializer):
    mailens_detail = EnseignantSerializer(source='mailens', read_only=True)
    
    class Meta:
        model = annonce
        fields = ['idannonce', 'objets', 'titre', 'type', 'mailens', 'mailens_detail']
        read_only_fields = ['idannonce', 'mailens']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                ens = enseignant.objects.get(mailens=request.user.username)
                validated_data['mailens'] = ens
            except enseignant.DoesNotExist:
                raise serializers.ValidationError(
                    "L'utilisateur n'est pas un enseignant enregistré."
                )
        return super().create(validated_data)


class ConcernerAnnonceSerializer(serializers.ModelSerializer):
    annonce_detail = AnnonceSerializer(source='idannonce', read_only=True)
    
    class Meta:
        model = concernerAnnonce
        fields = ['id', 'idannonce', 'idclasse', 'annonce_detail']


class ConsulterAnnonceSerializer(serializers.ModelSerializer):
    annonce_detail = AnnonceSerializer(source='idannonce', read_only=True)
    enseignant_detail = EnseignantSerializer(source='mailens', read_only=True)
    
    class Meta:
        model = consulterAnnonce
        fields = ['id', 'numero_carte', 'idannonce', 'mailens', 'annonce_detail', 'enseignant_detail']
        read_only_fields = ['id', 'numero_carte']
