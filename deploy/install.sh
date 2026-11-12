#!/usr/bin/env bash
# One-time install of prepmitra.influencioweb.com on the shared server (run as root).
# Expects the release uploaded to /tmp/prepmitra.tgz (backend, deploy, docs/question-bank) and /tmp/web.tgz (frontend/dist).
# Everything lives in its own places: /opt/prepmitra, /var/www/prepmitra, compose project "prepmitra",
# API on 127.0.0.1:8110 and one new nginx site file. No other site's config or containers are touched.
set -euo pipefail

DOMAIN=prepmitra.influencioweb.com
APP=/opt/prepmitra
WEB=/var/www/prepmitra
COMPOSE="docker compose -f $APP/deploy/docker-compose.prod.yml"

# 1. Code and web build
mkdir -p "$APP" "$WEB"
tar -xzf /tmp/prepmitra.tgz -C "$APP"
tar -xzf /tmp/web.tgz -C "$WEB"
mkdir -p "$APP/backend/secrets" && chmod 700 "$APP/backend/secrets"

# 2. Config, generated here and kept only on the server (skipped if it already exists)
umask 077
[ -f "$APP/deploy/.env" ] || printf 'POSTGRES_PASSWORD=%s\n' "$(openssl rand -hex 24)" > "$APP/deploy/.env"
if [ ! -f "$APP/backend/.env" ]; then
  cat > "$APP/backend/.env" <<EOF
APP_NAME=PrepMitra AI
APP_ENV=production
CORS_ORIGINS=https://$DOMAIN
PUBLIC_BASE_URL=https://$DOMAIN
WEB_BASE_URL=https://$DOMAIN
JWT_SECRET=$(openssl rand -base64 48 | tr -d '\n')
ACCESS_TOKEN_MINUTES=15
REFRESH_TOKEN_DAYS=30
BOOTSTRAP_ADMIN_PHONE=
FIREBASE_PROJECT_ID=ai-preaparation
GOOGLE_CLIENT_ID=
AI_PROVIDER=mock
ANTHROPIC_API_KEY=
AI_MODEL_STRONG=claude-opus-5-5
AI_MODEL_FAST=claude-haiku-5-5
SPEECH_PROVIDER=mock
EMAIL_PROVIDER=console
PUSH_PROVIDER=console
FCM_CREDENTIALS_FILE=
PAYMENT_GATEWAY=mock
RATE_LIMITS_ENABLED=true
STORAGE_DIR=storage
FONTS_DIR=fonts
EOF
fi
umask 022

# 3. Database, migrations + seed, API and worker
$COMPOSE up -d --build

# 4. Question bank (draft: stored but not served until approved)
$COMPOSE run --rm -v "$APP/docs/question-bank:/bank:ro" api python -m app.services.bank_import --bank /bank

# 5. nginx site + HTTPS
cp "$APP/deploy/nginx-$DOMAIN.conf" "/etc/nginx/sites-available/$DOMAIN"
ln -sf "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
nginx -t
systemctl reload nginx
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --redirect --register-unsafely-without-email

rm -f /tmp/prepmitra.tgz /tmp/web.tgz
curl -fsS "https://$DOMAIN/v1/health" && echo && echo "PrepMitra is live at https://$DOMAIN"
