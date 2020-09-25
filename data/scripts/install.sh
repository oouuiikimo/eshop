unlink /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Taipei /etc/localtime
apt-get update #&& apt-get install -y nginx \
apt-get install -y cron && apt-get install -y rsyslog
pip3 install -r /home/user/data/scripts/requirements.txt
pip3 install --upgrade pip
#cp /home/user/data/scripts/nginx_server.conf /etc/nginx/sites-available/default
#service nginx restart
service cron start
service rsyslog start
supervisord -c "/home/user/data/scripts/supervisord.conf"



