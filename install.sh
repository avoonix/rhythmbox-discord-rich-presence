pip install --user pypresence 

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
sudo tee /etc/systemd/user/discord-rich-presence.service <<EOF
[Unit]
Description=Discord Rich Presence
StartLimitIntervalSec=0
Wants=dbus.socket

[Service]
Type=simple
Restart=always
RestartSec=1
ExecStart=/usr/bin/env python $DIR/main.py

[Install]
WantedBy=default.target
EOF

loginctl enable-linger $USER
systemctl enable --user discord-rich-presence.service
systemctl start --user discord-rich-presence.service
