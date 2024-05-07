from django.views import View
from loggers.loggers import logger, err_logger
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Max


loggr = logger()
errlogger = err_logger()


class Dal(View):
    
    model = None # to reset the model attr

    # get list of model objects from database 
    def table_objects_list(self, model):
        loggr.info('got to dal.dalviws.table_object_list()')
        try:
            # get the list 
            table_list = model.objects.all()
            if table_list:
                loggr.info('OK got object/s from db HTTP/1.1 200 - dalviews.Dal.table_objects_list')
                return table_list
            # if error  
            errlogger.error('DATABASE ERROR..OBJ NOT FOUND HTTP/1.1 400  at  dviews.Dal.table_objects_list')
            return JsonResponse({'status': 'DATABASE ERROR..OBJ NOT FOUND HTTP/1.1 400'}, status=400, safe=False) 
        
        # handle any exceptions that occur during processing this method
        except Exception as e:
            errlogger.error(f'ERROR HTTP/1.1 500 at dviews.Dal.table_objects_list:{e}')
            return JsonResponse({'status:':'ERROR dviews.Dal.table_objects_list','details:':str(e)}, status=500, safe=False)

    def set_table_object_list(self, model, num_objects, starting_id):
        loggr.info('got to dal.dalviws.set_table_object_list()')
        loggr.info(f'*******starting_id: {starting_id}')

        try:
            id_list = []
            queryset = model.objects.all()
            loggr.info(f'*******queryset: {queryset}')
            second_queryset = queryset[starting_id-1:]
            loggr.info(f'*******second_queryset: {second_queryset}')
            third_queryset = second_queryset[:num_objects]
            loggr.info(f'*******third_queryset: {third_queryset}')
            id_list= list(third_queryset)
            loggr.info(f'*******id_list: {id_list}')
            a = len(id_list)
            loggr.info(f'a = {a} ---num_objects = {int(num_objects)} ')
            while len(id_list) < num_objects:
                b = num_objects - a
                loggr.info(f'b = {b} ') 
                queryset = queryset[:b]
                loggr.info(f'*******last queryset: {queryset}')
                for i in queryset:
                    id_list.append(i)
                
            #table_list = list(queryset)
            loggr.info(f'*******LAST id_list: {id_list}')
            if id_list:
                loggr.info(f'OK got object/s from db HTTP/1.1 200 - dalviews.Dal.set_table_objects_list()--tabl_list:{id_list}')
                return id_list
            else:
                errlogger.error('DATABASE ERROR..OBJ NOT FOUND HTTP/1.1 400  at  dviews.Dal.set_table_objects_list()')
                return JsonResponse({'status': 'DATABASE ERROR..OBJ NOT FOUND HTTP/1.1 400'}, status=400, safe=False) 

        except Exception as e:
            errlogger.error(f'ERROR HTTP/1.1 500 at dviews.Dal.set_table_objects_list:{e}')
            return JsonResponse({'status':'ERROR dviews.Dal.set_table_objects_list','Details':str(e)}, status=500, safe=False)

    def creat_new(self, model, **kwargs):
        loggr.info('move to dviews.creat_new()')
        try:
            instance = model.objects.create(**kwargs)
            if instance:
                loggr.info('SUCCESS CREATING NEW INSTACE')
                return instance
            loggr.error(f'ERROR AT DAL.creat_new(): FAILD TO CREATE NEW INSTACE')
            return JsonResponse({'status': 'error', 'Details':'שגיאה. לא נשמר.'})
        except Exception as e:
            loggr.error(f'ERROR: FAILD TO CREATE NEW INSTACE:{e}')
            return JsonResponse({'status': 'error', 'Details':f'--שגיאה-- {e}'})
    

    def get_shifts_by_date_pos(self, date, position_id):
        loggr.info('move to dviews.get_shifts_by_date_pos()')
        try:
            shifts = Shift.objects.filter(shift_date=date, position_id=position_id)
            loggr.info(f'dviews shifts:{shifts}')
            return shifts
        except Exception as e:
            loggr.error(f'ERROR at dviews.get_shifts_by_date_pos(): FAILD TO GET SHIFTS:{e}')
            return JsonResponse({'status': 'error', 'details':'dviews.get_shifts_by_date_pos()-faild to get shifts'}) 


    def get_instance_by_date(self, model, obj_date, date):
        loggr.info('///MOVE TO  dviews. get_instance_by_date()')
        try:
            loggr.info(f'***obj_date:{obj_date}, ***date:{date}')
            instance = model.objects.filter(**{obj_date:date})
            loggr.info(f'instance: {instance}')
            return instance
        except Exception as e:
            return JsonResponse({'status':'error', 'details':str(e)})

    # get the last id for creating new guard list
    def get_last_id(self):
        try:
            loggr.info('///MOVE TO dviews.get_last_id()')
            # maximum date and hour
            latest_shift = Shift.objects.aggregate(
                max_date=Max('shift_date'),
                max_hour=Max('shift_hour'),
            )
            # last shift
            last_shift = Shift.objects.filter(
                shift_date=latest_shift['max_date'],
                shift_hour=latest_shift['max_hour']
            ).last()
            loggr.info(f'LAST SHIFT:{str(last_shift)}')
            # family_id from the last shift
            if last_shift:
                last_family_ids = last_shift.family_id.all()
                if last_family_ids:
                    last_family_id = last_family_ids.last().family_id
                    loggr.info(f'LAST FAMILY ID: {last_family_id}')
                    return last_family_id
            else:
                return JsonResponse({'ststus':'error', 'details':'No shifts found.'}, status=400, safe=False)
        except Exception as e:
            return JsonResponse({'status':'ERROR dviews.Dal.get_last_id()','Details':str(e)}, status=500, safe=False)















    #def get_shift_ids_by_date(self, shift_date):
    #    loggr.info('got to dal.get_shift_ids_by_date()')
    #    try:
    #        shift_details_list = ShiftDetails.objects.filter(shift_date=shift_date)
    #        loggr.info(f'shift_details_list:{shift_details_list}')
    #        shift_ids = []
    #        for shift_details in shift_details_list:
    #            shifts = Shift.objects.filter(shift_details_id=shift_details)
    #            shift_ids.extend(shift.id for shift in shifts)
    #        loggr.info(f'shift_ids:{shift_ids}')
    #        return shift_ids
    #    except Exception as e:
    #        loggr.error(f'ERROR: FAILED TO GET SHIFT IDS: {e}')
    #        return []

