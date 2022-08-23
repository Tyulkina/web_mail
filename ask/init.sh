sudo /etc/init.d/mysql start
mysql -uroot -e "create database Flow;"     
mysql -uroot -e "CREATE USER 'db_owner'@'localhost' IDENTIFIED BY 'SayHi_k20';"
mysql -uroot -e "GRANT ALL ON Flow.* TO 'db_owner'@'localhost';"
python3 manage.py makemigrations qa
python3 manage.py migrate
mysql -uroot -e "insert into auth_user (password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) values ('SayHi_k20',sysdate(),1,'test_user','Тест','Тестов','test@mail.ru',1,1,sysdate())"
sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart
sudo gunicorn -c /home/box/web/etc/gunicorn_django.conf ask.wsgi:application




