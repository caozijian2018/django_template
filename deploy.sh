cd /home/emu/emu_master

git pull

source /home/emu/emu_master/venv/bin/activate
pip3 install -r requirements.txt
python src/manage.py collectstatic --noinput --settings=settings.prod
python src/manage.py migrate --settings=settings.prod

#sudo supervisorctl restart site-api
#sudo service nginx reload