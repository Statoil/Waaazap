from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from models import HappynessRegistration, HappynessStatus
from serializers import HappynessRegistrationSerializer, HappynessStatusSerializer
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class HappynessRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows HappynessRegistrations to be viewed or edited.
    """
    logger = logging.getLogger('testlogger')
    logger.info("Accessing HappynessRegistration API endpoint (view)")
    queryset = HappynessRegistration.objects.all()
    serializer_class = HappynessRegistrationSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def happyness_status(request):
    if request.method == 'GET':
        #TODO: Get the real numbers from db/model
        sad_number = HappynessRegistration.objects.filter(mood='sad').count()
        flat_number = HappynessRegistration.objects.filter(mood='flat').count()
        good_number = HappynessRegistration.objects.filter(mood='good').count()
        happy_number = HappynessRegistration.objects.filter(mood='happy').count()
        happyness_status = HappynessStatus(1,sad_number,flat_number,good_number,happy_number)
        serializer = HappynessStatusSerializer(happyness_status)
        return JSONResponse(serializer.data)

@csrf_exempt
def happyness_reg_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        happyness_reg = HappynessRegistration.objects.all()
        serializer = HappynessRegistrationSerializer(happyness_reg, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        # logger = logging.getLogger('testlogger')
        # logger.info("POST recieved. Request info:"+request)
        data = JSONParser().parse(request)
        serializer = HappynessRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def happyness_reg_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        happyness_reg = HappynessRegistration.objects.get(pk=pk)
    except HappynessRegistration.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HappynessRegistrationSerializer(happyness_reg)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HappynessRegistrationSerializer(happyness_reg, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        happyness_reg.delete()
        return HttpResponse(status=204)