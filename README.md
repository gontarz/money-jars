# DRF based simple wallet-like api

use to keep data about cash amount and currencies, deposit, withdraw and transfer cash inside app

### installation:
download or clone 
- using docker: run docker
```buildoutcfg
docker-compose up
docker-compose run web python manage.py createsuperuser
```


- install manually: install requirements from requirements.txt add database configuration or provide local_settings.py
```buildoutcfg
pip install -r requirements.txt
```
visit http://0.0.0.0:8000/admin/
