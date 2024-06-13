from loggers.loggers import logger, err_logger
from ..api.serislizers_views import api_get_lists_by_dates, api_instance_by_date, api_get_instance_by_date_position, api_get_list, api_get_glist_by_id, api_get_futu_lists
from django.http import JsonResponse
from ..dal.models import GuardingList, Fguard
from ..api.serializers import GuardinglistSerializer
from ..utils.operations_funcs import get_family_id_from_glist, get_guard_by_family_id

loggr = logger()
errlogger = err_logger()


class CommonFacade():

    def get_lists_by_dates(self, date1, date2):
        loggr.info('///MOVE TO common_facade.get_lists_by_dates()') 
        try:
            lists_by_dates = api_get_lists_by_dates(
                model = GuardingList,
                model_serializer = GuardinglistSerializer,
                date1 = date1,
                date2 = date2
                )
            if lists_by_dates == None:
                  loggr.info(f'lists_by_dates == NONE')
                  return None
            loggr.info(f'lists_by_dates:{lists_by_dates}')
            return lists_by_dates 
        except Exception as e:
            return JsonResponse({'status':'ERROR at common_facade.get_lists_by_dates()','details':str(e)}, status=500, safe=False)

    def get_glist_by_date(self, date):
      loggr.info('///MOVE TO common_facade.get_glist_by_date()')
      try:
          loggr.info(f'***get_glist_by_date-date:{date}')
          glist = api_instance_by_date(
              model = GuardingList,
              model_serializer = GuardinglistSerializer,
              obj_date = 'glist_date',
              date = date,
              )
          if glist == None:
                  loggr.info(f'GLIST == NONE')
                  return None
          loggr.info(f'GLIST BY DATE:{glist}')
          return glist
      except Exception as e:
          loggr.error(f'ERROR AT common_facade.get_glist_by_date():{e}') 
          return JsonResponse({'status':'ERROR AT common_facade.get_glist_by_date()','details':str(e)}, status=500, safe=False)
    
    def get_glist_by_id(self, glist_id):
      loggr.info('///MOVE TO common_facade.get_glist_by_id()')
      try:
          glist = api_get_glist_by_id(glist_id)
          if glist == None:
                  loggr.info(f'GLIST == NONE')
                  return None
          loggr.info(f'GLIST BY ID:{glist}')
          return glist
      except Exception as e:
          loggr.error(f'ERROR AT common_facade.get_glist_by_id():{e}') 
          return JsonResponse({'status':'ERROR AT common_facade.get_glist_by_id()','details':str(e)}, status=500, safe=False)
      
    def get_instance_by_date_position(self, date, position):
        loggr.info('///MOVE TO common_facade.get_instance_by_date_position()')
        try:
            instance = api_get_instance_by_date_position(
              position = position,
              date = date,
              )
            if instance == None:
                  loggr.info(f'INSTANCE == NONE')
                  return None
            loggr.info(f'INSTANCE BY DATE AND POSITION:{instance}')
            return instance
        except Exception as e:
          loggr.error(f'ERROR AT common_facade.get_instance_by_date_position():{e}') 
          return JsonResponse({'status':'ERROR AT common_facade.get_instance_by_date_position()','details':str(e)}, status=500, safe=False)
    
    def get_guarding_list(self, request):
        loggr.info('///MOVE TO common_facade.get_guarding_list()')
        try:
            guarding_list = api_get_list(instance_model=GuardingList, model_serializer=GuardinglistSerializer)
            if guarding_list == None:
                  loggr.info(f'GUARDING LIST == NONE')
                  return None
            loggr.info(f'GUARDING LIST:{guarding_list}')
            #family_id = get_family_id_from_glist(guarding_list)
            #guard_id = get_guard_by_family_id(Fguard, family_id)
            return guarding_list
        except Exception as e:
            loggr.error(f'ERROR AT common_facade.get_guarding_list():{e}') 
            return JsonResponse({'status':'ERROR at common_facade.get_guarding_list()','details':str(e)}, status=500, safe=False)
    
    def get_future_glists(self, request):
        loggr.info('///MOVE TO common_facade.get_future_glists()')
        try:
            future_glists = api_get_futu_lists()
            if future_glists == None:
                  loggr.info(f'FUTURE GUARDING LIST == NONE')
                  return None
            loggr.info(f'FUTURE GUARDING LIST:{future_glists}')
            return future_glists
        except Exception as e:
            loggr.error(f'ERROR AT common_facade.get_future_glists():{e}') 
            return JsonResponse({'status':'ERROR at common_facade.get_future_glists()','details':str(e)}, status=500, safe=False)

