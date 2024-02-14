from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from ..facades.admin_facade import AdminFacade
from django.http import JsonResponse
from loggers.loggers import logger, err_logger

admin_facade = AdminFacade()
loggr = logger()
errlogger = err_logger()

@csrf_exempt
@api_view(['GET'])
def families_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  # Return a 405 Method Not Allowed error

    try:
        loggr.info('OK ------------got test 1')
        # get list of all families  
        families_list = admin_facade.get_all_families(request)
            # successful response with the list 
        return families_list

    # handle any exceptions that occur while fetching the list
    except Exception as e:
        return JsonResponse({'status': 'ERROR at url_views.families_list()','details':str(e)}, status=500, safe=False)
    
@api_view(['GET'])
def users_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    
    try:
        users_list = admin_facade.get_all_users(request)
        return users_list

    except Exception as e:
        return JsonResponse({'status': 'ERROR at url_views.families_list()','details':str(e)}, status=500, safe=False)
    

