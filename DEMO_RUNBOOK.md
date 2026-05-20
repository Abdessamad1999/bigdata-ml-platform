# Démo complète: run du premier projet de A à Z

Ce guide explique comment lancer le premier projet Big Data ML end-to-end dans le bon ordre: environnement Python, tests, Docker, MLflow, API, monitoring, GitHub Actions et déploiement AWS avec Terraform.

Projet concerné:

```text
cr-e-projet-end-to-end
```

## 0. Prérequis

Installer:

- Git
- Python 3.11
- Docker Desktop
- Docker Compose
- Terraform
- AWS CLI
- un compte AWS
- un repository GitHub

Vérifier les outils:

```bash
git --version
python --version
docker --version
docker compose version
terraform version
aws --version
```

Important: utiliser Python 3.11. Éviter Python 3.14 pour ce projet, car certaines librairies Big Data/ML peuvent ne pas encore avoir de packages compatibles.

## 1. Se placer dans le projet

Sous Windows PowerShell:

```powershell
cd "C:\Users\Abdessamad Benammou\Documents\Codex\2026-05-19\cr-e-projet-end-to-end"
```

Sous Linux / macOS:

```bash
cd cr-e-projet-end-to-end
```

## 2. Créer l’environnement virtuel Python

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloque l’activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis relancer:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Vérifier le projet localement

Lancer les tests:

```bash
pytest -q
```

Lancer le lint:

```bash
ruff check .
```

Ces commandes vérifient que le code Python est correct avant de lancer Docker.

## 4. Lancer la démo locale complète

Depuis la racine du projet:

```bash
docker compose up --build
```

Cette commande démarre:

- MLflow
- Spark master
- pipeline de démo
- API FastAPI
- Prometheus
- Grafana

Le conteneur `pipeline-demo` exécute automatiquement:

1. génération des données
2. transformation Spark
3. entraînement PyTorch
4. tracking MLflow
5. sauvegarde du modèle

## 5. Vérifier les services locaux

Ouvrir:

```text
MLflow:     http://localhost:5000
API:        http://localhost:8000/docs
Spark UI:   http://localhost:8080
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
```

Identifiants Grafana:

```text
admin / admin
```

## 6. Tester l’API d’inférence

Avec PowerShell:

```powershell
./scripts/predict_example.ps1
```

Ou avec curl:

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

Résultat attendu:

```json
{
  "fraud_probability": 0.72,
  "is_fraud": true
}
```

La valeur exacte peut changer selon l’entraînement.

## 7. Vérifier MLflow

Ouvrir:

```text
http://localhost:5000
```

Vérifier:

- expérience `fraud-deep-learning-demo`
- métriques du modèle
- paramètres d’entraînement
- artifacts du modèle

Métriques disponibles:

- accuracy
- F1-score
- ROC AUC
- train loss

## 8. Vérifier Spark

Ouvrir:

```text
http://localhost:8080
```

Spark UI permet de voir:

- le job de feature engineering
- les étapes du traitement
- les workers
- les logs d’exécution

## 9. Vérifier Prometheus

Ouvrir:

```text
http://localhost:9090
```

Tester:

```promql
up{job="fraud-api"}
```

```promql
rate(fraud_predictions_total[1m])
```

```promql
histogram_quantile(0.95, rate(fraud_prediction_latency_seconds_bucket[5m]))
```

Si `up{job="fraud-api"}` retourne `1`, Prometheus collecte bien les métriques de l’API.

## 10. Vérifier Grafana

Ouvrir:

```text
http://localhost:3000
```

Connexion:

```text
admin / admin
```

Aller dans les dashboards provisionnés.

Dashboard principal:

```text
Fraud API Monitoring
```

Il affiche:

- le débit des prédictions
- la latence p95 de l’API

## 11. Arrêter la stack locale

Arrêter les conteneurs:

```bash
docker compose down
```

Arrêter et supprimer les volumes:

```bash
docker compose down -v
```

Nettoyer les images inutilisées:

```bash
docker image prune
```

## 12. Initialiser Git

Si le projet n’est pas encore versionné:

```bash
git init
git add .
git commit -m "Initial end-to-end big data ML platform"
git branch -M main
```

Créer un repository GitHub, puis:

```bash
git remote add origin git@github.com:<org>/<repo>.git
git push -u origin main
```

Remplacer:

```text
<org>/<repo>
```

par le nom réel du repository.

## 13. Configurer AWS CLI

Lancer:

```bash
aws configure
```

Renseigner:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name
Default output format
```

Exemple région:

```text
eu-west-1
```

Vérifier:

```bash
aws sts get-caller-identity
```

Si la commande retourne un `Account`, un `UserId` et un `Arn`, AWS CLI est bien configuré.

## 14. Déployer l’infrastructure AWS avec Terraform

Aller dans le dossier Terraform:

```bash
cd infra/terraform
```

Initialiser Terraform:

```bash
terraform init
```

Vérifier le format:

```bash
terraform fmt -recursive
```

Valider la configuration:

```bash
terraform validate
```

Voir le plan:

```bash
terraform plan \
  -var="project_name=bigdata-ml-platform" \
  -var="environment=dev" \
  -var="aws_region=eu-west-1"
```

Déployer:

```bash
terraform apply \
  -var="project_name=bigdata-ml-platform" \
  -var="environment=dev" \
  -var="aws_region=eu-west-1"
```

Valider avec:

```text
yes
```

Terraform crée:

- bucket S3 pour le data lake
- repository ECR pour les images Docker
- rôle IAM pour les workloads
- policy IAM
- log group CloudWatch

Afficher les outputs:

```bash
terraform output
```

## 15. Builder et pousser l’image Docker vers AWS ECR

Récupérer l’URL du repository ECR:

```bash
terraform output ecr_repository_url
```

Revenir à la racine du projet:

```bash
cd ../..
```

Se connecter à ECR:

```bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com
```

Remplacer:

```text
ACCOUNT_ID
```

par votre identifiant de compte AWS.

Builder l’image:

```bash
docker build -t bigdata-ml-platform .
```

Tagger l’image:

```bash
docker tag bigdata-ml-platform:latest ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/bigdata-ml-platform-dev:latest
```

Pousser l’image:

```bash
docker push ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/bigdata-ml-platform-dev:latest
```

## 16. Configurer GitHub Actions

Dans GitHub:

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

Le workflow GitHub Actions est ici:

```text
.github/workflows/ci-cd.yml
```

Il exécute:

- installation des dépendances
- lint avec Ruff
- tests avec Pytest
- build Docker
- push Docker vers ECR sur `main`
- validation Terraform
- Terraform apply sur `main`

## 17. Déclencher la CI/CD

Faire une modification, puis:

```bash
git add .
git commit -m "Update project"
git push
```

Sur GitHub, aller dans:

```text
Actions -> CI/CD
```

Vérifier que les jobs passent:

- `test`
- `docker`
- `terraform`

## 18. Monitoring local

Le monitoring local utilise:

- API FastAPI
- Prometheus
- Grafana

Flux:

```text
FastAPI /metrics -> Prometheus -> Grafana
```

Fichiers importants:

```text
monitoring/prometheus.yml
monitoring/grafana/provisioning/datasources/prometheus.yml
monitoring/grafana/provisioning/dashboards/fraud-api.json
```

## 19. Monitoring AWS

Terraform crée un log group CloudWatch:

```text
/aws/bigdata-ml-platform-dev/pipeline
```

Dans AWS Console:

1. Aller dans CloudWatch.
2. Ouvrir Log groups.
3. Chercher le log group du projet.
4. Vérifier les logs des workloads/pipelines.

Dans cette première version, le monitoring applicatif complet est local avec Prometheus/Grafana. CloudWatch est préparé pour les logs côté AWS.

## 20. Nettoyer AWS

Pour supprimer l’infrastructure AWS:

```bash
cd infra/terraform
terraform destroy \
  -var="project_name=bigdata-ml-platform" \
  -var="environment=dev" \
  -var="aws_region=eu-west-1"
```

Valider avec:

```text
yes
```

Attention: cela supprime les ressources créées par Terraform.

## 21. Ordre résumé

Ordre correct:

```text
1. Installer les prérequis
2. Créer le venv Python 3.11
3. Installer requirements.txt
4. Lancer tests + lint
5. Lancer Docker Compose
6. Vérifier MLflow
7. Vérifier Spark UI
8. Vérifier API FastAPI
9. Tester /predict
10. Vérifier Prometheus
11. Vérifier Grafana
12. Initialiser Git
13. Pousser sur GitHub
14. Configurer AWS CLI
15. Déployer Terraform
16. Builder et pousser l’image Docker vers ECR
17. Configurer GitHub Actions
18. Vérifier CI/CD
19. Vérifier CloudWatch
20. Nettoyer si nécessaire
```

## 22. Commandes rapides

Local:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
ruff check .
docker compose up --build
```

Terraform:

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

Docker ECR:

```bash
docker build -t bigdata-ml-platform .
docker tag bigdata-ml-platform:latest ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/bigdata-ml-platform-dev:latest
docker push ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/bigdata-ml-platform-dev:latest
```

Arrêt local:

```bash
docker compose down -v
```

