from django.shortcuts import redirect, render, get_object_or_404

from .models import etudiant, enseignant, reponsable, classe, administrateur, module, annonce, ressource, note
from .form import classe_Form, enseignant_Form, etudiant_Form, responsable_Form, annonce_Form

# Create your views here.  

# Helper pour vérifier si un email existe dans les 4 tables
def email_existe(email):
    """Vérifie si un email existe dans l'une des 4 tables"""
    return (
        etudiant.objects.filter(email=email).exists() or
        enseignant.objects.filter(mailens=email).exists() or
        reponsable.objects.filter(mailesp=email).exists() or
        administrateur.objects.filter(emailadmin=email).exists()
    )


def get_session_responsable(request):
    mailesp = request.session.get('mailesp')
    if mailesp:
        try:
            return reponsable.objects.get(mailesp=mailesp)
        except reponsable.DoesNotExist:
            pass
    return None

#-----------------------------admin ,connexion, inscription-----------------------------
def accueil(request):
    return render(request, "page_accueil/acc_etu.html")     

def acc_prof(request):
    return render(request, "page_accueil/acc_prof.html")

def acc_admin(request):
    total_etudiants = etudiant.objects.count()
    total_enseignants = enseignant.objects.count()
    total_classes = classe.objects.count()
    total_responsables = reponsable.objects.count()
    
    classes = classe.objects.all()  

    context = {
        'total_etudiants': total_etudiants,
        'total_enseignants': total_enseignants,
        'total_classes': total_classes,
        'total_responsables': total_responsables,
        'classes': classes
    }
    return render(request, "page_accueil/acc_admin.html", context)

def acc_res(request):
    return render(request, "page_accueil/acc_res.html")

def gest_etu(request):

    etudiants = etudiant.objects.all()

    return render(request, "page_gest/gest_etu.html", {'etudiants': etudiants})

def gest_prof(request):
    enseignants = enseignant.objects.all()
    return render(request, "page_gest/gest_prof.html", {'enseignants': enseignants})

def gest_res(request):
    reponsables = reponsable.objects.all()
    return render(request, "page_gest/gest_res.html", {'reponsables': reponsables})

def gest_class(request):
    classes = classe.objects.all()
    classe_Forms = classe_Form()
    return render(request, "page_gest/gest_class1.html", {'classes': classes, 'form': classe_Forms})



def afficher_classe(request, idclasse):
    classes = classe.objects.get(idclasse=idclasse)
    etudiants= etudiant.objects.filter(idclasse=classes)
    return render(request, 'action_classe/afficher_classe.html', {'classes': classes, 'etudiants': etudiants})

def connexion(request):
    if request.method == 'POST':
        nom_util = request.POST.get('nom_util')
        mot_pass = request.POST.get('mot_pass')
        
        exist_etu = etudiant.objects.filter(email=nom_util, mot_pass=mot_pass).exists()
        exist_prof = enseignant.objects.filter(mailens=nom_util, mot_pass=mot_pass).exists() # 'mail' au lieu de 'mailens'
        exist_res = reponsable.objects.filter(mailesp=nom_util, mot_pass=mot_pass).exists()   # 'mail' au lieu de 'mailesp'
        exist_admin = administrateur.objects.filter(emailadmin=nom_util, mot_pass=mot_pass).exists()
        
        if exist_etu:
            return render(request, "page_accueil/acc_etu.html")
        elif exist_prof:
            request.session['mailens'] = nom_util
            request.session['user_type'] = 'enseignant'
            if exist_res: 
                request.session['mailesp'] = nom_util
                request.session['user_type'] = 'responsable'
                responsables = reponsable.objects.get(mailesp=nom_util)
                idclasse_res = responsables.idclasse
                total_etudiants = etudiant.objects.filter(idclasse=idclasse_res).count()
                total_enseignants = enseignant.objects.filter(id_classe=idclasse_res).count()
                
                return render(request, "page_accueil/acc_res.html", {"responsables": responsables, "total_etudiants": total_etudiants})
            else:
                 
                 return render(request, "page_accueil/acc_prof.html")


        elif exist_admin:
            classes = classe.objects.all()
            admins = administrateur.objects.get(emailadmin=nom_util)
            # calcul des totaux pour le tableau de bord
            total_etudiants = etudiant.objects.count()
            total_enseignants = enseignant.objects.count()
            total_classes = classe.objects.count()
            total_responsables = reponsable.objects.count()
            context = {
                'total_etu': total_etudiants,
                'total_prof': total_enseignants,
                'total_class': total_classes,
                'total_resp': total_responsables,
                'classes': classes,
                'admins': admins,

            }
            

            return render(request, "page_accueil/acc_admin.html" , context)
        else:
            err = "Nom d'utilisateur ou mot de passe incorrect"
            return render(request, "connexion.html", {"err": err})
    return render(request, "connexion.html", locals())

def inscription(request):
    etudiant_Forms= etudiant_Form()
    if request.method == 'POST':
        etudiant_Forms = etudiant_Form(request.POST)
        if etudiant_Forms.is_valid():
            email = etudiant_Forms.cleaned_data.get('email')
            if email_existe(email):
                etudiant_Forms.add_error('email', 'Cet email est déjà utilisé dans le système.')
                return render(request, "pages_ajout/inscription.html", {"form": etudiant_Forms})
            etudiant_Forms.save()
            return redirect('connexion')
   
    return render(request, "pages_ajout/inscription.html", {"form": etudiant_Forms})

def ajout_prof(request):
    if request.method == 'POST':
        form = enseignant_Form(request.POST)
        if form.is_valid():
            mailens = form.cleaned_data.get('mailens')
            if email_existe(mailens):
                form.add_error('mailens', 'Cet email est déjà utilisé dans le système.')
                return render(request, 'pages_ajout/ajout_prof.html', {'form': form})
            form.save()
            return redirect('acc_admin')
    else:
        form = enseignant_Form()
        
    return render(request, 'pages_ajout/ajout_prof.html', {'form': form})






def modifier_prof(request, mailens):
    enseignants = enseignant.objects.get(mailens=mailens)
    if request.method == 'POST':
        form = enseignant_Form(request.POST, instance=enseignants)
        if form.is_valid():
            mailens = form.cleaned_data.get('mailens')
            if email_existe(mailens) and mailens != enseignants.mailens:
                form.add_error('mailens', 'Cet email est déjà utilisé dans le système.')
                return render(request, 'action_prof/modifier_prof.html', {'form': form, 'enseignants': enseignants})
            form.save()
            return redirect('acc_admin')
    else:
        form = enseignant_Form(instance=enseignants)
        
    return render(request, 'action_prof/modifier_prof.html', {'form': form, 'enseignants': enseignants})    


def supprimer_prof(request, mailens):
    enseignants = enseignant.objects.get(mailens=mailens)
    if request.method == 'POST':
        enseignants.delete()
        return redirect('gest_prof')
       
    return render(request, 'page_gest/gest_prof.html', {'enseignants': enseignants})


def detail_enseignant(request, mailens):    
    # 1. On récupère l'enseignant grâce à son email
    enseignants = enseignant.objects.get(mailens=mailens)
    
    # 2. Sécurité : On teste si le champ de la clé étrangère 'id_classe' n'est pas vide
    if enseignants.id_classe is not None:
        id_numerique = enseignants.id_classe.idclasse
        classes = classe.objects.get(idclasse=id_numerique)
    else:
        classes = None  # Si aucun lien n'existe, on définit la variable à None sans faire planter Django

    # 3. On envoie les données proprement au template HTML
    return render(request, 'action_enseignant/detail_enseignant.html', {
        'enseignants': enseignants, 
        'classes': classes
    })

def ajout_res(request):
    # 1. On récupère les enseignants qui ne sont pas encore responsables
    emails_responsables = reponsable.objects.values_list('mailesp', flat=True)
    enseignants_disponibles = enseignant.objects.exclude(mailens__in=emails_responsables)
    
    error_message = None

    if request.method == 'POST':
        # 2. COMPTAGE : On vérifie combien de responsables existent déjà dans la base
        total_responsables = reponsable.objects.count()

        # 3. BLOCAGE : Si on a atteint ou dépassé 7, on refuse l'insertion
        if total_responsables >= 8:
            error_message = "Impossible d'ajouter un responsable. La limite maximale de 7 responsables est atteinte."
        else:
            mailesp = request.POST.get('mailesp')
            if mailesp:
                try:
                    prof = enseignant.objects.get(mailens=mailesp)
                    
                    # Création du responsable si la limite n'est pas atteinte
                    reponsable.objects.create(
                        mailesp=prof.mailens,
                        nom=prof.nom,
                        prenom=prof.prenom,
                        numero=prof.numero,
                        specialite=prof.specialite,
                        mot_pass=prof.mot_pass,
                        emailadmin=prof.emailadmin,
                        idclasse=None
                    )
                    return redirect('gest_res') # Redirection vers la gestion des responsables
                    
                except enseignant.DoesNotExist:
                    error_message = "Cet enseignant n'existe pas."
                except Exception as e:
                    error_message = f"Une erreur est survenue lors de l'ajout : {e}"

    context = {
        'enseignants': enseignants_disponibles,
        'error_message': error_message
    }
    return render(request, 'pages_ajout/ajout_res.html', context)
def supprimer_res(request, mailesp):
    responsables = reponsable.objects.get(mailesp=mailesp)
    if request.method == 'POST':
        responsables.delete()
        return redirect('gest_res')
       
    return render(request, 'page_gest/gest_res.html', {'responsables': responsables})


def modifier_res(request, mailesp):
    #modifier seulement la classe du responsable
    responsables = reponsable.objects.get(mailesp=mailesp)
    classes = classe.objects.all()

    if request.method == 'POST':
        classe_id = request.POST.get('classes')
        classe_a_affecter = classe.objects.get(idclasse=classe_id)
        responsables.idclasse = classe_a_affecter
        responsables.save()
       
    
    return render(request, 'action_res/modifier_res.html', {'responsables': responsables, 'classes': classes})

                        #etudiant
def detail_etudiant(request, email):    
    etudiants = etudiant.objects.get(email=email)
    
    id_numerique = etudiants.idclasse.idclasse  
    
    classes = classe.objects.get(idclasse=id_numerique)  
    
    return render(request, 'action_etudiant/detail_etudiant.html', {
        'etudiants': etudiants, 
        'classes': classes
    })

def supprimer_etudiant(request, email):
    etudiants = etudiant.objects.get(email=email)
    if request.method == 'POST':
        etudiants.delete()
        return redirect('gest_etu')
    return render(request, 'action_etudiant/supprimer_etudiant.html', {'etudiants': etudiants})

def modifier_etudiant(request, email):
    etudiants = etudiant.objects.get(email=email)
    etudiant_Forms = etudiant_Form(instance=etudiants)
    if request.method == 'POST':
        form = etudiant_Form(request.POST, instance=etudiants)
        if form.is_valid():
            form.save()
            return redirect('gest_etu')
    else:
        form = etudiant_Form(instance=etudiants)
    return render(request, 'action_etudiant/modifier_etudiant.html', {'form': form})


                          #classe



def gest_class(request):
    classes = classe.objects.all()
   
    classe_Forms = classe_Form()
    return render(request, "page_gest/gest_class1.html", {'classes': classes, 'form': classe_Forms})


def afficher_classe(request, idclasse):
    classes = classe.objects.get(idclasse=idclasse)
    res= reponsable.objects.filter(idclasse=classes) 


    etudiants= etudiant.objects.filter(idclasse=classes)

    return render(request, 'action_classe/afficher_classe.html', {'classes': classes, 'etudiants': etudiants, 'res': res})


def ajout_class(request):
    if request.method == 'POST':
        form = classe_Form(request.POST)
        if form.is_valid():
            form.save()
            
    else:
        form = classe_Form()
        
    return render(request, 'pages_ajout/ajou_class.html', {'form': form})



def detail_class(request):
    classes= classe.objects.all()
    return render(request, 'action_classe/detail_class.html', {  'classes': classes})


def modifier_class(request, idclasse):
    classes = classe.objects.get(idclasse=idclasse)
    if request.method == 'POST':
        form = classe_Form(request.POST, instance=classes)
        if form.is_valid():
            form.save()
            return redirect('acc_admin')
    else:
        form = classe_Form(instance=classes)
        
    return render(request, 'action_classe/modifier.html', {'form': form, 'classes': classes})



def supprimer_class(request, idclasse):
    
    classes = classe.objects.get(idclasse=idclasse)
    if request.method == 'POST':
        classes.delete()
       
        
    return render(request, 'action_classe/supprimer_class.html', {'classes': classes})



def affecter_class(resquest):   
    reponsables=reponsable.objects.all()
    classes=classe.objects.all()
    
    return render(resquest,'action_classe/affecter_class.html', {
        'reponsables': reponsables,
        'classes': classes
    })


def class_a_affecter(resquest,mailesp):
    reponsables=reponsable.objects.all()
    responsable_a_affecter = reponsable.objects.get(mailesp=mailesp)
    
    # Récupérer les classes non assignées (ou assignées au responsable actuel)
    classes_assignees = reponsable.objects.filter(idclasse__isnull=False).exclude(mailesp=mailesp).values_list('idclasse', flat=True)
    classes_disponibles = classe.objects.exclude(idclasse__in=classes_assignees)
    
    error_message = None
    success_message = None
    
    if resquest.method=='POST':
        action = resquest.POST.get('action')
        
        # Action de retirer une classe
        if action == 'retirer':
            responsable_a_affecter.idclasse = None
            responsable_a_affecter.save()
            success_message = "Classe retirée avec succès."
            return redirect('acc_admin')
        
        # Action d'affecter une classe
        elif action == 'affecter':
            classe_id = resquest.POST.get('classe')
            classe_a_affecter = classe.objects.get(idclasse=classe_id)
            
            # Vérifier si la classe est déjà assignée à un autre responsable
            if reponsable.objects.filter(idclasse=classe_a_affecter).exclude(mailesp=mailesp).exists():
                error_message = "Cette classe est déjà assignée à un autre responsable."
                return render(resquest, 'action_classe/class_a_affecter.html', {
                    'reponsables': reponsables, 
                    'classes': classes_disponibles,
                    'responsable_actuel': responsable_a_affecter,
                    'error_message': error_message
                })
            
            responsable_a_affecter.idclasse = classe_a_affecter
            responsable_a_affecter.save()
            return redirect('acc_admin')
       
    return render(resquest,'action_classe/class_a_affecter.html', {
        'reponsables': reponsables,
        'classes': classes_disponibles,
        'responsable_actuel': responsable_a_affecter,
        'error_message': error_message,
        'success_message': success_message
    })






def index(request):
    return render(request, 'index.html')




#-------------------------------------responsable-----------------------------


def gest_res_etu(request,mailesp):
    res= reponsable.objects.get(mailesp=mailesp)
    idclasse_res = res.idclasse

    etudiants = etudiant.objects.filter(idclasse=idclasse_res)

    return render(request, "responsable/gestion_etudiant.html", {'etudiants': etudiants, 'responsables': res})

def gest_res_prof(request, mailesp):
    res = reponsable.objects.get(mailesp=mailesp)
    idclasse_res = res.idclasse
    enseignants = enseignant.objects.filter(id_classe=idclasse_res).prefetch_related('module_set')
 
    modules = module.objects.filter(idclasse=idclasse_res)
    return render(request, "responsable/gestion_prof.html", {'enseignants': enseignants , 'responsables': res, 'modules': modules })


def gest_res_class(request, idclasse):
    res = reponsable.objects.get(idclasse=idclasse)
    classes = classe.objects.filter(idclasse=idclasse)
    modules = module.objects.filter(idclasse__idclasse=idclasse)
    return render(request, "responsable/gestion_classe.html", {'classes': classes , 'responsables': res, 'modules': modules})


def det_class_res(request, idclasse): 
    res = reponsable.objects.filter(idclasse=idclasse) # filter au cas où il y en a plusieurs, ou .get() si unique
    classes = get_object_or_404(classe, idclasse=idclasse)
    etudiants = etudiant.objects.filter(idclasse=classes).order_by('nom', 'prenom')
    # Récupérer les modules associés à cette classe
    modules = module.objects.filter(idclasse=classes).order_by('nom_module') 
    notes_qs = note.objects.filter(idmodule__in=modules, numero_carte__in=etudiants)

    # Construire une structure rows pour le template : liste de {'etu': etu, 'notes': [note_par_module...]}
    rows = []
    for etu in etudiants:
        row_notes = []
        for mod in modules:
            n = notes_qs.filter(idmodule=mod, numero_carte=etu).first()
            row_notes.append(n.note if n and n.note is not None else None)
        rows.append({'etu': etu, 'notes': row_notes})

    context = {
        'classes': classes, 
        'etudiants': etudiants, 
        'res': res,
        'modules': modules, # On envoie les modules au template
        'rows': rows, # lignes pré-calculées (étudiant + notes)
    }
    
    return render(request, 'responsable/detail_classe.html', context)

def ajout_pr(request):
    responsables = get_session_responsable(request)

    enseignants = enseignant.objects.all()
    context = {
        'enseignants': enseignants,
        'responsables': responsables,
    }

    return render(request, "responsable/ajout_pr.html", context)




def assigner_prof(request, mailesp):
    responsables = get_session_responsable(request)
    
    # Sécurité : On récupère l'enseignant ou on renvoie une erreur 404 s'il n'existe pas
    enseignants = get_object_or_404(enseignant, mailens=mailesp)
    
    idclasse_res = responsables.idclasse
    modules = module.objects.filter(idclasse=idclasse_res)
    
    # OBLIGATOIRE : On écoute explicitement la soumission du formulaire en POST
    if request.method == 'POST':
        assigner = request.POST.get('assigner')
        
        if assigner:
            module_a_assigner = module.objects.get(idmodule=assigner)
            
            # ATTENTION : Vérifie bien le nom du champ dans ton modèle "module"
            # Si ton champ ForeignKey s'appelle 'mailens', écris : module_a_assigner.mailens = enseignants
            # Si ton champ ForeignKey s'appelle 'enseignant', laisse la ligne ci-dessous :
            module_a_assigner.enseignant = enseignants
            
            module_a_assigner.idclasse = idclasse_res
            module_a_assigner.save() # Sauvegarde dans la base de données
            enseignants.id_classe = idclasse_res
            enseignants.save() # Sauvegarde de l'enseignant avec la classe assignée
            # Redirection après succès
            return redirect('ajout_pr')
            
    context = {
        'modules': modules,
        'responsables': responsables,
        'enseignant_selectionne': enseignants,
    }
    return render(request, "responsable/assigner_prof.html", context)



def base_res(request):
    responsables = get_session_responsable(request)
    return render(request, "base_res.html", {'responsables': responsables})





def modifier_prof_res(request, mailens):
    enseignants = enseignant.objects.get(mailens=mailens)
    if request.method == 'POST':
        form = enseignant_Form(request.POST, instance=enseignants)
        if form.is_valid():
            mailens = form.cleaned_data.get('mailens')
            if email_existe(mailens) and mailens != enseignants.mailens:
                form.add_error('mailens', 'Cet email est déjà utilisé dans le système.')
                return render(request, 'responsable/modifier_prof.html', {'form': form, 'enseignants': enseignants})
            form.save()
            return redirect('acc_admin')
    else:
        form = enseignant_Form(instance=enseignants)
        
    return render(request, 'responsable/modifier_prof.html', {'form': form, 'enseignants': enseignants})    


def supprimer_prof_res(request, mailens):
    enseignants = enseignant.objects.get(mailens=mailens)
    if request.method == 'POST':
        enseignants.delete()
        return redirect('gest_prof')
       
    return render(request, 'responsable/gestion_prof.html', {'enseignants': enseignants})

def gest_res_annone(request, mailesp):
    res = reponsable.objects.get(mailesp=mailesp)
    
   
    # Récupérer les annonces de cet enseignant
    annonces = annonce.objects.filter(mailres=res).order_by('-idannonce') if res else annonce.objects.none()
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        objets = request.POST.get('objets')
        type_annonce = request.POST.get('type')
        
        if titre and objets and type_annonce and res:
            annonce.objects.create(
                titre=titre,
                objets=objets,
                type=type_annonce,
                mailres=res
            )
            return redirect('gest_res_annone', mailesp=mailesp)
    
    return render(request, "responsable/gestion_annonce.html", {
        'annonces': annonces,
        'responsables': res
    })


def gest_annonce_et_ressource(request, mailesp):
    return render(request, "responsable/gest_annonce_et_ressource.html", {'mailesp': mailesp})


def gest_res_ressource(request, mailesp):
    res = reponsable.objects.get(mailesp=mailesp)
    ressources = ressource.objects.filter(idclasse=res.idclasse).order_by('-idressource')
    return render(request, "responsable/gestion_ressource.html", {
        'ressources': ressources,
        'responsables': res
    })