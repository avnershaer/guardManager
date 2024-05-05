from loggers.loggers import logger
from django.http import JsonResponse
from ..api.serializers import *
from datetime import datetime
from ..dal.models import Shift
loggr = logger()


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
    

    
