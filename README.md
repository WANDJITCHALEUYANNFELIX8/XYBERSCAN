# XYBERSCAN
🛡️  (Phase 1 : MVP)

Rendre le numérique plus sûr pour les PME africaines. Un projet de la communauté Open Source Xyberclan.

<p align="center">
  <img src="assets/3.png" alt="XyberScan Logo" width="300"/>
</p>

*📖 Présentation du Projet*

La majorité des petites et moyennes entreprises en Afrique ne disposent pas des ressources pour auditer la sécurité de leurs sites web. XYBERSCAN est un outil gratuit, en français et adapté au contexte local, conçu pour combler ce manque.


L'objectif est de développer un scanner de vulnérabilités web en Python capable de générer des rapports compréhensibles pour aider les entreprises à se protéger.

🚀 Fonctionnalités du MVP (Phase 1)
Pour cette première phase, le scanner se concentre sur des analyses fondamentales sans authentification:


Vérification des Headers HTTP : Analyse des en-têtes de sécurité (CSP, HSTS, X-Frame-Options, etc.).



Audit SSL/TLS : Vérification de la validité du certificat et des protocoles utilisés.



Détection de Fichiers Sensibles : Recherche de fichiers exposés par erreur (ex: .env, .git, wp-config.php).



Scan de Ports : Vérification des ports réseau critiques ouverts sur le serveur (21, 22, 3306, etc.).



Rapport Terminal : Affichage d'un bilan synthétique et coloré avec des recommandations de correction.


🛠️ Installation & Utilisation

Note : Ce projet nécessite Python 3.10+.

Cloner le projet :

Bash

git clone https://github.com/CYBERCLAN237/XYBERSCAN.git

<br>cd xyberscan

Installer les dépendances :

Bash

pip install -r requirements.txt
Lancer un scan :

Bash

python scanner.py [URL_CIBLE]
🤝 Contribuer au projet
La communauté Xyberclan accueille tous les niveaux:


Développeurs Python (Bases de Python requises).


Testeurs QA (Aucun prérequis).


Rédacteurs techniques (Français requis).

Veuillez consulter le fichier CONTRIBUTING.md pour connaître les règles de contribution et le workflow GitHub.


⚖️ Éthique et Légalité
Ce scanner est développé à des fins éducatives et défensives.

Il est strictement interdit de scanner des sites sans autorisation explicite du propriétaire.

L'utilisation malveillante de cet outil est contraire aux valeurs de Xyberclan.

✨ Propulsé par xyberclan.dev
