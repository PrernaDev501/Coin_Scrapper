from django.urls import path
from .views import StartScrapingView, ScrapingStatusView
from api import views

urlpatterns = [

    path('taskmanager/start_scraping', StartScrapingView.as_view()),
    path('taskmanager/scraping_status/<uuid:job_id>', ScrapingStatusView.as_view()),
]
