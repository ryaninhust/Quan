serve:
	gunicorn -k egg:gunicorn#tornado app:app -b 0.0.0.0:8000

daemon_serve:
	gunicorn -D -k egg:gunicorn#tornado app:app -b 0.0.0.0:8000

stop:
	pkill gunicorn

test: 
	python tools/test_db.py;make test_data; pytest tests/tests.py; make resetdb

db:
	mysql -uroot simi

initdb:
	echo "create database simi;" | mysql -uroot

clrdb:
	echo "drop database if exists simi;" | mysql -uroot

resetdb: clrdb initdb

test_data:
	make db < tests/test.sql

dump_db:
	mysqldump -uroot simi
