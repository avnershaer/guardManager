from ..dal.dviews import Dal
from ..utils.operations_funcs import serialize_data
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from ..api.serializers import GuardinglistSerializer

loggr = logger()
errlogger = err_logger()
dal = Dal()


# retrieve a list of objects from the database
def api_get_list(instance_model, model_serializer):
    loggr.info('///MOVE TO serializers_views.api_get_list()')
    try:
        # get a list of objects using the data access layer (dal)
        objects_list = dal.table_objects_list(model=instance_model)
        # if got an error message from dviews
        if isinstance(objects_list, JsonResponse): 
            return objects_list
        # no errors - serialize the data 
        obj_list = serialize_data(model_serializer=model_serializer, instance_model=instance_model, objects=objects_list, many=True).data
        # return jsonresponse with object list
        loggr.info(f'obj_list:{obj_list}')
        return obj_list
        
    # handle any exceptions that occur during processing this method      
    except Exception as e:
        return JsonResponse({'status:':'ERROR serializers.api_get_list','details:':str(e)}, status=500, safe=False)

def api_instance_by_date(model, model_serializer, obj_date, date):
    loggr.info('///MOVE TO serializers_views.api_instance_by_date()')
    try:
        instance = dal.get_instance_by_date(model, obj_date, date)
        
        if isinstance(instance, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_instance_by_date():{instance}') 
            return instance
        serialized_instance = serialize_data(
            model_serializer=model_serializer, 
            instance_model=model, 
            objects=instance, 
            many=True
            ).data
        return serialized_instance
    except Exception as e:
        loggr.error(f'ERROR AT serializers_views.api_instance_by_date():{e}')
        return JsonResponse({'status:':'ERROR AT serializers_views.api_instance_by_date()','details:':str(e)}, status=500, safe=False)
        
def api_get_last_id():
    loggr.info('///MOVE TO serializers_views.api_get_last_id()')
    try:
        last_id = dal.get_last_id()
        if isinstance(last_id, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_get_last_id():{last_id}') 
            return last_id
        loggr.info(f'*****last_id:{last_id}')
        return last_id
    except Exception as e:
        loggr.error(f'ERROR AT serializers_views.api_get_last_id():{e}')
        return JsonResponse({'status:':'ERROR AT serializers_views.api_get_last_id()','details:':str(e)}, status=500, safe=False)