from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from ..api.serislizers_views import api_get_last_id

loggr = logger()
errlogger = err_logger()

@csrf_exempt
@api_view(['GET'])
def get_last_id(request):
    loggr.info('GOT TO url_views.get_last_id()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        last_id = api_get_last_id()
        loggr.info(f'RETURN LAST ID:{last_id}')
        # successful response with last family id from shifts
        return JsonResponse({'status':'success', 'Details': last_id}, status=200, safe=False)
    # handle any exceptions that occur while fetching last family id from shifts
    except Exception as e:
        return JsonResponse({'status': 'ERROR at url_views.anonymous_urls.get_last_id()','details':str(e)}, status=500, safe=False)