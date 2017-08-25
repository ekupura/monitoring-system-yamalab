echo "$(date): executed script" >> /var/log/cron.log 2>&1
python3 /send-metrics.py

