# Documentation simple du projet Big Data ML End-to-End

Ce document explique le projet étape par étape, le rôle de chaque outil utilisé, et comment lancer la démonstration.

## 1. Objectif du projet

Le but du projet est de construire une chaîne complète Big Data + Machine Learning:

1. Générer des données de transactions.
2. Transformer ces données avec Spark.
3. Entraîner un modèle de deep learning avec PyTorch.
4. Suivre les expériences avec MLflow.
5. Servir le modèle via une API FastAPI.
6. Surveiller l’API avec Prometheus et Grafana.
7. Préparer l’infrastructure AWS avec Terraform.
8. Automatiser les tests et le déploiement avec GitHub Actions.
9. Lancer toute la démo localement avec Docker Compose.

## 2. Architecture globale

```text
Data Generator
      |
      v
Raw CSV Data
      |
      v
Spark ETL
      |
      v
Features Parquet
      |
      v
PyTorch Training
      |
      v
MLflow + Model Artifact
      |
      v
FastAPI Inference API
      |
      v
Prometheus + Grafana Monitoring
```

Sur AWS, Terraform prépare les ressources nécessaires comme S3, ECR, IAM et CloudWatch.

## 3. Structure du projet

```text
.
|-- data/
|   |-- generate_data.py
|-- spark/
|   |-- jobs/etl_features.py
|-- apps/
|   |-- training/train_model.py
|   |-- inference/api.py
|-- scripts/
|   |-- run_demo.py
|   |-- predict_example.ps1
|-- infra/
|   |-- terraform/
|-- monitoring/
|   |-- prometheus.yml
|   |-- grafana/
|-- tests/
|-- .github/workflows/ci-cd.yml
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
|-- Makefile
|-- README.md
```

## 4. Étapes du pipeline

### Étape 1: Génération des données

Fichier:

```text
data/generate_data.py
```

Ce script crée un fichier CSV avec des transactions fictives.

Chaque transaction contient par exemple:

- montant de la transaction
- heure de la transaction
- niveau de risque du marchand
- ancienneté du compte utilisateur
- risque du pays
- label `is_fraud`, qui indique si la transaction est frauduleuse ou non

Sortie générée:

```text
data/raw/transactions.csv
```

### Étape 2: Transformation Big Data avec Spark

Fichier:

```text
spark/jobs/etl_features.py
```

Spark lit les données CSV, puis prépare des variables utilisables par le modèle.

Exemples de transformations:

- transformation du montant avec `log1p`
- encodage de l’heure avec `sin` et `cos`
- création d’un score d’ancienneté du compte
- sélection des colonnes finales du modèle

Sortie générée:

```text
data/processed/features.parquet
```

Le format Parquet est utilisé parce qu’il est très courant dans les projets Big Data. Il est plus efficace que CSV pour les gros volumes.

### Étape 3: Entraînement Deep Learning

Fichier:

```text
apps/training/train_model.py
```

Le modèle est construit avec PyTorch.

Il s’agit d’un petit réseau de neurones qui prédit si une transaction est frauduleuse.

Le script fait:

- chargement des features Parquet
- séparation train/test
- normalisation des données
- entraînement du modèle
- calcul des métriques
- sauvegarde du modèle
- enregistrement dans MLflow

Métriques suivies:

- accuracy
- F1-score
- ROC AUC
- train loss

Modèle sauvegardé:

```text
models/fraud_net.pt
```

### Étape 4: Tracking avec MLflow

MLflow sert à suivre les expériences Machine Learning.

Il permet de sauvegarder:

- paramètres d’entraînement
- métriques
- modèle entraîné
- historique des runs

Dans la démo locale, MLflow est disponible ici:

```text
http://localhost:5000
```

### Étape 5: API d’inférence avec FastAPI

Fichier:

```text
apps/inference/api.py
```

FastAPI expose le modèle entraîné sous forme d’API HTTP.

Endpoints principaux:

```text
GET /health
POST /predict
GET /metrics
```

Documentation interactive:

```text
http://localhost:8000/docs
```

Exemple de prédiction:

```powershell
./scripts/predict_example.ps1
```

### Étape 6: Monitoring avec Prometheus et Grafana

Prometheus collecte les métriques exposées par l’API.

Fichier:

```text
monitoring/prometheus.yml
```

Grafana affiche les métriques dans un dashboard.

Dashboard:

```text
monitoring/grafana/provisioning/dashboards/fraud-api.json
```

Services disponibles:

```text
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
```

Identifiants Grafana:

```text
admin / admin
```

## 5. Outils utilisés

## Git

Git est utilisé pour versionner le code.

Il permet de:

- suivre les modifications
- créer des branches
- revenir à une version précédente
- travailler en équipe

Commandes utiles:

```bash
git init
git add .
git commit -m "Initial project"
git branch -M main
```

## GitHub

GitHub permet d’héberger le dépôt Git en ligne.

Il sert aussi à:

- collaborer avec d’autres développeurs
- ouvrir des pull requests
- gérer les issues
- déclencher GitHub Actions

Exemple:

```bash
git remote add origin git@github.com:<org>/<repo>.git
git push -u origin main
```

## GitHub Actions

Fichier:

```text
.github/workflows/ci-cd.yml
```

GitHub Actions automatise la CI/CD.

Dans ce projet, le workflow fait:

- installation des dépendances Python
- lint avec Ruff
- tests avec Pytest
- build de l’image Docker
- validation Terraform
- push de l’image vers AWS ECR si configuré
- déploiement Terraform sur la branche `main`

## Docker

Fichier:

```text
Dockerfile
```

Docker permet de créer une image contenant l’application et ses dépendances.

Avantage:

- même environnement partout
- facile à lancer localement
- compatible avec CI/CD et cloud

Commande:

```bash
docker build -t bigdata-ml-platform:local .
```

## Docker Compose

Fichier:

```text
docker-compose.yml
```

Docker Compose lance plusieurs services ensemble.

Services du projet:

- MLflow
- Spark master
- pipeline de démo
- API FastAPI
- Prometheus
- Grafana

Commande:

```bash
docker compose up --build
```

## Apache Spark

Spark est un moteur Big Data utilisé pour traiter de gros volumes de données.

Dans ce projet, Spark sert à:

- lire les données brutes
- transformer les colonnes
- créer les features
- écrire le résultat en Parquet

Spark UI:

```text
http://localhost:8080
```

## PyTorch

PyTorch est utilisé pour créer et entraîner le modèle deep learning.

Dans ce projet, le modèle prédit la fraude à partir des features préparées par Spark.

## MLflow

MLflow est utilisé pour gérer le cycle de vie Machine Learning.

Il permet de:

- comparer plusieurs entraînements
- suivre les métriques
- sauvegarder les modèles
- retrouver les paramètres utilisés

## FastAPI

FastAPI sert à exposer le modèle sous forme d’API.

Avantages:

- rapide
- simple
- documentation Swagger automatique
- très utilisé pour les APIs Machine Learning

## Prometheus

Prometheus collecte les métriques de l’API.

Exemples de métriques:

- nombre de prédictions
- latence des prédictions
- disponibilité du service

## Grafana

Grafana affiche les métriques sous forme de graphiques.

Il permet de créer des dashboards pour surveiller l’application.

## Terraform

Dossier:

```text
infra/terraform/
```

Terraform permet de créer l’infrastructure cloud sous forme de code.

Dans ce projet, Terraform prépare:

- bucket S3 pour le data lake
- repository ECR pour les images Docker
- rôle IAM pour les pipelines
- log group CloudWatch

Commandes:

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

## AWS

AWS est la plateforme cloud cible.

Services AWS utilisés ou préparés:

- S3: stockage des données
- ECR: stockage des images Docker
- IAM: gestion des permissions
- CloudWatch: logs et monitoring cloud

## Pytest

Pytest sert à tester le code Python.

Commande:

```bash
pytest -q
```

## Ruff

Ruff sert à vérifier la qualité du code Python.

Commande:

```bash
ruff check .
```

## 6. Lancer la démo locale

Depuis la racine du projet:

```bash
docker compose up --build
```

Ensuite ouvrir:

```text
MLflow:     http://localhost:5000
API:        http://localhost:8000/docs
Spark UI:   http://localhost:8080
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
```

Pour tester l’API:

```powershell
./scripts/predict_example.ps1
```

## 7. Déploiement AWS

Avant le déploiement, configurer les credentials AWS.

Puis:

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

Pour GitHub Actions, configurer les secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ACCOUNT_ID
```

Et configurer la variable GitHub:

```text
ECR_REPOSITORY
```

Exemple:

```text
bigdata-ml-platform-dev
```

## 8. Résultat attendu

À la fin, le projet permet de démontrer une chaîne complète:

```text
Données -> Spark -> Deep Learning -> MLflow -> API -> Monitoring -> CI/CD -> AWS
```

C’est une base solide pour un projet académique, portfolio, PFE, ou démonstration professionnelle DevOps/Data/ML.

## 9. Améliorations possibles

Améliorations futures:

- ajouter Airflow pour orchestrer les jobs
- utiliser AWS Glue ou EMR pour Spark managé
- déployer l’API sur ECS Fargate
- ajouter un Model Registry MLflow
- ajouter des alertes Grafana
- ajouter des tests d’intégration Docker
- ajouter un backend Terraform S3 + DynamoDB
- ajouter un pipeline de réentraînement automatique

