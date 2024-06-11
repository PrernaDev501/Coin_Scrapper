## Overview
This project scrapes cryptocurrency data from CoinMarketCap using Django Rest Framework, Celery, and Selenium.

## API Endpoints
- `/api/taskmanager/start_scraping` [POST] - Starts a scraping job.
- `/api/taskmanager/scraping_status/<job_id>` [GET] - Checks the status of a scraping job.

## Setup
- Install dependencies: `pip install -r requirements.txt`
- Run Redis server: `redis-server`
- Run Celery worker: `celery -A crypto_scraper worker -l info`
- Run Django server: `python manage.py runserver`

  
