from loggers.loggers import logger, err_logger
from ..api.serislizers_views import api_get_lists_by_dates
from django.http import JsonResponse
from ..dal.models import GuardingList
from ..api.serializers import GuardinglistSerializer


loggr = logger()
errlogger = err_logger()


class CommonFacade():

    def get_lists_by_dates(self, date1, date2):
        loggr.info('///MOVE TO CommonFacade.get_lists_by_dates()') 
        try:
            lists_by_dates = api_get_lists_by_dates(
                model = GuardingList,
                model_serializer = GuardinglistSerializer,
                date1 = date1,
                date2 = date2
                )
            if lists_by_dates == None:
                  loggr.info(f'lists_by_dates:NONE')
                  return None
            loggr.info(f'lists_by_dates:{lists_by_dates}')
            return lists_by_dates 
        except Exception as e:
            return JsonResponse({'status':'ERROR at admin_facade.AdminFacade.get_all_families','details':str(e)}, status=500, safe=False)
            