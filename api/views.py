from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import JobSerializer
from .tasks import scrape_coin_data
import uuid

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins')

        # Check if 'coins' is None or empty
        if coins is None or not coins:
            return Response({'error': 'No coins provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if all elements in 'coins' are strings
        if not all(isinstance(coin, str) for coin in coins):
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        job_id = uuid.uuid4()
        job = Job.objects.create(job_id=job_id)
        for coin in coins:
            Task.objects.create(job=job, coin=coin)
            scrape_coin_data.delay(coin, str(job_id))

        return Response({'job_id': str(job_id)}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)
        return Response(serializer.data)
