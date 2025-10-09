# &#128570; Projet de Chatbot &#128570; 

## &#128203; Généralités :
- python3.12 / django 5.2 
- base de donnée mysql ou postgresql
- auteur : 
- admin : adminDemo
- pw :    0000

##  &#8205;&#127891; Démonstration : [ici](https://www.xxxxxx.fr)

## &#129520; Fonctionnalités :
### Fonctionnalités 
### Fonctionnalités 




## &#129489;&#8205;&#127891; Les utilisateurs :

- #### cas 1 : 
   
- #### cas 2 : 
        
## &#129489;&#8205;&#129309;&#8205;&#129489;  Les groupes :


## &#128736; Installation : 

- installer pyenv, poetry et python3 v3.12 :
```bash
    curl https://pyenv.run | bash
    curl -sSL https://install.python-poetry.org | python3
    pyenv local 3.12.10
```

- cloner le projet :
```bash
    git clone https://xxxxxxxxx.git
```
- créer une base de donnée Mysql ou Postgresql

- en développement, créer et paramétrer /mooc/mooc/settings/develop.py, ou bien définir des variables d'environnement :
    ```bash 
        SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxx'
        DEBUG = True
        ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
        CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]
        PROTOCOL = "http"
        SITE_ID = 1
        DATABASES = {
            'default':  {
                'ENGINE': 'django.db.backends.postgresql' ou 'django.db.backends.mysql,
                'NAME': 'xxxxxxxxxxxx',
                'USER': 'xxxxxxxxxxxx',
                'PASSWORD': 'xxxxxxxxxxxxx',
                'HOST': '127.0.0.1',
                'PORT': xxxx,
            }
        }
        
    ``` 
- en production, créer et paramétrer /mooc/mooc/settings/production.py ou bien définir des variables d'environnement,:
    ```bash 
        SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxx'
        DEBUG = False
        ALLOWED_HOSTS = ['www.xxxxx.xx', ... ]
        CSRF_TRUSTED_ORIGINS = ['https://www.xxxxx.xx', ... ]
        PROTOCOL = 'https'
        SITE_ID = 1
        DATABASES = {
            'default':  {
                'ENGINE': 'django.db.backends.postgresql' ou 'django.db.backends.mysql,
                'NAME': 'xxxxxxxxxxxx',
                'USER': 'xxxxxxxxxxxx',
                'PASSWORD': 'xxxxxxxxxxxxx',
                'HOST': '127.0.0.1',
                'PORT': xxxx,
            }
        }
        STATIC_ROOT = 'chemin vers fichiers statiques sur le serveur'
        MEDIA_ROOT =  'chemin vers fichiers media sur le serveur'
    ``` 

- installer les dépendances, définies dans le fichier **pyproject.toml** :
    ```bash
        poetry install
    ```

- activer l'environnement virtuel:
    sur console du serveur, à la racine du projet (dossier /Mooc/ ) :
    ```bash 
        source .venv/bin/activate
    ```
    - première migration de la base de donnée :
    ```bash
        ./mooc/manage.py migrate
    ```
    - création du superuser (administrateur):
    ```bash
        ./mooc/manage.py createsuperuser
    ```
    - création des groupes, catégories et pré-remplissage de la bd (valeurs par défaut):
    ```bash
        ./mooc/manage.py initgroups
    ```
    - initialisation tailwind :
    ```bash
        ./mooc/manage.py tailwind install
        ./mooc/manage.py tailwind build
    ```

    - collecte des fichiers statiques (en production) :
    ```bash
        ./mooc/manage.py collectstatic
    ```

    - lancer le serveur (voir ci-dessous), se connecter en tant qu'administrateur et aller sur l'administration django
        - modifier le user : entrer subId (random), nom, prénom, group (auteur, gestionnaire, admin)        
        - compléter les champs image et fichier des tables home/libelles et home/defaultcontent

## &#128640; Lancement du serveur de développement :
- option 1 : en ligne de commande
    ```bash
        ./mooc/manage.py tailwind dev
    ```


## &#8505;&#65039; Informations :

    dépendances : pyproject.toml
    


