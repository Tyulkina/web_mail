sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf /home/ekaterina/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart
sudo gunicorn -c /home/ekaterina/box/web/etc/gunicorn_django.conf ask.wsgi:application 
#sudo gunicorn -c /home/ekaterina/box/web/etc/gunicorn.conf hello:application 



