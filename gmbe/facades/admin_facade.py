from ..api.serislizers_views import api_get_list
from ..dal.models import *
from ..api.serializers import *
from ..api.serislizers_views import api_get_instances_by_parm, api_create_new, api_update_instance, api_get_fields_by_id
from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from ..utils.create_list_funcs import create_guarding_list, save_shift_details
from ..dal.dviews import Dal
from ..utils.operations_funcs import get_last_id, handle_exchange_guard
from ..utils.requests_data import fguard_data

dal = Dal()
loggr = logger()
errlogger = err_logger()


class AdminFacade():
    
    def get_all_families(self, request): #(request for @require_role)
        loggr.info('///MOVE TO admin_facade.get_all_families()')
        try:
            families_list = api_get_list(
                instance_model=Families, 
                model_serializer = FamiliesSerializer
                )
            loggr.info(f'families_list:{families_list}')
            return families_list
        except Exception as e:
            return JsonResponse(
                {'status':'ERROR at admin_facade.get_all_families','details':str(e)}, 
                status=500, 
                safe=False
                )
            
    def get_all_fguards(self, request):
        loggr.info('///MOVE TO admin_facade.get_all_fguards()')
        try:
            fguards_list = api_get_list(
                instance_model=Fguard, 
                model_serializer = FguardSerializer
                )
            loggr.info(f'families_list:{fguards_list}')
            return fguards_list
        except Exception as e:
            return JsonResponse(
                {'status':'ERROR at admin_facade.get_all_fguards','details':str(e)}, 
                status=500, 
                safe=False
                )
            
    def get_all_users(self, request):
        loggr.info('///MOVE TO admin_facade.get_all_users()')
        try:
            users_list = api_get_list(
                instance_model=User, 
                model_serializer=UserSerializer
                )
            return users_list
        except Exception as e:
            return JsonResponse(
                {'status':'ERROR at admin_facade.AdminFacade.get_all_users()','details':str(e)}, 
                status=500, 
                safe=False
                )
        
    def get_Positions_list(self, request):
        loggr.info('///MOVE TO admin_facade.get_Positions_list()')
        try:
            positions_list = api_get_list(
                instance_model=Position, 
                model_serializer=PositionSerializer
                )
            return positions_list
        except Exception as e:
            return JsonResponse(
                {'status':'ERROR at admin_facade.AdminFacade.get_positions_list()','details':str(e)}, 
                status=500, 
                safe=False
                )
        
    def get_paid_guards_list(self, request):
        loggr.info('///MOVE TO admin_facade.get_Positions_list()')
        try:
            paid_guards_list = api_get_list(
                instance_model=PaidGuards, 
                model_serializer=PaidGuardsSerializer
                )
            return paid_guards_list
        except Exception as e:
            return JsonResponse(
                {'status':'ERROR at AdminFacade.get_positions_list()','details':str(e)}, 
                status=500, 
                safe=
                False
                )
        
    def get_all_exchanges(self, request):
        loggr.info('///MOVE TO admin_facade.get_all_exchanges()')
        try:
            exchanges_list = api_get_list(instance_model=Exchanges, model_serializer=ExchangesSerializer)
            return exchanges_list
        except Exception as e:
            return JsonResponse({'status':'ERROR at AdminFacade.get_all_exchanges()','details':str(e)}, status=500, safe=False)
        
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
            last_fguard_id = Fguard.objects.get(fguard_id=glist_last_id)
            loggr.info(f'^^^^last_guard_id:{last_fguard_id}')
            last_guard_id = last_fguard_id.family_id.family_id
            loggr.info(f'^^^^last_family_id:{last_guard_id}')
            
            family_instance = Families.objects.get(family_id=last_guard_id)

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
            
            guarding_list = dal.create_new(
                GuardingList,
                last_guard_id = family_instance,  
                glist_position_id = glist_position_id,
                glist_date = glist_date,
                glist_day = glist_day 
                )
            if isinstance(guarding_list, JsonResponse):
                loggr.error(f'ERROR AT save_guarding_list():{guarding_list} ')
                return guarding_list
            guarding_list.shifts.set(glist_shifts)
            loggr.info(f'GUARDING LIST:{guarding_list}')
            return JsonResponse(
                {
                'status':'success', 
                'Details':'רשימת השמירה נשמרה', 
                'position':glist_position_name, 
                'date':glist_date
                }, 
                status=200, 
                safe=False
                )
        except Exception as e:
            loggr.error((f'ERROR at admin_facade.save_guarding_list:{e}'))
            return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)
        
    def reg_exchange_guard(self, request, ex_type):
        loggr.info('///MOVE TO admin_facade.reg_exchange_guard()')
        try:
            ex_data = request.data.get('selectedRow')
            substitute_guard = request.data.get('substituteGuard').get('family_id')
            exchange_result = handle_exchange_guard(ex_type, ex_data, substitute_guard)
            if exchange_result == None:
                return None
            return exchange_result
        except Exception as e:
            loggr.error((f'ERROR at admin_facade.reg_exchange_guard:{e}'))
            return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)
    
    def paid_exchange_guard(self, request, ex_type):
        loggr.info('///MOVE TO admin_facade.reg_exchange_guard()')
        try:
            ex_data = request.data.get('selectedRow')
            substitute_guard = request.data.get('substituteGuard').get('family_id')
            exchange_result = handle_exchange_guard(ex_type, ex_data, substitute_guard)
            if exchange_result == None:
                return None
            return exchange_result
        except Exception as e:
            loggr.error((f'ERROR at admin_facade.reg_exchange_guard:{e}'))
            return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)
    
    def cross_exchange_guard(self, request, ex_type):
        loggr.info('///MOVE TO admin_facade.cross_exchange_guard()')
        try:
            exchange_result = {'first':None, 'second':None}

            ex_data = request.data.get('selectedRow')
            substitute_guard = request.data.get('substituteGuard').get('guardId')

            first_exchange_result = handle_exchange_guard(ex_type, ex_data, substitute_guard)
            if first_exchange_result == None:
                return None
            exchange_result['first'] = first_exchange_result
            ex_data = request.data.get('substituteGuard')
            substitute_guard = request.data.get('selectedRow').get('guardId')
            second_exchange_result = handle_exchange_guard(ex_type, ex_data, substitute_guard)
            if second_exchange_result == None:
                return None
            exchange_result['second'] = second_exchange_result
            return exchange_result
        
        except Exception as e:
            loggr.error((f'ERROR at admin_facade.reg_exchange_guard:{e}'))
            return JsonResponse({'status':'error', 'details':e}, status=500, safe=False)

    def get_exchange_list_by_type(self, ex_type):
          loggr.info('///MOVE TO admin_facade.get_exchange_list_by_type()')
          try:
              exchange_list_by_type = api_get_instances_by_parm(
                  model = Exchanges, 
                  instance = 'exchange_type', 
                  parm = ex_type,
                  model_serializer = ExchangesSerializer
                  )
              if exchange_list_by_type == None:
                      loggr.info(f'Exchange List By Type == NONE')
                      return None
              return exchange_list_by_type
          except Exception as e:
              loggr.error(f'ERROR AT admin_facade.get_exchange_list_by_type():{e}') 
              return JsonResponse(
                  {'status':'ERROR AT admin_facade.get_exchange_list_by_type()','details':str(e)}, 
                  status=500, 
                  safe=False
                  )
    
    def create_position(self, request):
        loggr.info('///MOVE TO admin_facade.create_position()')
        try:
            position_name = request.data.get('positionName')
            data = {'position_name': position_name}
            new_position = api_create_new(
                model = Position,
                model_serializer = PositionSerializer, 
                data = data
            )
            if isinstance(new_position, JsonResponse):
                return new_position
            return new_position
        except Exception as e:
              loggr.error(f'ERROR AT admin_facade.create_position():{e}') 
              return JsonResponse(
                  {'status':'ERROR AT admin_facade.create_position()','details':str(e)}, 
                  status=500, 
                  safe=False
                  )
        
    def update_fguard(self, request):
        loggr.info(f'///MOVE TO admin_facade.update_fguard() request:{request.FILES}')
        try:
            data = fguard_data(request)
            id = data['fguard_id']
            updated_fguard = api_update_instance(
                validated_data=data, 
                id=id, 
                instance_model=Fguard, 
                model_serializer=FguardSerializer,
                )
            return updated_fguard
        except Exception as e:
          loggr.error(f'ERROR AT admin_facade.update_fguard():{e}') 
          return JsonResponse(
              {'status':'ERROR AT admin_facade.update_fguard()','details':str(e)}, 
              status=500, 
              safe=False
              )
        
    def get_shifts_for_fguard(self, request, fguard_id):
        loggr.info('///MOVE TO admin_facade.get_fguard_by_fguard_id()')
        try:
            fguard = api_get_fields_by_id(
                Shift,
                ShiftSerializer,
                'fguard_id',
                fguard_id
            )
            return fguard
        except Exception as e:
            loggr.error(f'ERROR AT admin_facade.get_fguard_by_fguard_id():{e}')
            raise e
    
    def get_exchanges_for_fguard(self, request, fguard_id):
        loggr.info('///MOVE TO admin_facade.get_fguard_by_fguard_id()')
        try:
            fguard = api_get_instances_by_parm(
                Exchanges,
                'origin_guard_id',
                fguard_id,
                ExchangesSerializer,
            )
            return fguard
        except Exception as e:
            loggr.error(f'ERROR AT admin_facade.get_fguard_by_fguard_id():{e}')
            raise e
    
    def get_did_exchanges_for_fguard(self, request, fguard_id):
        loggr.info('///MOVE TO admin_facade.get_fguard_by_fguard_id()')
        try:
            fguard = api_get_instances_by_parm(
                Exchanges,
                'substitute_fguard_id',
                fguard_id,
                ExchangesSerializer,
            )
            return fguard
        except Exception as e:
            loggr.error(f'ERROR AT admin_facade.get_fguard_by_fguard_id():{e}')
            raise e
