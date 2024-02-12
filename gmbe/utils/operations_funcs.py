from loggers.loggers import logger 
from django.http import JsonResponse


loggr = logger()


# serialize recived data
def serialize_data(instance_model, model_serializer, objects, many):
    
    try:
        # if there are objects to serialize
        if objects:
            loggr.info(f'O.K got objects for serialize - operations_funcs.serialize_data - HTTP/1.1 200 {instance_model}')
            
            # serialize the objects using the provided model serializer
            serialize_data = model_serializer(objects, many=many)
            logger.info(f'O.K objects BEEN SERIALIZED - operations_funcs.serialize_data - HTTP/1.1 200')
            
            # successful jsonresponse with serialized data
            return JsonResponse({'status': 'success O.K HTTP/1.1 200', 'Details': serialize_data}, status=200, safe=False)
        
        # if no objects to serialize
        else:
            # error jsonresponse if serialized data is not valid
            return JsonResponse({'status':f'ERROR', 'details':'NO objects for serialize- HTTP/1.1 500'}, status=500)(obj=objects)
    
    except Exception as e:
        return (f'ERROR:{e}')