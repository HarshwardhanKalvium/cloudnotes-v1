# CloudNotes deployment

This deployment uses Ubuntu, PostgreSQL, gunicorn, and systemd. The commands below
are intended to be run from the project directory on the Linux server.

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv postgresql postgresql-contrib ufw
sudo -u postgres createuser --pwprompt cloudnotes
sudo -u postgres createdb --owner=cloudnotes cloudnotes
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
sudo cp .env.example /etc/cloudnotes/cloudnotes.env
sudo chmod 600 /etc/cloudnotes/cloudnotes.env
sudo ufw allow 5000/tcp
sudo cp deploy/cloudnotes.service /etc/systemd/system/cloudnotes.service
sudo systemctl daemon-reload
sudo systemctl enable --now cloudnotes
```

Set the real `DATABASE_URL`, `SECRET_KEY`, and `UPLOAD_FOLDER` in
`/etc/cloudnotes/cloudnotes.env`. Do not commit that file.

The service runs exactly:

```text
gunicorn --bind 0.0.0.0:5000 app:app
```

Check the deployment and managed-service behaviors:

```bash
curl http://SERVER_IP:5000/
sudo systemctl status cloudnotes
sudo systemctl kill --kill-who=main cloudnotes
sleep 6
sudo systemctl is-active cloudnotes
sudo reboot
# After reconnecting:
sudo systemctl is-enabled cloudnotes
curl http://SERVER_IP:5000/
```

`Restart=always` makes systemd start a replacement after a crash. Enabling the
unit for `multi-user.target` starts it automatically after boot.

Request path:

```text
your browser -> host / VM network -> OS firewall / open port
-> Linux server -> Flask on 0.0.0.0:5000
```

For a VM, use its bridged IP or forward host port 5000 to guest port 5000.
