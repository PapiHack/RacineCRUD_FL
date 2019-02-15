# RacineCRUD_FL  
Version flask du projet RacineCRUD.  
## Usage  
Installez les dépendances enumérées dans `requirements.txt` et modifiez la config en fonction de votre environnement. Vous pouvez utilisé les `virtualenv` si vous le souhaitez.  
### Installation des dépendances
Placez vous dans le repertoire du projet saisissez un coup de :  
`pip install -r requirements.txt`  
Démarrez le serveur intégré avec `python app.py`  
### Configuration  
Par défaut c'est du `sqlite` qui est utilisé côté base de donnée avec le module `SQLAlchemy`.  
Libre à vous de modifier cette dernière si vous le souhaitez.  
### Note  
Le point d'entrée de l'application est le fichier `app.py`.  
Vous pouvez l'executer via la commande `./app.py` ou `python app.py`