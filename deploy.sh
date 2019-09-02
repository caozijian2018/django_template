git pull
sh docker-maker/depoy.sh
python3 src/manage.py migrate
docker-compose up -d
#sudo supervisorctl restart site-api
#sudo service nginx reload