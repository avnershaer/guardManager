from loggers.loggers import logger, err_logger
from django.http import JsonResponse
from ..api.serializers import *
from ..utils.requests_data import exchange_request_data
from ..dal.models import Shift, Exchanges
from ..dal.dviews import Dal


dal = Dal()
loggr = logger()
errlogger = err_logger()


# serialize recived data
def serialize_data(instance_model, model_serializer, objects, many):
    loggr.info('got to operations_funcs.serialize_data()')
    try:
        # if there are objects to serialize
        if objects:
            loggr.info(f'O.K got objects for serialize - operations_funcs.serialize_data - HTTP/1.1 200 {instance_model}')
            
            # serialize the objects using the provided model serializer
            serialize_data = model_serializer(objects, many=many)
            loggr.info(f'O.K objects BEEN SERIALIZED at operations_funcs.serialize_data SERIALIZED DATA:{serialize_data}')
            
            # successful jsonresponse with serialized data
            return serialize_data
        
        # if no objects to serialize
        else:
            # error jsonresponse if serialized data is not valid
            return JsonResponse({'status':f'ERROR', 'details':'NO objects for serialize- HTTP/1.1 500'}, status=500, safe=False)
    
    except Exception as e:
        loggr.error(f'ERROR at operations_funcs.serialize_data: {e}')
        return JsonResponse({'status:':'ERROR raised at operations_funcs.serialize_data:', 'details:':str(e)}, status=500, safe=False)
    
def get_last_id():
    loggr.info('got to operations_funcs.get_last_id()')
    try:
        shifts = Shift.objects.all()
        guards_id_list = []
        for shift in shifts:
            guards = shift.family_id.all()
            loggr.info(f'====**guards:{guards}')
            for guard in guards:
                guards_id_list.append(guard.family_id)
                loggr.info(f'======guard.id:{guard.family_id}')
        # last family_id
        if guards_id_list:
            last_id = guards_id_list[-1]
        else:
            last_id = None
        return int(last_id)
    except Exception as e:
        loggr.error(f'error at utils.operations_funcs.get_last_id():{e}')
        return e

# get last id for guarding list
def get_shift_last_id(shift_dict):
    loggr.info('GOT TO operations_funcs.get_shift_last_id()')
    id_list = []
    try:
        # iterate over the dictionary whith the guard keys
        for guard_key, guard_data in shift_dict.items():
            guards = guard_data.get('guards', {})
            for guard_id, guard_details in guards.items():
                family_id = guard_details.get('family', {}).get('family_id')
                if family_id is not None:
                    id_list.append(family_id)
        
        loggr.info(f'ID LIST: {id_list}')
        if id_list:
            last_id = id_list[-1]
            loggr.info(f'LAST ID:{last_id}')
            return last_id
        else:
            loggr.error('ERROR: No guards found in shift_dict')
            return None
    except Exception as e:
        loggr.error(f'ERROR at operations_funcs.get_shift_last_id(): {e}')
        return JsonResponse({'status:':'ERROR raised at operations_funcs.serialize_data:', 'details:':str(e)}, status=500, safe=False)

def english_to_hebrew_days():
    loggr.info(f'GOT TO operation_funcs.create_guarding_list()')
    return {
    'Monday': 'יום שני',
    'Tuesday': 'יום שלישי',
    'Wednesday': 'יום רביעי',
    'Thursday': 'יום חמישי',
    'Friday': 'יום שישי',
    'Saturday': 'יום שבת',
    'Sunday': 'יום ראשון'
    }

def handle_exchange_guard(ex_type, ex_data, substitute_guard):
        loggr.info('///MOVE TO admin_facade.reg_exchange_guard()')
        from ..api.serislizers_views import api_create_new
        try:
            request_data = exchange_request_data(ex_type, ex_data, substitute_guard)
            if isinstance(request_data, JsonResponse):
                return request_data
            
            reg_exchange = dal.exchange_guard(
                request_data['shift_id'], 
                request_data['origin_guard_id'], 
                request_data['substitute_guard_id']
                )
            
            if reg_exchange:
                loggr.info('OK_EXCHANGE')
                write_exchange = api_create_new(Exchanges, ExchangesSerializer, request_data)
                if write_exchange:
                    loggr.info(f'OK_write_exchange: {write_exchange}')
                    return write_exchange
            
            loggr.info('write_exchange: none')  
            return None
        
        except Exception as e:
            loggr.error((f'ERROR at admin_facade.reg_exchange_guard:{e}'))
            return JsonResponse({'status':'error', 'details':e}, status=500, safe=False) 

    


    
