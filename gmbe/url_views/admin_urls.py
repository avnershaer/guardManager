from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from ..facades.admin_facade import AdminFacade
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from rest_framework import status
from ..api.serializers import SetGuardingListSerializer

admin_facade = AdminFacade()
loggr = logger()
errlogger = err_logger()

@csrf_exempt
@api_view(['GET'])
def families_list(request):
    loggr.info(f'{request} request recived - admin_urls.families_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  # Return a 405 Method Not Allowed error
    try:
        # get list of all families  
        families_list = admin_facade.get_all_families(request)
        # successful response with the list 
        return JsonResponse({'Details': families_list}, status=200, safe=False)
    # handle any exceptions that occur while fetching the list
    except Exception as e:
        return JsonResponse({'status': 'ERROR at url_views.admin_urls.families_list()','details':str(e)}, status=500, safe=False)

@csrf_exempt  
@api_view(['GET'])
def users_list(request):
    loggr.info(f'{request} request recived - admin_urls.users_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        users_list = admin_facade.get_all_users(request)
        return JsonResponse({'details:':users_list}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'ERROR at url_views.admin_urls.users_list()','details':str(e)}, status=500, safe=False)

@csrf_exempt    
@api_view(['GET'])
def positions_list(request):
    loggr.info(f'{request} request recived - admin_urls.positions_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        positions_list=admin_facade.get_Positions_list(request)
        return JsonResponse({'details':positions_list}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'ERROR at url_views.admin_urls.positions_list()','details':str(e)}, status=500, safe=False)
    

@csrf_exempt    
@api_view(['GET'])
def paid_guards_list(request):
    loggr.info(f'{request} request recived - admin_urls.paid_guards_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        paid_guards_list=admin_facade.get_paid_guards_list(request)
        return JsonResponse({'details':paid_guards_list}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'ERROR at admin_urls.paid_guards_list()','details':str(e)}, status=500, safe=False)

@csrf_exempt    
@api_view(['GET'])
def get_all_exchanges(request):
    loggr.info(f'{request} request recived - admin_urls.get_all_exchanges()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        all_exchanges = admin_facade.get_all_exchanges(request)
        return JsonResponse({'details':all_exchanges}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'ERROR at admin_urls.get_all_exchanges()','details':str(e)}, status=500, safe=False)
    
@csrf_exempt
@api_view(['GET'])
def shifts_list(request):
    loggr.info(f'{request} request recived - admin_urls.shifts_list()')
    if request.method != 'GET':
        return JsonResponse({'status':'error', 'Details':'GET requests only!'}, status=405)  
    try:
        shifts_list = admin_facade.get_shifts_list(request)
        return JsonResponse({'status':'success', 'Details':shifts_list})
    except Exception as e:
        return JsonResponse({'status': 'ERROR at admin_urls.shifts_list()','details':str(e)}, status=500, safe=False)

@csrf_exempt
@api_view(['POST'])
def create_guard_list(request):
    loggr.info(f'{request} request recived - admin_urls.create_guard_list()')
    if request.method != 'POST':
        return JsonResponse({'error': 'POST requests only!'}, status=405)  
    try:
        guard_list = admin_facade.create_guard_list(request)
        loggr.info('got guard_list at admin_urls.create_guard_list()')
        return JsonResponse(
            {'status':'success', 'Details': 
             guard_list}, 
             status=200, 
             safe=False)
    
    except Exception as e:
        return JsonResponse(
            {'status': 'ERROR at url_views.admin_urls.create_guard_list()','details':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt
@api_view(['POST'])
def save_guarding_list(request):
    loggr.info(f'{request} request recived - admin_urls.save_guarding_list()')
    if request.method != 'POST':
        return JsonResponse({'error': 'POST requests only!'}, status=405)  
    try:
        glist = admin_facade.save_guarding_list(request)
        loggr.info(f'O.K GLIST')
        return glist
    except Exception as e:
        return JsonResponse({'status':'ERROR', 'Details':str(e)})

@csrf_exempt
@api_view(['PUT'])
def exchange_guard(request):
    loggr.info(f'{request} request recived - admin_urls.exchange_guard()')
    if request.method != 'PUT':
        return JsonResponse({'error': 'PUT requests only!'}, status=405)  
    try:
        ex_type = 'ordinary'
        exchange_result = admin_facade.reg_exchange_guard(request, ex_type)
        if exchange_result == None:
            return JsonResponse(
                {'status':'OK for exchange BUT DID NOT write the exchange', 'Details':exchange_result}, 
                status=200, 
                safe=False
                )
        loggr.info(f'OK exchange_guard')
        return JsonResponse(
            {'status':'success', 'Details': exchange_result}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'status':'ERROR', 'Details':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt
@api_view(['PUT'])
def paid_exchange_guard(request):
    loggr.info(f'{request} request recived - admin_urls.paid_exchange_guard()')
    if request.method != 'PUT':
        return JsonResponse({'error': 'PUT requests only!'}, status=405)  
    try:
        ex_type = 'paid'
        exchange_result = admin_facade.paid_exchange_guard(request, ex_type)
        if exchange_result == None:
            return JsonResponse(
                {'status':'OK for exchange BUT DID NOT write the exchange', 'Details':exchange_result}, 
                status=200, 
                safe=False
                )
        loggr.info(f'OK exchange_guard')
        return JsonResponse(
            {'status':'success', 'Details': exchange_result}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'status':'ERROR', 'Details':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt
@api_view(['PUT'])
def cross_exchange_guards(request):
    loggr.info(f'{request} request recived - admin_urls.cross_exchange_guards()')
    if request.method != 'PUT':
        return JsonResponse({'error': 'PUT requests only!'}, status=405)  
    try:
        ex_type = 'cross'
        exchange_result = admin_facade.cross_exchange_guard(request, ex_type)
        loggr.info(f'OK cross exchange_guards')
        return JsonResponse(
            {'status':'success', 'Details': exchange_result}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'status':'ERROR', 'Details':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt
@api_view(['GET'])
def get_exchange_report_by_type(request, ex_type):
    loggr.info(f'{request} request recived - admin_urls.get_exchange_report_by_type()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405, safe=False)  
    try:
        exchange_report_by_type = admin_facade.get_exchange_list_by_type(ex_type)
        if exchange_report_by_type == None:
            return JsonResponse(
                {'status':'none', 'details':"אין דוחות להצגה"}, 
                status=404, 
                safe=False
                )
        loggr.info('OK get_exchange_report_by_type')
        return JsonResponse(
            {'status':'success', 'details':exchange_report_by_type}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse({'status':'ERROR', 'Details':str(e)}, status=500, safe=False)

@csrf_exempt
@api_view(['POST'])
def create_position(request):
    loggr.info(f'{request} request recived - admin_urls.create_position()')
    if request.method != 'POST':
        return JsonResponse({'error': 'POST requests only!'}, status=405)  
    try:
        new_position = admin_facade.create_position(request)
        if isinstance(new_position, JsonResponse):
                return new_position
        loggr.info(f'O.K CREATE POSITION')
        return JsonResponse(
            {'status':'success', 'details':new_position}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse({'status':'ERROR', 'Details':str(e)})
