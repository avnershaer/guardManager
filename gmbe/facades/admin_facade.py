from ..api.serislizers_views import api_get_list
from ..dal.models import *
from ..api.serializers import *
from ..api.serislizers_views import api_instance_by_date, api_create_new
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from ..utils.create_list_funcs import create_guarding_list, save_shift_details
from ..dal.dviews import Dal
from ..utils.operations_funcs import get_last_id
from ..utils.requests_data import exchange_request_data


dal = Dal()
loggr = logger()
errlogger = err_logger()


class AdminFacade():#(AnonymousFacade)
    
    def get_all_families(self, request): #(request for @require_role)
        loggr.info('///MOVE TO admin_facade.get_all_families()')
        try:
            # get list of all families
            families_list = api_get_list(instance_model=Families, model_serializer = FamiliesSerializer)
            loggr.info(f'families_list:{families_list}')
            # success reponse with list of families.  
            return families_list
        # handle any exceptions that occur during getting the list 
        except Exception as e:
            return JsonResponse({'status':'ERROR at admin_facade.AdminFacade.get_all_families','details':str(e)}, status=500, safe=False)
            
    def get_all_users(self, request):
        loggr.info('///MOVE TO admin_facade.get_all_users()')
        try:
            users_list = api_get_list(instance_model=User, model_serializer=UserSerializer)
            return users_list
        except Exception as e:
            return JsonResponse({'status':'ERROR at admin_facade.AdminFacade.get_all_users()','details':str(e)}, status=500, safe=False)
        
    def get_Positions_list(self, request):
        loggr.info('///MOVE TO admin_facade.get_Positions_list()')
        try:
            positions_list = api_get_list(instance_model=Position, model_serializer=PositionSerializer)
            return positions_list
        except Exception as e:
            return JsonResponse({'status':'ERROR at admin_facade.AdminFacade.get_positions_list()','details':str(e)}, status=500, safe=False)
        
    def get_shifts_list(self, request):
        loggr.info('///MOVE TO admin_facade.get_shifts_list()')
        try:
            shifts_list = api_get_list(instance_model=Shift, model_serializer=ShiftSerializer)
            return shifts_list
        except Exception as e:
            return JsonResponse({'status':'ERROR at admin_facade.AdminFacade.get_shifts_list()','details':str(e)}, status=500, safe=False)

    def create_guard_list(self, request):
        loggr.info('///MOVE TO admin_facade.create_guard_list()')
        try:
            guard_list = create_guarding_list(request)
            loggr.info(f'guard list BEEN CREATED - admin_facade.create_guard_list()')
            return guard_list
        except Exception as e:
            return JsonResponse({'status':'ERROR at admin_facade.AdminFacade.create_guard_list()', 'details':str(e)}, status=500, safe=False)

    def save_guarding_list(self, request):
        loggr.info('///MOVE TO admin_facade.save_guarding_list()')
        try:
            loggr.info(f'^^^^REQUEST:{request.data}')

            shifts = request.data.get('shifts')
            loggr.info(f'^^^^SHIFTS:{shifts}')
            save_shift_details(request, shifts)
            
            glist_last_id = get_last_id()
            loggr.info(f'^^^^glist_last_id:{glist_last_id}')
            last_guard_id = Families.objects.get(family_id=glist_last_id)
            loggr.info(f'^^^^last_guard_id:{last_guard_id}')

            glist_position_id = request.data.get('shifts').get('1').get('position_id').get('position_id')
            glist_position_name = request.data.get('shifts').get('1').get('position_id').get('position_name')
            glist_position_id = Position.objects.get(position_id=glist_position_id)
            loggr.info(f'^^^^glist_position_id:{glist_position_id}')
            loggr.info(f'^^^^glist_position_name:{glist_position_name}')

            glist_date = request.data.get('list_date')
            loggr.info(f'^^^^glist_date:{glist_date}')

            glist_day = request.data.get('list_day')
            loggr.info(f'^^^^glist_day:{glist_day}')
            glist_shifts = dal.get_shifts_by_date_pos(glist_date, glist_position_id)
            loggr.info(f'^^^^glist_shifts:{glist_shifts}')
            
            guarding_list = dal.creat_new(
                GuardingList,
                last_guard_id = last_guard_id,  
                glist_position_id = glist_position_id,
                glist_date = glist_date,
                glist_day = glist_day 
                )
            if isinstance(guarding_list, JsonResponse):
                loggr.error(f'ERROR AT save_guarding_list():{guarding_list} ')
                return guarding_list
            guarding_list.shifts.set(glist_shifts)
            loggr.info(f'GUARDING LIST:{guarding_list}')
            return JsonResponse({'status':'success', 'Details':'רשימת השמירה נשמרה', 'position':glist_position_name, 'date':glist_date}, status=200, safe=False)

        except Exception as e:
            loggr.error((f'ERROR at admin_facade.save_guarding_list:{e}'))
            return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)
        
    def reg_exchange_guard(self, request):
        loggr.info('///MOVE TO admin_facade.reg_exchange_guard()')
        ex_type = 'ordinary'
        request_data = exchange_request_data(request, ex_type)
        if isinstance(request_data, JsonResponse):
            return request_data
        reg_exchange = dal.exchange_guard(request_data['shift_id'], request_data['origin_guard_id'], request_data['substitute_guard_id'])
        if reg_exchange:
            loggr.info('OK_EXCHANGE')
            write_exchange = api_create_new(Exchanges, ExchangesSerializer, request_data)
            if write_exchange:
                loggr.info(f'OK_write_exchange: {write_exchange}')
                return write_exchange
        loggr.info('write_exchange: none')  
        return None

