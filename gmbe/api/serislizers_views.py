from ..dal.dviews import Dal
from ..utils.operations_funcs import serialize_data
from django.http import JsonResponse
from loggers.loggers import logger, err_logger


loggr = logger()
errlogger = err_logger()
dal = Dal()


# retrieve a list of objects from the database
def api_get_list(instance_model, model_serializer):
    loggr.info('OK ------------got test 3')
    try:
        # get a list of objects using the data access layer (dal)
        objects_list = dal.table_objects_list(model=instance_model)
        # if got an error message from dviews
        if isinstance(objects_list, JsonResponse): 
            return objects_list
        # no errors - serialize the data 
        obj_list = serialize_data(model_serializer=model_serializer, instance_model=instance_model, objects=objects_list, many=True)
        # return jsonresponse with object list
        return obj_list
        
    # handle any exceptions that occur during processing this method      
    except Exception as e:
        return JsonResponse({'status:':'ERROR serializers.api_get_list','details:':str(e)}, status=500, safe=False)
