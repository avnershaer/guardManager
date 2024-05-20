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
    loggr.info('///// MOVE TO url_views.get_lists_by_dates()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405, safe=False)  
    try:
        lists_by_dates = common_fadcade.get_lists_by_dates(date1, date2)
        if lists_by_dates == None:
            return JsonResponse({'status':'none', 'details':'לא נמצאו רשימות שמירה לטווח התאריכים הנ"ל'}, status=404, safe=False)
        loggr.info(f'LISTS BY DATES:{str(lists_by_dates)}')
        return JsonResponse({'status':'success', 'Details':lists_by_dates}, status=200, safe=False)
    except Exception as e:
        loggr.info(f'ERROR get_lists_by_dates(): {e}')
        return JsonResponse({'status':'ERROR', 'Details':str(e)}, status=500, safe=False)

@csrf_exempt  
@api_view(['GET'])
def get_glist_by_date(request, date):
    loggr.info('///// MOVE TO url_views.get_glist_by_date()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405, safe=False)  
    try:
        date = str(date)
        loggr.info(f'***date:{date}') 
        glist = common_fadcade.get_glist_by_date(date)
        if glist == None:
            return JsonResponse({'status':'none', 'details':'לא נמצאו רשימות שמירה לתאריך הנ"ל'}, status=404, safe=False)
        loggr.info(f'GLIST BY DATE:{str(glist)}')
        return JsonResponse({'status':'success', 'Details':glist}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status':'ERROR', 'Details':str(e)}, status=500, safe=False)

@csrf_exempt  
@api_view(['GET'])
def get_glist_by_id(request, glist_id):
    loggr.info('///// MOVE TO common_urls.get_glist_by_id()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405, safe=False)  
    try:
        glist_id = int(glist_id)
        glist = common_fadcade.get_glist_by_id(glist_id)
        if glist == None:
            return JsonResponse({'status':'none', 'details':'לא נמצאה רשימת שמירה לתאריך הנ"ל'}, status=404, safe=False)
        loggr.info(f'GLIST BY DATE:{str(glist)}')
        return JsonResponse({'status':'success', 'Details':glist}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status':'ERROR', 'Details':str(e)}, status=500, safe=False)

@csrf_exempt
@api_view(['GET'])
def get_list_by_date_position(request, date, position_id):
    loggr.info('///// MOVE TO url_views.get_glist_by_date()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405, safe=False)  
    try:
        date = str(date)
        position = int(position_id)
        loggr.info(f'***date:{date}, ***position:{position}') 
        list_by_date_position = common_fadcade.get_instance_by_date_position(date, position)
        if list_by_date_position == None:
            return JsonResponse({'status':'none', 'details':'לא נמצאו רשימות שמירה לתאריך הנ"ל'}, status=404, safe=False)
        loggr.info(f'GLIST BY DATE and POSITION:{str(list_by_date_position)}')
        return JsonResponse({'status':'success', 'Details':list_by_date_position}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status':'ERROR', 'Details':str(e)}, status=500, safe=False)

@csrf_exempt
@api_view(['GET'])
def guarding_list(request):
    loggr.info(f'{request} request recived - admin_urls.guarding_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        guarding_list = common_fadcade.get_guarding_list(request)
        if guarding_list == None:
            return JsonResponse({'status':'none', 'details':'לא נמצאה רשימת שמירה לתאריך הנ"ל'}, status=404, safe=False)
        loggr.info(f'GLIST BY DATE and POSITION:{str(guarding_list)}')
        return JsonResponse({'status':'success', 'Details':guarding_list}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status':'ERROR', 'Details':str(e)}, status=500, safe=False)        
