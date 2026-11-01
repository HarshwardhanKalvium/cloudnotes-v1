#!/usr/bin/env bash
set -euo pipefail

APP_DIR=/opt/cloudnotes

sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip postgresql postgresql-contrib ufw
sudo useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin cloudnotes || true
sudo mkdir -p "$APP_DIR" /etc/cloudnotes
sudo cp -R ./* "$APP_DIR/"
sudo python3 -m venv "$APP_DIR/.venv"
sudo "$APP_DIR/.venv/bin/pip" install --upgrade pip
sudo "$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"
sudo chown -R cloudnotes:cloudnotes "$APP_DIR"

sudo -u postgres psql <<'SQL'
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'cloudnotes') THEN
        CREATE ROLE cloudnotes LOGIN PASSWORD 'change-me';
    END IF;
END
$$;
SELECT 'CREATE DATABASE cloudnotes OWNER cloudnotes'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cloudnotes')\gexec
SQL

echo "Create /etc/cloudnotes/cloudnotes.env from .env.example with production values."
sudo cp "$APP_DIR/deploy/cloudnotes.service" /etc/systemd/system/cloudnotes.service
sudo ufw allow 5000/tcp
sudo systemctl daemon-reload
sudo systemctl enable --now cloudnotes
