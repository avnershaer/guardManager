from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from ..facades.admin_facade import AdminFacade
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from rest_framework import status
from ..api.serializers import SetGuardingListSerializer
from rest_framework.parsers import MultiPartParser, FormParser


admin_facade = AdminFacade()
loggr = logger()
errlogger = err_logger()

@csrf_exempt
@api_view(['GET'])
def families_list(request):
    loggr.info(f'{request} request recived - admin_urls.families_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)
    try:
        families_list = admin_facade.get_all_families(request)
        return JsonResponse(
            {'Details': families_list}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    
@csrf_exempt  
@api_view(['GET'])
def users_list(request):
    loggr.info(f'{request} request recived - admin_urls.users_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        users_list = admin_facade.get_all_users(request)
        return JsonResponse(
            {'details:':users_list}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt  
@api_view(['GET'])
def fguards_list(request):
    loggr.info(f'{request} request recived - admin_urls.fguards_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        fguards_list = admin_facade.get_all_fguards(request)
        return JsonResponse(
            {'details':fguards_list}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt  
@api_view(['GET'])
def pguards_list(request):
    loggr.info(f'{request} request recived - admin_urls.pguards_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        fguards_list = admin_facade.get_all_pguards(request)
        return JsonResponse(
            {'details':fguards_list}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt    
@api_view(['GET'])
def positions_list(request):
    loggr.info(f'{request} request recived - admin_urls.positions_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        positions_list=admin_facade.get_Positions_list(request)
        return JsonResponse(
            {'details':positions_list}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    

@csrf_exempt    
@api_view(['GET'])
def paid_guards_list(request):
    loggr.info(f'{request} request recived - admin_urls.paid_guards_list()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        paid_guards_list=admin_facade.get_paid_guards_list(request)
        return JsonResponse(
            {'details':paid_guards_list}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt    
@api_view(['GET'])
def get_all_exchanges(request):
    loggr.info(f'{request} request recived - admin_urls.get_all_exchanges()')
    if request.method != 'GET':
        return JsonResponse({'error': 'GET requests only!'}, status=405)  
    try:
        all_exchanges = admin_facade.get_all_exchanges(request)
        return JsonResponse(
            {'details':all_exchanges}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    
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
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

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
            {'error':str(e)}, 
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
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

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
            {'error':str(e)}, 
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
            {'error':str(e)}, 
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
            {'error':str(e)}, 
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
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    
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
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    
@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def update_fguard(request):
    loggr.info(f'{request} request recived - admin_urls.update_fguard()')
    if request.method != 'POST':
        return JsonResponse({'error': 'POST requests only!'}, status=405)  
    try:
        fguard_pic = request.FILES.get('fguard_pic')
        loggr.info(f'Uploaded file: {fguard_pic}')
        updated_fguard = admin_facade.update_fguard(request)
        if isinstance(updated_fguard, JsonResponse):
                return updated_fguard
        elif updated_fguard == None:
            return JsonResponse(
                {'error': 'ERROR UPDATING GUARD - GOT NONE'}, 
                status=500
                )
        loggr.info(f'O.K UPDATED GUARD')
        return JsonResponse(
            {'status':'success', 'details':updated_fguard}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def update_pguard(request):
    loggr.info(f'{request} request recived - admin_urls.update_fguard()')
    if request.method != 'POST':
        return JsonResponse({'error': 'POST requests only!'}, status=405)  
    try:
        pguard_pic = request.FILES.get('pguard_pic')
        loggr.info(f'Uploaded file: {pguard_pic}')
        updated_pguard = admin_facade.update_pguard(request)
        if isinstance(updated_pguard, JsonResponse):
                return updated_pguard
        elif updated_pguard == None:
            return JsonResponse(
                {'error': 'ERROR UPDATING GUARD - GOT NONE'}, 
                status=500
                )
        loggr.info(f'O.K UPDATED GUARD')
        return JsonResponse(
            {'status':'success', 'details':updated_pguard}, 
            status=200, 
            safe=False
            )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    
@csrf_exempt
@api_view(['GET'])
def get_fguard_shifts(request, fguard_id):
    loggr.info(f'{request} request recived - admin_urls.get_fguard_shifts()')
    try:
        fguard = admin_facade.get_shifts_for_fguard(request, fguard_id)
        if fguard:
            return JsonResponse(
            {'status':'success', 'details':fguard}, 
            status=200, 
            safe=False
            )
        return JsonResponse(
                {'error': 'לא נמצאו משמרות לשומר'}, 
                status=500
                )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt
@api_view(['GET'])
def get_exchanges_for_fguard(request, fguard_id):
    loggr.info(f'{request} request recived - admin_urls.get_fguard_by_id()')
    try:
        fguard = admin_facade.get_exchanges_for_fguard(request, fguard_id)
        if fguard:
            return JsonResponse(
            {'status':'success', 'details':fguard}, 
            status=200, 
            safe=False
            )
        return JsonResponse(
                {'error': 'לא נמצאו החלפות לשומר'}, 
                status=404
                )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    
@csrf_exempt
@api_view(['GET'])
def get_did_exchanges_for_fguard(request, fguard_id):
    loggr.info(f'{request} request recived - admin_urls.get_did_exchanges_for_fguard()')
    try:
        fguard = admin_facade.get_did_exchanges_for_fguard(request, fguard_id)
        if fguard:
            return JsonResponse(
            {'status':'success', 'details':fguard}, 
            status=200, 
            safe=False
            )
        return JsonResponse(
                {'error': 'לא נמצאו החלפות לשומר'}, 
                status=500
                )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )

@csrf_exempt
@api_view(['GET'])
def get_paid_exchanges_for_fguard(request, fguard_id):
    loggr.info(f'{request} request recived - admin_urls.get_paid_exchanges_for_fguard()')
    try:
        fguard = admin_facade.get_paid_exchanges_for_fguard(request, fguard_id)
        if fguard:
            return JsonResponse(
            {'status':'success', 'details':fguard}, 
            status=200, 
            safe=False
            )
        return JsonResponse(
                {'error': 'לא נמצאו החלפות בשכר לשומר'}, 
                status=404
                )
    except Exception as e:
        return JsonResponse(
            {'error':str(e)}, 
            status=500, 
            safe=False
            )
    
