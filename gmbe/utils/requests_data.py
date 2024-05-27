from loggers.loggers import logger, err_logger
from django.http import JsonResponse


loggr = logger()
errlogger = err_logger()

def exchange_request_data(request):
    loggr.info('///MOVE TO requests_data.requests_data()')
    try:
        gaurd_id = request.data.get('selectedRow').get('guardId')
        loggr.info(f"GUARD ID: {gaurd_id}")
        shift_id = request.data.get('selectedRow').get('shiftId')
        loggr.info(f"SHIFT ID: {shift_id}")
        substitute_guard_id = request.data.get('substituteGuard').get('family_id')
        loggr.info(f"SUBSTITUTE_GUARD_ID: {substitute_guard_id}")
        return {
            'guard_id': gaurd_id,
            'shift_id': shift_id,
            'substitute_guard_id': substitute_guard_id,
        }
    except Exception as e:
        return JsonResponse({'status':'error', 'details':e}, status=500, save=False)

