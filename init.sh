#sudo rm -rf /etc/nginx/sites-enabled/default
#sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/
#sudo /etc/init.d/nginx restart
#sudo gunicorn -c /home/box/web/etc/gunicorn_django.conf ask.ask.wsgi:application
#sudo gunicorn -c /home/box/web/etc/gunicorn.conf hello:application
sudo /etc/init.d/mysql start
mysql -uroot -e "create database Flow;"     
mysql -uroot -e "CREATE USER 'db_owner'@'localhost' IDENTIFIED BY 'SayHi_k20';"
mysql -uroot -e "GRANT ALL ON Flow.* TO 'db_owner'@'localhost';"
git clone https://github.com/Tyulkina/web_mail.git /hone/box/web
cd web/ask/
python3 manage.py makemigrations qa
python3 manage.py migrate
 


