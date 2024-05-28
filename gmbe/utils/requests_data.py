from loggers.loggers import logger, err_logger
from django.http import JsonResponse
from ..dal.models import Position, Families, Shift

loggr = logger()
errlogger = err_logger()

def exchange_request_data(request, ex_type):
    loggr.info('///MOVE TO requests_data.requests_data()')
    try:
        gaurd_id = request.data.get('selectedRow').get('guardId')
        shift_id = request.data.get('selectedRow').get('shiftId')
        substitute_guard_id = request.data.get('substituteGuard').get('family_id')
        position_id = request.data.get('selectedRow').get('posId')
        list_date = request.data.get('selectedRow').get('glistDate')
        list_day = request.data.get('selectedRow').get('glistDay')
        shift_hour = request.data.get('selectedRow').get('shiftHour')

         # fetch required instances
        position_instance = Position.objects.get(position_id = position_id)
        origin_guard_instance = Families.objects.get(family_id = gaurd_id)
        substitute_guard_instance = Families.objects.get(family_id = substitute_guard_id)
        shift_instance = Shift.objects.get(shift_id=shift_id)

        
        exchange_data = {
            'origin_guard_id': origin_guard_instance,
            'shift_id': shift_instance,
            'substitute_guard_id': substitute_guard_instance,
            'position_id': position_instance,
            'exchange_date': list_date,
            'exchange_day': list_day,
            'exchange_hour': shift_hour,
            'exchange_type': ex_type,
        }

        return exchange_data
    
    except Exception as e:
        return JsonResponse({'status':'error', 'details':e}, status=500, save=False)

