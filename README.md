<center>

# Eureka

</center>

Eureka est une plateforme communautaire de partage de notes de cours, TD et autres ressources pour les étudiants en Informatique et Cybersécurité de l'INSA Hauts-de-France.  
Le site est disponible à l'adresse suivante : [eurekainsahdf.fr](https://eurekainsahdf.fr)  
Ce site est développé par le club informatique de l'INSA Hauts-de-France, `./insa.sh`
Il aura pour but de s'étendre à toutes les années ainsi que spécialités de l'INSA.

<br>

## Fonctionnalités

Le site est déjà en ligne et fonctionnel, cependant il est encore en développement.  
Voici les fonctionnalités déjà implémentées :
- Authentification administrateur sécurisée
- Dépôt, modification et suppression de ressources
- Consultation des ressources
- Vérification de la sécurité des ressources
- Système de recherche
- Mode sombre et mode jour
- Tri par spécialité et par année
- log des activités concernant le dépôt ou la modification de ressources
- des easter eggs ???

<br>

## Fonctionnalités en cours de développement

Un certain nombre de fonctionnalités ne sont pas encore implémentées, voici la liste :
- Système de vote pour les ressources
- Gestion de modérateurs
- inclusion d'autres spécialités

<br>

## Modules requis

- Flask==2.2.2
- mysql_connector_repackaged==0.3.1
- python-dotenv==1.0.0
- python_bcrypt==0.3.2

Un fichier `requirements.txt` est disponible à la racine du projet.

<br>

## Execution

Le projet nécessite une connexion à une base de données MySQL.

- host_db = "url de la base de données"
- user_db = "utilisateur de la base de données"
- password_db = "mot de passe de l'utilisateur"
- secret_key = "clé secrète pour Flask"
- virusTotalAPI = "la clé API de VirusTotal pour le scan des fichiers"

Le projet peut simplement être exécuté en utilisant la commande : 

`python3 app.py`
