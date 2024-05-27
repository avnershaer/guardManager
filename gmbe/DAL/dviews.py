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
        loggr.info('///MOVE TO dal.dalviws.table_object_list()')
        try:
            table_list = model.objects.all()
            if table_list:
                return table_list
            return None  
        except Exception as e:
            return JsonResponse({'status':'error', 'details':str(e)}, status=500, safe=False)

        
    def get_lists_by_dates(self, model, date1, date2):
        loggr.info("///MOVE TO DAL.get_lists_by_dates()")
        try:
            guarding_lists = model.objects.filter(glist_date__range=(date1, date2))
            if guarding_lists:
                loggr.info(f'OK GOT GUARDING LISTS:{guarding_lists}')
                return guarding_lists
            loggr.error('ERROR: GOT NO GUARDING LISTS')
            return None
        except Exception as e:
            raise e
        
    def get_instance_by_date(self, model, obj_date, date):
        loggr.info('///MOVE TO  dviews. get_instance_by_date()')
        try:
            loggr.info(f'***obj_date:{obj_date}, ***date:{date}')
            instance = model.objects.filter(**{obj_date:date})
            if instance:
                loggr.info(f'instance: {instance}')
                return instance
            return None
        except Exception as e:
            return JsonResponse({'status':'error', 'details':str(e)})
    
    def get_glist_by_id(self, glist_id):
        loggr.info('///MOVE TO  dviews. get_instance_by_date()')
        try:
            instance = GuardingList.objects.filter(guarding_list_id=glist_id)
            if instance:
                loggr.info(f'instance: {instance}')
                return instance
            return None
        except Exception as e:
            return JsonResponse({'status':'error', 'details':str(e)})

    def get_instance_by_date_position(self, date, position):
        loggr.info('///MOVE TO dal.dalviws.get_instance_by_date_position()')
        try:
            instance = GuardingList.objects.filter(glist_date=date, glist_position_id=position)
            if instance:
                return instance
            return None
        except Exception as e:
            return JsonResponse({'status':'error', 'details':str(e)})

    def set_table_object_list(self, model, num_objects, starting_id):
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
        loggr.info('///MOVE TO dviews.creat_new()')
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
        loggr.info('///MOVE TO dviews.get_shifts_by_date_pos()')
        try:
            shifts = Shift.objects.filter(shift_date=date, position_id=position_id)
            loggr.info(f'dviews shifts:{shifts}')
            return shifts
        except Exception as e:
            loggr.error(f'ERROR at dviews.get_shifts_by_date_pos(): FAILD TO GET SHIFTS:{e}')
            return JsonResponse({'status': 'error', 'details':'dviews.get_shifts_by_date_pos()-faild to get shifts'}) 

    # get the last id for creating new guard list
    def get_last_id(self):
        loggr.info('///MOVE TO dviews.get_last_id()')
        try:
            # Query the GuardingList model ordered by guarding_list_id in descending order
            last_guard_list_instance = GuardingList.objects.order_by('-guarding_list_id').first()
            # Retrieve the last_guard_id from the last_guard_list_instance
            last_guard_id = last_guard_list_instance.last_guard_id.family_id
            return last_guard_id
        except Exception as e:
            return JsonResponse({'status':'ERROR dviews.Dal.get_last_id()','Details':str(e)}, status=500, safe=False)
        
    def get_future_lists(self):
        loggr.info('///MOVE TO dviews.get_future_lists()')
        try:
            today = timezone.now().date()
            futu_lists = GuardingList.objects.filter(glist_date__gte=today).order_by('glist_date')
            if futu_lists:
                return futu_lists
            return None
        except Exception as e:
            return JsonResponse({'status':'ERROR dviews.Dal.get_future_lists()','Details':str(e)}, status=500, safe=False)
    
    def exchange_guard(self, shift_id, guard_id, substitute_guard_id):
        loggr.info('///MOVE TO dviews.exchange_guard()')
        try:
            loggr.info(f"SHIFT_ID: {shift_id}")

            shift_instance = Shift.objects.get(shift_id=int(shift_id))
            loggr.info(f"Shift instance retrieved: {shift_instance}")
            substitute_guard = Families.objects.get(family_id=substitute_guard_id)
            loggr.info(f"Substitute guard retrieved: {substitute_guard}")
            current_guard = shift_instance.family_id.filter(family_id=guard_id).first()
            if current_guard:
                shift_instance.family_id.remove(current_guard)
                loggr.info(f"Removed current guard: {current_guard}")
                shift_instance.family_id.add(substitute_guard)
                shift_instance.save()
                loggr.info(f'OK SAVED NEW REPLACED GUARD -- SHIFT INSTANCE: {shift_instance}')
                if shift_instance:
                    loggr.info(f'OK SAVED NEW REPLACED GUARD -- SHIFT INSTANCE: {shift_instance}')
                    return shift_instance
                return None
            return None
        except Exception as e:
            loggr.error(f"ERROR dviews.exchange_guard(): {str(e)}")
            return JsonResponse({'status': 'ERROR', 'Details': str(e)}, status=500)












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

