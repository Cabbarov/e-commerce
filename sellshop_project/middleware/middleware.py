import sys

from django.conf import settings as _settings
from loguru import logger

from sellshop_project.settings import Settings



settings = Settings(_settings)
logger.remove(0)
logger.add(sys.stderr, colorize=True, format=settings.MESSAGE_FORMAT)

class DjangoLoggingMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request URL: {request.get_raw_uri()}")
        logger.info(f"Request METHOD: {request.method}")
        logger.info(f"Request GET data: {request.GET}")
        logger.info(f"Request POST data: {request.POST}")
        logger.info(f"Request FILES data: {request.FILES}")
        file = open('session.log', 'a')
        file.write(f"Request: {request.method}\n {request.get_raw_uri()}\n {request.GET}\n {request.POST}\n {request.FILES}\n ")
        file.close()

        response = self.get_response(request)
        logger.info(f"Request USER: {request.user}")
        logger.info(f"Response STATUS_CODE: {response.status_code}")    
        file1 = open('session.log', 'a')
        file1.write(f"Request USER: {request.user}\n Response STATUS_CODE: {response.status_code}\n")

        return response

    