from celery import shared_task
import requests
from bs4 import BeautifulSoup
from .models import Task

@shared_task
def scrape_coin_data(coin, job_id):
    url = f'https://coinmarketcap.com/currencies/{coin.lower()}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the necessary data using BeautifulSoup
        # For example, scraping the price:
        price_element = soup.find('div', class_='priceValue')
        if price_element:
            price = price_element.text
        else:
            price = 'Price not available'
        # Continue extracting other required data

        try:
            task = Task.objects.get(job__job_id=job_id, coin=coin)
            task.output = {
                'price': price,
                # Add other scraped data here
            }
            task.status = 'completed'
            task.save()
        except Task.DoesNotExist:
            pass  # Handle Task.DoesNotExist exception if needed
    else:
        try:
            task = Task.objects.get(job__job_id=job_id, coin=coin)
            task.status = 'failed'
            task.output = {}
            task.save()
        except Task.DoesNotExist:
            pass  # Handle Task.DoesNotExist exception if needed
