from .models import etudiant,enseignant,reponsable,classe,administrateur,module,annonce
from django.forms import ModelForm
class etudiant_Form(ModelForm):
    class Meta:
        model=etudiant
        fields='__all__'

class enseignant_Form(ModelForm):
    class Meta:
        model=enseignant
        fields='__all__'

class responsable_Form(ModelForm):
    
    class Meta:
        model=reponsable
        fields='__all__'
    

class classe_Form(ModelForm):
    class Meta:
        model=classe
        fields='__all__'

class annonce_Form(ModelForm):
    class Meta:
        model=annonce
        fields=['message', 'titre', 'type']
        