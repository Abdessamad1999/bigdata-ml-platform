# Commandes expliquées du projet

Ce fichier regroupe les commandes importantes du premier projet `bigdata-ml-platform`, avec une explication simple pour chaque commande.

## 1. Aller dans le dossier du projet

### Windows PowerShell

```powershell
cd "C:\Users\Abdessamad Benammou\Documents\Codex\2026-05-19\bigdata-ml-platform"
```

Cette commande place le terminal dans le dossier du projet.

### Linux / macOS

```bash
cd bigdata-ml-platform
```

Cette commande fait la même chose sous Linux ou macOS.

## 2. Créer un environnement virtuel Python

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
```

Cette commande crée un environnement virtuel Python 3.11 dans le dossier `.venv`.

```powershell
.\.venv\Scripts\Activate.ps1
```

Cette commande active l’environnement virtuel.

### Linux / macOS

```bash
python3.11 -m venv .venv
```

Cette commande crée l’environnement virtuel.

```bash
source .venv/bin/activate
```

Cette commande active l’environnement virtuel.

## 3. Mettre à jour pip

```bash
python -m pip install --upgrade pip
```

Cette commande met à jour `pip`, l’outil utilisé pour installer les librairies Python.

## 4. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

Cette commande installe toutes les librairies listées dans `requirements.txt`, comme Spark, MLflow, PyTorch, FastAPI, Pytest et Ruff.

## 5. Lancer les tests unitaires

```bash
pytest -q
```

Cette commande lance les tests du projet. L’option `-q` signifie `quiet`, donc l’affichage est plus court.

## 6. Vérifier la qualité du code

```bash
ruff check .
```

Cette commande analyse le code Python et détecte les erreurs de style, imports inutiles ou problèmes simples.

## 7. Générer les données manuellement

```bash
python data/generate_data.py
```

Cette commande génère un fichier CSV de transactions fictives.

Résultat:

```text
data/raw/transactions.csv
```

## 8. Lancer le job Spark manuellement

```bash
python spark/jobs/etl_features.py --input data/raw/transactions.csv --output data/processed/features.parquet
```

Cette commande lance le traitement Spark.

Elle lit:

```text
data/raw/transactions.csv
```

Puis elle écrit les features dans:

```text
data/processed/features.parquet
```

## 9. Entraîner le modèle manuellement

```bash
python apps/training/train_model.py --features data/processed/features.parquet --model-dir models --epochs 8
```

Cette commande entraîne le modèle deep learning avec PyTorch.

Elle utilise les features Parquet et sauvegarde le modèle dans:

```text
models/fraud_net.pt
```

## 10. Lancer tout le pipeline Python

```bash
python scripts/run_demo.py
```

Cette commande exécute le pipeline complet:

1. génération des données
2. transformation Spark
3. entraînement du modèle
4. tracking MLflow
5. sauvegarde du modèle

## 11. Construire l’image Docker

```bash
docker build -t bigdata-ml-platform:local .
```

Cette commande construit une image Docker locale du projet.

Nom de l’image:

```text
bigdata-ml-platform:local
```

## 12. Lancer la démo complète avec Docker Compose

```bash
docker compose up --build
```

Cette commande construit les images Docker puis démarre tous les services:

- MLflow
- Spark master
- pipeline demo
- API FastAPI
- Prometheus
- Grafana

## 13. Lancer Docker Compose en arrière-plan

```bash
docker compose up --build -d
```

Cette commande lance les services en arrière-plan. Le terminal reste disponible.

## 14. Voir les conteneurs actifs

```bash
docker compose ps
```

Cette commande affiche les services Docker Compose en cours d’exécution.

## 15. Voir les logs Docker

```bash
docker compose logs
```

Cette commande affiche les logs de tous les services.

Pour suivre les logs en temps réel:

```bash
docker compose logs -f
```

## 16. Arrêter les services Docker

```bash
docker compose down
```

Cette commande arrête et supprime les conteneurs Docker Compose.

## 17. Arrêter les services et supprimer les volumes

```bash
docker compose down -v
```

Cette commande arrête les conteneurs et supprime aussi les volumes Docker.

Elle est utile pour repartir de zéro.

## 18. Tester l’API avec PowerShell

```powershell
./scripts/predict_example.ps1
```

Cette commande envoie une transaction exemple à l’API `/predict`.

## 19. Tester l’API avec curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "amount_log": 5.3,
    "hour_sin": -0.7,
    "hour_cos": 0.2,
    "merchant_risk": 0.82,
    "account_age_score": 1.0,
    "country_risk": 0.65
  }'
```

Cette commande appelle l’API FastAPI pour obtenir une prédiction de fraude.

## 20. Vérifier la santé de l’API

```bash
curl http://localhost:8000/health
```

Cette commande vérifie si l’API est disponible.

Résultat attendu:

```json
{
  "status": "ok",
  "model_loaded": "true"
}
```

## 21. Ouvrir les interfaces locales

### MLflow

```text
http://localhost:5000
```

Interface pour voir les expériences, métriques et modèles.

### API FastAPI

```text
http://localhost:8000/docs
```

Documentation interactive de l’API.

### Spark UI

```text
http://localhost:8080
```

Interface pour suivre les jobs Spark.

### Prometheus

```text
http://localhost:9090
```

Interface pour interroger les métriques.

### Grafana

```text
http://localhost:3000
```

Interface dashboards.

Identifiants:

```text
admin / admin
```

## 22. Requêtes Prometheus utiles

```promql
up{job="fraud-api"}
```

Cette requête vérifie si Prometheus arrive à joindre l’API.

```promql
rate(fraud_predictions_total[1m])
```

Cette requête affiche le nombre de prédictions par seconde.

```promql
histogram_quantile(0.95, rate(fraud_prediction_latency_seconds_bucket[5m]))
```

Cette requête affiche la latence p95 des prédictions.

## 23. Initialiser Git

```bash
git init
```

Cette commande initialise un dépôt Git local.

```bash
git add .
```

Cette commande ajoute tous les fichiers au prochain commit.

```bash
git commit -m "Initial end-to-end big data ML platform"
```

Cette commande crée un commit avec le code actuel.

```bash
git branch -M main
```

Cette commande renomme la branche principale en `main`.

## 24. Connecter le projet à GitHub

```bash
git remote add origin git@github.com:<org>/<repo>.git
```

Cette commande connecte le dépôt local au repository GitHub.

Remplacer:

```text
<org>/<repo>
```

par votre organisation et nom de repository.

```bash
git push -u origin main
```

Cette commande pousse le code vers GitHub.

## 25. Configurer AWS CLI

```bash
aws configure
```

Cette commande configure AWS CLI.

Elle demande:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name
Default output format
```

Vérifier la connexion AWS:

```bash
aws sts get-caller-identity
```

Cette commande affiche l’identité AWS utilisée.

## 26. Initialiser Terraform

```bash
cd infra/terraform
```

Cette commande place le terminal dans le dossier Terraform.

```bash
terraform init
```

Cette commande initialise Terraform et télécharge le provider AWS.

## 27. Formater Terraform

```bash
terraform fmt -recursive
```

Cette commande formate les fichiers Terraform.

## 28. Valider Terraform

```bash
terraform validate
```

Cette commande vérifie que la configuration Terraform est correcte.

## 29. Voir le plan Terraform

```bash
terraform plan \
  -var="project_name=bigdata-ml-platform" \
  -var="environment=dev" \
  -var="aws_region=eu-west-1"
```

Cette commande montre les ressources AWS qui seront créées.

## 30. Déployer avec Terraform

```bash
terraform apply \
  -var="project_name=bigdata-ml-platform" \
  -var="environment=dev" \
  -var="aws_region=eu-west-1"
```

Cette commande crée les ressources AWS:

- S3
- ECR
- IAM
- CloudWatch logs

## 31. Voir les outputs Terraform

```bash
terraform output
```

Cette commande affiche les valeurs importantes créées par Terraform, comme le bucket S3 et l’URL ECR.

## 32. Se connecter à AWS ECR

```bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com
```

Cette commande connecte Docker au registre AWS ECR.

Remplacer:

```text
ACCOUNT_ID
```

par l’identifiant du compte AWS.

## 33. Tagger l’image Docker pour ECR

```bash
docker tag bigdata-ml-platform:local ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/bigdata-ml-platform-dev:latest
```

Cette commande prépare l’image Docker pour être poussée vers ECR.

## 34. Pousser l’image vers ECR

```bash
docker push ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/bigdata-ml-platform-dev:latest
```

Cette commande envoie l’image Docker dans AWS ECR.

## 35. Configurer GitHub Actions

Dans GitHub, aller dans:

```text
Repository -> Settings -> Secrets and variables -> Actions
```

Ajouter les secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ACCOUNT_ID
```

Ajouter la variable:

```text
ECR_REPOSITORY
```

Exemple:

```text
bigdata-ml-platform-dev
```

## 36. Déclencher la CI/CD

```bash
git add .
git commit -m "Update project"
git push
```

Ces commandes envoient une modification vers GitHub et déclenchent le workflow GitHub Actions.

## 37. Supprimer l’infrastructure AWS

```bash
cd infra/terraform
```

Cette commande retourne dans le dossier Terraform.

```bash
terraform destroy \
  -var="project_name=bigdata-ml-platform" \
  -var="environment=dev" \
  -var="aws_region=eu-west-1"
```

Cette commande supprime les ressources AWS créées par Terraform.

Attention: elle supprime réellement les ressources cloud.

## 38. Résumé des commandes principales

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
ruff check .
docker compose up --build
docker compose down -v
cd infra/terraform
terraform init
terraform plan
terraform apply
terraform output
terraform destroy
```

Ces commandes couvrent le cycle principal: installation, test, démo locale, déploiement AWS et nettoyage.

