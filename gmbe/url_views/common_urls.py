from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from ..facades.common_facade import CommonFacade

common_fadcade= CommonFacade()
loggr = logger()
errlogger = err_logger()

@csrf_exempt
@api_view(['GET'])
def get_lists_by_dates(request, date1, date2):
    loggr.info('GOT TO url_views.get_lists_by_dates()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        lists_by_dates = common_fadcade.get_lists_by_dates(date1, date2)
        if lists_by_dates == None:
            return JsonResponse({'status':'none', 'details':'לא נמצאו רשימות שמירה לטווח התאריכים הנ"ל'}, status=404)
        loggr.info(f'LISTS BY DATES:{str(lists_by_dates)}')
        return JsonResponse({'status':'success', 'Details':lists_by_dates}, status=200, safe=False)
    except Exception as e:
        return loggr.info(f'ERROR get_lists_by_dates(): {e}')
        
