from loggers.loggers import logger, err_logger
from django.http import JsonResponse
from ..dal.models import Position, Families, Shift
from ..api.serislizers_views import api_get_instance_by_entity_id


loggr = logger()
errlogger = err_logger()

def fetch_required_instances(model, instance, entity_id):
    loggr.info('///MOVE TO requests_data.fetch_required_instances()')
    try:
        instance = api_get_instance_by_entity_id(model, instance, entity_id)
        if instance == None:
            return None
        return instance
    except Exception as e:
        loggr.error((f'ERROR at requests_data.fetch_required_instances():{e}'))
        return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)

def get_instances(position_id, guard_id, substitute_guard, shift_id):
    loggr.info('///MOVE TO requests_data.get_instances()')
    try:
        position_instance = fetch_required_instances(
                model = Position, 
                instance = 'position_id', 
                entity_id = position_id
                )
        if position_instance == None:
            return None
        shift_instance = fetch_required_instances(
                model=Shift, 
                instance = 'shift_id', 
                entity_id = shift_id
                )
        if shift_instance == None:
            return None
        origin_guard_instance = fetch_required_instances(
                model=Families, 
                instance = 'family_id', 
                entity_id = guard_id
                )
        if origin_guard_instance == None:
            return None
        substitute_guard_instance = fetch_required_instances(
                model=Families, 
                instance = 'family_id', 
                entity_id = substitute_guard
                )
        if substitute_guard_instance == None:
            return None
        return {
            'position_instance': position_instance, 
            'shift_instance': shift_instance, 
            'origin_guard_instance': origin_guard_instance, 
            'substitute_guard_instance': substitute_guard_instance
        }
    except Exception as e:
        loggr.error((f'ERROR at requests_data.get_instances():{e}'))
        return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)
    
def exchange_data_dict(instances, list_date, list_day, shift_hour, ex_type):
    loggr.info('///MOVE TO requests_data.exchange_data()')
    try:
        exchange_data = {
                'origin_guard_id': instances['origin_guard_instance'],
                'shift_id': instances['shift_instance'],
                'substitute_guard_id': instances['substitute_guard_instance'],
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
        instances = get_instances(position_id, guard_id, substitute_guard, shift_id)
        if instances == None:
            return None
        exchange_data = exchange_data_dict(instances, list_date, list_day, shift_hour, ex_type)
        if isinstance(exchange_data, JsonResponse):
            return exchange_data
        return exchange_data
    except Exception as e:
        return JsonResponse({'status':'error', 'details':e}, status=500, save=False)

