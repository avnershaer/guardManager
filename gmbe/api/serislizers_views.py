from ..dal.dviews import Dal
from ..utils.operations_funcs import serialize_data
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from ..api.serializers import GuardinglistSerializer
from ..dal.models import GuardingList
import json


loggr = logger()
errlogger = err_logger()
dal = Dal()


# retrieve a list of objects from the database
def api_get_list(instance_model, model_serializer):
    loggr.info('///MOVE TO serializers_views.api_get_list()')
    try:
        objects_list = dal.table_objects_list(instance_model)
        if isinstance(objects_list, JsonResponse):
            return objects_list
        elif objects_list == None:
            return None
        serialized_lists =serialize_data(
            model_serializer=model_serializer, 
            instance_model=instance_model, 
            objects=objects_list, 
            many=True
            ).data
        return serialized_lists
    except Exception as e:
       loggr.error(f'ERROR AT serializers_views.api_get_list():{e}')
       raise e 

def api_get_glist_by_id(glist_id):
    loggr.info('///MOVE TO serializers_views.api_get_glist_by_id()')
    try:
        objects_list = dal.get_glist_by_id(glist_id)
        if isinstance(objects_list, JsonResponse):
            return objects_list
        elif objects_list == None:
            return None
        serialized_lists =serialize_data(
            model_serializer=GuardinglistSerializer, 
            instance_model=GuardingList, 
            objects=objects_list, 
            many=True
            ).data
        return serialized_lists
    except Exception as e:
       loggr.error(f'ERROR AT serializers_views.api_get_glist_by_id():{e}')
       raise e 
        
 
# get guarding lists in range of dates
def api_get_lists_by_dates(model, model_serializer, date1, date2):
    loggr.info('///MOVE TO serializers_views.get_lists_by_dates')
    try:
        lists_by_dates = dal.get_lists_by_dates(model, date1, date2)
        if isinstance(lists_by_dates, JsonResponse):
            return lists_by_dates
        elif lists_by_dates == None:
            return None
        serialized_lists =serialize_data(
            model_serializer=model_serializer, 
            instance_model=model, 
            objects=lists_by_dates, 
            many=True
            ).data
        return serialized_lists
    except Exception as e:
       loggr.error(f'ERROR AT serializers_views.get_lists_by_dates():{e}')
       raise e        


def api_instance_by_date(model, model_serializer, obj_date, date):
    loggr.info('///MOVE TO serializers_views.api_instance_by_date()')
    try:
        instance = dal.get_instance_by_date(model, obj_date, date)
        if isinstance(instance, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_instance_by_date():{instance}') 
            return instance
        elif instance == None:
            return None
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

def api_get_instance_by_date_position(date, position):
    loggr.info('///MOVE TO serializers_views.api_get_instance_by_date_position()')
    try:
        instance = dal.get_instance_by_date_position(date, position)
        if isinstance(instance, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_get_instance_by_date_position():{instance}') 
            return instance
        elif instance == None:
            return None
        serialized_instance = serialize_data(
            model_serializer=GuardinglistSerializer, 
            instance_model=GuardingList, 
            objects=instance, 
            many=True
            ).data
        return serialized_instance
    except Exception as e:
        loggr.error(f'ERROR AT serializers_views.api_get_instance_by_date_position():{e}')
        return JsonResponse({'status:':'ERROR AT serializers_views.api_get_instance_by_date_position()','details:':str(e)}, status=500, safe=False)

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