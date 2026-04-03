#!/bin/bash
# Deploy manuel vers Cloud Run (sans Cloud Build CI/CD)
# Usage: ./deploy.sh [PROJECT_ID] [REGION]

PROJECT_ID=${1:-$(gcloud config get-value project)}
REGION=${2:-europe-west1}
IMAGE="gcr.io/$PROJECT_ID/meetwater-api:latest"

echo "Deploy vers Cloud Run..."
echo "  Project : $PROJECT_ID"
echo "  Region  : $REGION"
echo "  Image   : $IMAGE"

docker build -t "$IMAGE" . && \
docker push "$IMAGE" && \
gcloud run deploy meetwater-api \
  --image="$IMAGE" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars="ALLOWED_ORIGINS=https://meetwater.fr,https://www.meetwater.fr" \
  --update-secrets="DATABASE_HOSTNAME=DATABASE_HOSTNAME:latest,DATABASE_PORT=DATABASE_PORT:latest,DATABASE_PASSWORD=DATABASE_PASSWORD:latest,DATABASE_NAME=DATABASE_NAME:latest,DATABASE_USERNAME=DATABASE_USERNAME:latest,SECRET_KEY=SECRET_KEY:latest,ALGORYTHM=ALGORYTHM:latest,ACCESS_TOKEN_EXPIRE_MINUTES=ACCESS_TOKEN_EXPIRE_MINUTES:latest,FROM_EMAIL=FROM_EMAIL:latest,SMTP_HOST=SMTP_HOST:latest,SMTP_PORT=SMTP_PORT:latest,SMTP_USER=SMTP_USER:latest,SMTP_PASSWORD=SMTP_PASSWORD:latest,FRONTEND_BASE_URL=FRONTEND_BASE_URL:latest" \
  --project="$PROJECT_ID"

echo "Done."
