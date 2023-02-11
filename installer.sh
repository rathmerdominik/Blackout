#!/bin/bash
USER="root"
GROUP="root"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ "$1" == "uninstall" ]
	then 
	sudo systemctl disable --now blackout.timer
	# I will not use globbing here because if the user has anything else
	sudo rm /etc/systemd/system/blackout.*

	sudo systemctl daemon-reload

	rm -rf /opt/blackout

	echo "Successfully uninstalled!"

	exit 0
fi

python -m venv venv

./venv/bin/pip install -r requirements.txt

mkdir /opt/blackout
cp -r ./* /opt/blackout 
chown -R $USER:$GROUP /opt/blackout

cat << EOF > /etc/systemd/system/blackout.timer
[Unit]
Description=Scheduled blackout timer

[Timer]
OnCalendar=*:0/5
Persistent=true

[Install]
WantedBy=timers.target

EOF

cat << EOF > /etc/systemd/system/blackout.service
[Unit]
Description=An automatic youtube music downloader

[Service]
TimeoutStartSec=600
Type=oneshot
ExecStart=/opt/blackout/venv/bin/python /opt/blackout/blackout.py
User=$USER
Group=$GROUP

EOF

systemctl daemon-reload
systemctl enable --now blackout.timer

echo "Everything ready!"