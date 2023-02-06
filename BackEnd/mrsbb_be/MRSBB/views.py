from django.http import HttpResponse
import json

# Create your views here.


def get_api(request):
    if request.method == 'GET':
        try:
            response = json.dumps([{'hello': "world"}])
        except:
            response = json.dumps([{'Error': 'No'}])
    return HttpResponse(response, content_type='application/json')
