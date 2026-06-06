from django.db import models

# Create your models here.
doms = [
    ('ANA', 'analyse'),
    ('ALG', 'algebre'),
    ('Ph', 'Physique'),
    ('Chi', 'Chimie'),
    ('Bio', 'Biologie')
]

niv = [
    ('L1', 'Licence 1'),
    ('L2', 'Licence 2'),
    ('L3', 'Licence 3'), 
    ('M1', 'Master 1'),
    ('M2', 'Master 2'),
    ('D1', 'Doctorat1'),
    ('D2', 'Doctorat2')
]

stat = [
    ('prof', 'professeur simple'),
    ('ress', 'professeur responsable')
]

cycle = [
    ("C1", "premier cycle"),
    ("C2", "deuxieme cycle"),
    ("C3", "troisieme cycle")
]

types = [("se", "section informatique")]

genre=[("M", "Masculin"), ("F", "Féminin")]
sitmate=[("celib", "Célibataire"), ("marie", "Marié(e)"), ("divorce", "Divorcé(e)"), ("veuf", "Veuf(ve)")]
class etudiant(models.Model):
    email = models.EmailField(primary_key=True)
    numero_carte = models.CharField(max_length=50, null=True)
    nom = models.CharField(max_length=50, null=True)
    prenom = models.CharField(max_length=50, null=True)
    adresse = models.CharField(max_length=50, null=True)
    date_naiss = models.DateField(auto_now_add=True, null=True)
    genre = models.CharField(max_length=50, null=True, choices=genre)
    site_mat = models.CharField(max_length=50, null=True, choices=sitmate)
    tel = models.IntegerField(null=True)
    mot_pass = models.CharField(max_length=50, null=True)
    idclasse = models.ForeignKey('classe', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class administrateur(models.Model):
    emailadmin = models.EmailField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    mot_pass = models.CharField(max_length=50, null=True) 




class enseignant(models.Model):
    mailens = models.CharField(primary_key=True) 
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    specialite = models.CharField( choices=doms)
    mot_pass = models.CharField(max_length=50, null=True)
    emailadmin = models.ForeignKey('administrateur', on_delete=models.CASCADE, null=True)
    id_classe = models.ForeignKey('classe', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"Enseignant : {self.prenom} {self.nom}"


class reponsable(models.Model):
    mailesp = models.CharField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    specialite = models.CharField(max_length=50, choices=doms)
    mot_pass = models.CharField(max_length=50, null=True)
    emailadmin = models.ForeignKey('administrateur', on_delete=models.CASCADE, null=True)
    idclasse = models.ForeignKey('classe', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Responsable : {self.prenom} {self.nom}"


class classe(models.Model):
    idclasse = models.AutoField(primary_key=True)
    niveau = models.CharField(max_length=50, choices=niv)
    cycle = models.CharField(max_length=50, choices=cycle, null=True)
    emailadmin = models.ForeignKey(administrateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Classe {self.niveau}"


class module(models.Model):
    idmodule = models.AutoField(primary_key=True)
    nom_module = models.CharField(max_length=50)
    coefficient = models.IntegerField(null=True)
    durésemaine = models.IntegerField(null=True)
    emailresp = models.ForeignKey(reponsable, on_delete=models.CASCADE, null=True)
    idclasse = models.ForeignKey(classe, on_delete=models.CASCADE, null=True)
    enseignant = models.ForeignKey(enseignant, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.nom_module


class annonce(models.Model):
    idannonce = models.AutoField(primary_key=True)
    message = models.CharField(max_length=50)
    titre = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    mailres = models.ForeignKey(reponsable, on_delete=models.CASCADE, null=True)
    idclasse = models.ForeignKey(classe, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.titre


class consulterAnnonce(models.Model):
    id = models.AutoField(primary_key=True) 
    numero_carte = models.ForeignKey(etudiant, on_delete=models.CASCADE)
    idannonce = models.ForeignKey(annonce, on_delete=models.CASCADE)
    mailens = models.ForeignKey(enseignant, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('numero_carte', 'idannonce', 'mailens'),)


class ressource(models.Model):
    idressource = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='ressources/',null=True)
    
    idclasse = models.ForeignKey(classe, on_delete=models.CASCADE)
    mailens = models.ForeignKey(enseignant, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nom


class consulterRessource(models.Model):
    id = models.AutoField(primary_key=True) # Clé primaire explicite
    numero_carte = models.ForeignKey(etudiant, on_delete=models.CASCADE)
    idressource = models.ForeignKey(ressource, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)


class concernerAnnonce(models.Model):
    id = models.AutoField(primary_key=True) # Clé primaire explicite
    idannonce = models.ForeignKey(annonce, on_delete=models.CASCADE)
    idclasse = models.ForeignKey(classe, on_delete=models.CASCADE)


class concernerHistorique(models.Model):
    id = models.AutoField(primary_key=True) # Clé primaire explicite
    idressource = models.ForeignKey(ressource, on_delete=models.CASCADE)
    numero_carte = models.ForeignKey(etudiant, on_delete=models.CASCADE)
    emailens = models.ForeignKey(enseignant, on_delete=models.CASCADE)


class dispenser(models.Model):
    id = models.AutoField(primary_key=True) # Clé primaire explicite
    mailens = models.ForeignKey(enseignant, on_delete=models.CASCADE)
    idclasse = models.ForeignKey(classe, on_delete=models.CASCADE)



class note (models.Model):
    idnote = models.AutoField(primary_key=True)
    numero_carte = models.ForeignKey(etudiant, on_delete=models.CASCADE)
    idmodule = models.ForeignKey(module, on_delete=models.CASCADE)
    note = models.FloatField(null=True)