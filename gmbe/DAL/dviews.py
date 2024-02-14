from django.views import View
from loggers.loggers import logger, err_logger
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse


loggr = logger()
errlogger = err_logger()


class Dal(View):
    
    model = None # to reset the model attr

    # get list of model objects from database 
    def table_objects_list(self, model):
        loggr.info('OK ------------got test 4')

        try:
            # get the list 
            table_list = model.objects.all()
            if table_list:
                loggr.info('OK got object/s from db HTTP/1.1 200 - dalviews.Dal.table_objects_list')
                return table_list
            
            
            # if error  
            loggr.info('OK ------------got test 5')
            errlogger.error('DATABASE ERROR..OBJ NOT FOUND HTTP/1.1 400  at  dviews.Dal.table_objects_list')
            return JsonResponse({'status': 'DATABASE ERROR..OBJ NOT FOUND HTTP/1.1 400'}, status=400, safe=False) 
        
        # handle any exceptions that occur during processing this method
        except Exception as e:
            errlogger(f'ERROR HTTP/1.1 500 at dviews.Dal.table_objects_list:{e}')
            return JsonResponse({'status:':'ERROR dviews.Dal.table_objects_list','details:':str(e)}, status=500, safe=False)
