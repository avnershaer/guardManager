from django.views import View
from loggers.loggers import logger, err_logger
from .models import *
from django.utils import timezone
from datetime import timedelta

logr = logger()
errlogger = err_logger()


class Dal(View):
    
    model = None # resets the model attr

    # get list of model objects from database 
    def table_objects_list(self, model):
        
        try:
            # get the list 
            table_list = model.objects.all()
            
            # success respose with list details
            if table_list:
                return table_list
            
            # error response 
            return errlogger('DATABASE ERROR..OBJ NOT FOUND..model: dal.dviews')
        
        # handle any exceptions that occur during processing this method
        except Exception as e:
            return errlogger(f'DATABASE ERROR..OBJ NOT FOUND..model: DAL..DETAILS:{e}')