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


def api_create_new(model, model_serializer, data):
    loggr.info('///MOVE TO serializers_views.api_create_new()')
    try:
        new_instance = dal.create_new(model, **data)
        if isinstance(new_instance, JsonResponse):
            return new_instance       
        serialized_details = serialize_data(
            model, 
            model_serializer, 
            new_instance,
            False
            )
        if isinstance(serialized_details, JsonResponse):
            return serialized_details
        return serialized_details.data
    except Exception as e:
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_create_new()','details:':str(e)}, 
            status=500, 
            safe=False
            )


def api_get_list(instance_model, model_serializer):
    loggr.info('///MOVE TO serializers_views.api_get_list()')
    try:
        objects_list = dal.table_objects_list(instance_model)
        if isinstance(objects_list, JsonResponse):
            return objects_list
        elif objects_list == None:
            return None
        serialized_lists = serialize_data(
            model_serializer =model_serializer, 
            instance_model = instance_model, 
            objects = objects_list, 
            many = True
            ).data
        return serialized_lists
    except Exception as e:
       loggr.error(f'ERROR AT serializers_views.api_get_list():{e}')
       return JsonResponse(
           {'status:':'ERROR AT serializers_views.api_get_list()','details:':str(e)}, 
           status=500, 
           safe=False
           )

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
       return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_get_glist_by_id()'}, 
            status=500, 
            safe=False
            )
         

def api_get_instances_by_parm(model, instance, parm, model_serializer):
    loggr.info('///MOVE TO serializers_views.api_get_instance_by_parm()')
    try:
        instances_by_parm = dal.get_instance_by_parm(model, instance, parm)
        if isinstance(instances_by_parm, JsonResponse):
            return instances_by_parm
        elif instances_by_parm == None:
            return None
        serialized_lists =serialize_data(
            model_serializer=model_serializer, 
            instance_model=model, 
            objects=instances_by_parm, 
            many=True
            ).data
        return serialized_lists
    except Exception as e:
        loggr.error(f'ERROR AT serializers_views.api_get_instance_by_parm():{e}')
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_get_instances_by_parm()'}, 
            status=500, 
            safe=False
            )
        
 
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
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_get_lists_by_dates()','details:':str(e)}, 
            status=500, 
            safe=False
            )

def api_instance_by_date(model, model_serializer, obj_date, date):
    loggr.info('///MOVE TO serializers_views.api_instance_by_date()')
    try:
        instance = dal.get_instance_by_date(model, obj_date, date)
        if isinstance(instance, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_instance_by_date()') 
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
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_instance_by_date()','details:':str(e)},
            status=500, 
            safe=False
            )

def api_get_instance_by_date_position(date, position):
    loggr.info('///MOVE TO serializers_views.api_get_instance_by_date_position()')
    try:
        instance = dal.get_instance_by_date_position(date, position)
        if isinstance(instance, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_get_instance_by_date_position()') 
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
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_get_instance_by_date_position()','details:':str(e)}, 
            status=500, 
            safe=False
            )

def api_get_last_id():
    loggr.info('///MOVE TO serializers_views.api_get_last_id()')
    try:
        last_id = dal.get_last_id()
        if isinstance(last_id, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_get_last_id()') 
            return last_id
        loggr.info(f'*****last_id:{last_id}')
        return last_id
    except Exception as e:
        loggr.error(f'ERROR AT serializers_views.api_get_last_id():{e}')
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_get_last_id()','details:':str(e)}, 
            status=500, 
            safe=False
            )

def api_get_instance_by_entity_id(model, instance, entity_id):
    loggr.info('///MOVE TO serializers_views.api_get_instance_by_entity_id()')
    try:
        fetched_instance = dal.get_instance_by_entity_id(model, instance, entity_id)
        if fetched_instance == None:
            return None
        return fetched_instance
    except Exception as e:
        loggr.error(f'ERROR AT serializers_views.api_get_instance_by_entity_id():{e}')
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_get_instance_by_entity_id()','details:':str(e)}, 
            status=500, 
            safe=False
            )

def api_get_futu_lists():
    loggr.info('///MOVE TO serializers_views.api_get_futu_lists()')
    try:
        futu_lists = dal.get_future_lists()
        if isinstance(futu_lists, JsonResponse):
            loggr.error(f'ERROR AT serializers_views.api_get_futu_lists()') 
            return futu_lists
        elif futu_lists == None:
            return None
        serialized_instance = serialize_data(
            model_serializer=GuardinglistSerializer, 
            instance_model=GuardingList, 
            objects=futu_lists, 
            many=True
            ).data
        return serialized_instance
    except Exception as e:
        loggr.error(f'ERROR AT serializers_views.api_get_futu_lists():{e}')
        return JsonResponse(
            {'status:':'ERROR AT serializers_views.api_get_futu_lists()','details:':str(e)}, 
            status=500, 
            safe=False
            )
