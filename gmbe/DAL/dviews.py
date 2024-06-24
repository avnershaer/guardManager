from django.views import View
from loggers.loggers import logger, err_logger
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Max
from django.db.models import Q


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
                loggr.info(f'OK GOT GUARDING LISTS')
                return guarding_lists
            loggr.error('ERROR: GOT NO GUARDING LISTS')
            return None
        except Exception as e:
            raise e
        
    def get_instance_by_date(self, model, obj_date, date):
        loggr.info('///MOVE TO  dviews. get_instance_by_date()')
        try:
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
    
    def get_field_name_by_id(self, model, field_name, idd):
        loggr.info('///MOVE TO dviews.get_field_name_by_id()')
        try:
            filter_args = {field_name: idd}
            instances = model.objects.filter(**filter_args)
            if instances.exists():
                loggr.info(f'OK instances: {instances}')
                return instances
            loggr.info('No instances found.')
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
            if hasattr(model, 'user') and hasattr(User, 'is_active'):
                queryset = model.objects.filter(Q(user__is_active=True) | Q(user__isnull=True))
            else:
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

    def create_new(self, model, **kwarg):
        loggr.info('///MOVE TO dviews.creat_new()')
        try:
            instance = model.objects.create(**kwarg)
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
    
    def get_instance_by_parm(self, model, instance, parm):
        loggr.info('///MOVE TO dviews.get_shifts_by_date_pos()')
        try:
            kwargs = {instance: parm}
            query_instance = model.objects.filter(**kwargs)
            loggr.info(f'instance_by_parm:{query_instance}')
            return query_instance
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
    
    def exchange_guard(self, shift_id, guard_id, substitute_guard_id, ex_type):
        loggr.info('///MOVE TO dviews.exchange_guard()')
        try:
            shift_instance = Shift.objects.get(shift_id=shift_id.shift_id)
            if ex_type == 'paid': #check if fguard or paid guard and get instance
                substitute_guard = PaidGuards.objects.get(pguard_id=substitute_guard_id.pguard_id)
            elif ex_type == 'ordinary' or ex_type == 'cross':
                substitute_guard = Fguard.objects.get(fguard_id=substitute_guard_id.fguard_id)
            current_guard = shift_instance.fguard_id.filter(fguard_id=guard_id.fguard_id).first()
            if current_guard:
                shift_instance.fguard_id.remove(current_guard)
                loggr.info(f"Removed current guard: {current_guard}")
                if isinstance(substitute_guard, Fguard):
                    shift_instance.fguard_id.add(substitute_guard)
                elif isinstance(substitute_guard, PaidGuards):
                    shift_instance.pguard_id.add(substitute_guard)
                shift_instance.save()
                loggr.info(f'OK SAVED NEW REPLACED GUARD')
                if shift_instance:
                    loggr.info(f'OK SAVED NEW REPLACED GUARD')
                    return shift_instance
                return None
            return None
        except Exception as e:
            loggr.error(f"ERROR dviews.exchange_guard(): {str(e)}")
            return JsonResponse({'status': 'ERROR', 'Details': str(e)}, status=500)

    def get_instance_by_entity_id(self, model, instance, entity_id):
        loggr.info('///MOVE TO dviews.get_instance_by_entity_id()')
        try:
            kwargs = {instance: entity_id}
            fetched_instance = model.objects.get(**kwargs)
            if fetched_instance: 
                loggr.info(f'OK GOT INSTANCE at dviews.get_instance_by_entity_id()')
                return fetched_instance
            loggr.error("ERROR AT dviews.get_instance_by_entity_id() - fetch_instance NOT FOUND")
            return None
        except Exception as e:
            loggr.error(f"ERROR dviews.get_instance_by_entity_id(): {str(e)}")
            return JsonResponse({'status': 'ERROR', 'Details': str(e)}, status=500)

    def get_first_fguard_id_by_family_id(self, family_id, ex_type):
        loggr.info('///MOVE TO dviews.get_first_fguard_id_by_family_id()')
        try:
            if ex_type == 'ordinary' or ex_type == "cross":
                first_fguard = Fguard.objects.filter(family_id=family_id).order_by('fguard_id').first()
                if first_fguard:
                    return first_fguard.fguard_id
                return None
            elif ex_type =="paid":
                first_fguard = PaidGuards.objects.filter(family_id=family_id).order_by('pguard_id').first()
                if first_fguard:
                    return first_fguard.pguard_id
                return None
        except Exception as e:
            loggr.error(f"ERROR dviews.get_first_fguard_id_by_family_id(): {str(e)}")
            return JsonResponse({'status': 'ERROR', 'Details': str(e)}, status=500)
    
    def update(self, model, id, **kwargs):
        loggr.info('///MOVE TO dviews.update()')
        try:
            # Retrieve the instance
            instance = model.objects.get(pk=id)
    
            # Update the attributes on the instance
            for attr, value in kwargs.items():
                if attr == 'remove_pic' and value:
                    # Remove the picture
                    instance.fguard_pic.delete(save=False)
                    instance.fguard_pic = None  # or instance.fguard_pic = '' if you prefer
                else:
                    setattr(instance, attr, value)
    
            # Save the instance to trigger any save methods and signals
            instance.save()
    
            loggr.info(f'OK GOT updated instance')
            return instance
        except model.DoesNotExist:
            loggr.error(f'ERROR dviews.update(): Instance with id {id} not found')
            return JsonResponse({'status': 'ERROR', 'Details': f'Instance with id {id} not found'}, status=404)
        except Exception as e:
            loggr.error(f"ERROR dviews.update()(): {str(e)}")
            return JsonResponse({'status': 'ERROR', 'Details': str(e)}, status=500)