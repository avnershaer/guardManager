from loggers.loggers import logger, err_logger
from django.http import JsonResponse
from ..dal.models import Position, Families, Shift, Fguard, PaidGuards
from ..dal.dviews import Dal
from ..api.serializers import PositionSerializer, ShiftSerializer, FguardSerializer, PaidGuardsSerializer

dal =Dal()
loggr = logger()
errlogger = err_logger()

def fetch_required_instances(model, instance, entity_id, model_serializer ):
    loggr.info('///MOVE TO requests_data.fetch_required_instances()')
    from ..api.serislizers_views import api_get_instance_by_entity_id
    try:
        instance = api_get_instance_by_entity_id(model, model_serializer, instance, entity_id)
        if instance == None:
            return None
        return instance
    except Exception as e:
        loggr.error((f'ERROR at requests_data.fetch_required_instances():{e}'))
        return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)

def get_instances(position_id, guard_id, substitute_guard, shift_id, ex_type):
    loggr.info('///MOVE TO requests_data.get_instances()')
    try:
        position_instance = fetch_required_instances(
                model = Position, 
                model_serializer = PositionSerializer,
                instance = 'position_id', 
                entity_id = position_id
                )
        if position_instance == None:
            return None
        
        shift_instance = fetch_required_instances(
                model=Shift,
                model_serializer = ShiftSerializer, 
                instance = 'shift_id', 
                entity_id = shift_id
                )
        if shift_instance == None:
            return None
        
        origin_guard_instance = fetch_required_instances(
                model=Fguard, 
                model_serializer = FguardSerializer,
                instance = 'fguard_id', 
                entity_id = guard_id
                )
        if origin_guard_instance == None:
            return None
        
        if ex_type == 'ordinary':
            substitute_guard_id = dal.get_first_fguard_id_by_family_id(
                    family_id=substitute_guard, 
                    ex_type = ex_type
                    )
            if substitute_guard_id == None:
                return None
            substitute_guard_instance = fetch_required_instances(
                    model=Fguard, 
                    model_serializer = FguardSerializer,
                    instance = 'fguard_id', 
                    entity_id = substitute_guard_id
                    )
            substitute_pguard_instance = None

        elif ex_type == 'cross':
            substitute_guard_instance = fetch_required_instances(
                    model=Fguard, 
                    model_serializer = FguardSerializer,
                    instance = 'fguard_id', 
                    entity_id = substitute_guard
                    )
            substitute_pguard_instance = None

        elif ex_type == 'paid':
            substitute_guard_id = dal.get_first_fguard_id_by_family_id(
                    family_id=substitute_guard['family_id'], 
                    ex_type = ex_type
                    )
            if substitute_guard_id == None:
                return None
            substitute_pguard_instance = fetch_required_instances(
                    model=PaidGuards, 
                    model_serializer = PaidGuardsSerializer,
                    instance = 'pguard_id', 
                    entity_id = substitute_guard_id
                    )
            substitute_guard_instance = None

        return {
            'position_instance': position_instance, 
            'shift_instance': shift_instance, 
            'origin_guard_instance': origin_guard_instance, 
            'substitute_guard_instance': substitute_guard_instance,
            'substitute_pguard_instance': substitute_pguard_instance,
        }
    except Exception as e:
        loggr.error((f'ERROR at requests_data.get_instances():{e}'))
        return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)
    
def exchange_data_dict(instances, list_date, list_day, shift_hour, ex_type):
    loggr.info('///MOVE TO requests_data.exchange_data_dict()')
    try:
        exchange_data = {
                'origin_guard_id': instances['origin_guard_instance'],
                'shift_id': instances['shift_instance'],
                'substitute_fguard_id': instances['substitute_guard_instance'],
                'substitute_Pguard_id': instances['substitute_pguard_instance'],
                'position_id': instances['position_instance'],
                'exchange_date': list_date,
                'exchange_day': list_day,
                'exchange_hour': shift_hour,
                'exchange_type': ex_type,
            }   
        return exchange_data
    except Exception as e:
        loggr.error((f'ERROR at requests_data.exchange_data_dict():{e}'))
        return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)
    
def exchange_request_data(ex_type, ex_data, substitute_guard):
    loggr.info('///MOVE TO requests_data.requests_data()')
    try:
        guard_id = ex_data.get('guardId')
        shift_id = ex_data.get('shiftId')
        position_id = ex_data.get('posId')
        list_date = ex_data.get('glistDate')
        list_day = ex_data.get('glistDay')
        shift_hour = ex_data.get('shiftHour')
        instances = get_instances(position_id, guard_id, substitute_guard, shift_id, ex_type)
        if instances == None:
            return None
        exchange_data = exchange_data_dict(instances, list_date, list_day, shift_hour, ex_type)
        if isinstance(exchange_data, JsonResponse):
            return exchange_data
        return exchange_data
    except Exception as e:
        return JsonResponse({'status':'error', 'details':e}, status=500, save=False)

def fguard_data(request):
    loggr.info('///MOVE TO requests_data.fguard_data()')
    try:
        fguard_name = request.data.get('fguard_name')
        fguard_phone = request.data.get('fguard_phone')
        fguard_email = request.data.get('fguard_email')
        fguard_id = request.data.get('fguard_id')
        armed = request.data.get('armed')
        cap_armed = armed.capitalize()
        fguard_pic = request.FILES.get('fguard_pic')

        data_for_update = {
            'fguard_id': fguard_id,
            'fguard_name': fguard_name,
            'fguard_phone': fguard_phone,
            'fguard_email': fguard_email,
            'armed': cap_armed
        }
        data_for_update['fguard_pic'] = fguard_pic
        return data_for_update
    except Exception as e:
        loggr.error(f'error at requests_data.fguard_data(): {str(e)}')  
        return JsonResponse({'status': 'error', 'details': str(e)}, status=500)

def pguard_data(request):
    loggr.info('///MOVE TO requests_data.Pguard_data()')
    try:
        pguard_name = request.data.get('pguard_name')
        pguard_phone = request.data.get('pguard_phone')
        pguard_email = request.data.get('pguard_email')
        pguard_id = request.data.get('pguard_id')
        armed = request.data.get('armed')
        cap_armed = armed.capitalize()
        pguard_pic = request.FILES.get('pguard_pic')

        data_for_update = {
            'pguard_id': pguard_id,
            'pguard_name': pguard_name,
            'pguard_phone': pguard_phone,
            'pguard_email': pguard_email,
            'armed': cap_armed
        }
        data_for_update['pguard_pic'] = pguard_pic
        return data_for_update
    except Exception as e:
        loggr.error(f'error at requests_data.pguard_data(): {str(e)}')  
        return JsonResponse({'status': 'error', 'details': str(e)}, status=500)