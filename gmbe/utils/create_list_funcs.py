from django.http import JsonResponse
from loggers.loggers import logger, err_logger
from ..dal.dviews import Dal
from ..utils.operations_funcs import serialize_data 
from ..dal.models import GuardingList, Families, SetGuardingList, Position, Shift
from ..api.serializers import GuardinglistSerializer, SetGuardingListSerializer, FamiliesSerializer, PositionSerializer
from datetime import time, timedelta, datetime
from ..api.serislizers_views import api_get_list
import json

loggr = logger()
errlogger = err_logger()
dal = Dal()

def guarding_list_data(request):
    loggr.info(f'got to utils.guarding_list_data()')
    try:
        date = request.data.get('date')
        loggr.info(f'DATE:{date}')
        day = request.data.get('day')
        loggr.info(f'DAY:{day}')
        position_id = request.data.get('glistData').get('position_id')
        loggr.info(f'POSITION ID:{position_id}')
        num_of_gards = request.data.get('glistData').get('num_of_gards')
        loggr.info(f'NUM OF GUARDS:{num_of_gards}')
        hours_per_shift = request.data.get('glistData').get('hours_per_shift')
        hours_per_shift = int(hours_per_shift)
        loggr.info(f'HOURS PER SHIFT:{hours_per_shift}')
        daily_guard_hours = request.data.get('glistData').get('daily_guard_hours')
        daily_guard_hours = int(daily_guard_hours)
        loggr.info(f'DAILY GUARD HOURS:{daily_guard_hours}')
        gaurd_start_time = request.data.get('glistData').get('start_gaurd_hour')
        loggr.info(f'GUARD START TIME:{gaurd_start_time}')
        model = request.data.get('glistData').get('model')
        loggr.info(f'MODEL:{model}')
        starting_user_id = request.data.get('glistData').get('starting_user_id')
        loggr.info(f'STARTING USER ID:{starting_user_id}')
        position = Position.objects.get(position_id=position_id)
        serialized_position = PositionSerializer(position).data
        loggr.info(f'POSITION:{position}')
        loggr.info(f'POSITION_id:{position_id}')
        loggr.info(f'SERIALZE_POSITION:{serialized_position}')
        return {
            'date': date,
            'day': day,
            'position_id': position_id,
            'num_of_gards': num_of_gards,
            'hours_per_shift': hours_per_shift,
            'daily_guard_hours': daily_guard_hours,
            'gaurd_start_time': gaurd_start_time,
            'model': model,
            'starting_user_id': starting_user_id,
            'serialized_position': serialized_position
        }
    except Exception as e:
       loggr.error(f'ERROR---create_list_funcs.guarding_list_data(): {e}')
       return JsonResponse({'status:': 'ERROR----create_list_funcs.guarding_list_data()', 'details:': str(e)}, status=500, safe=False)



def create_guarding_list(request):
    loggr.info(f'got to utils.create_guarding_list()')
    english_to_hebrew_days = {
    'Monday': 'יום שני',
    'Tuesday': 'יום שלישי',
    'Wednesday': 'יום רביעי',
    'Thursday': 'יום חמישי',
    'Friday': 'יום שישי',
    'Saturday': 'יום שבת',
    'Sunday': 'יום ראשון'
    }
    glist_data = guarding_list_data(request)
    glist_date = datetime.strptime(glist_data['date'], '%Y-%m-%d')  # convert date in string to datetime object
    glist_day = english_to_hebrew_days[glist_date.strftime('%A')]  # Get the Hebrew name of the day from the initial glist_date
    glist_starting_user_id = glist_data['starting_user_id']
    days_of_lists = int(request.data.get('numOfLists'))
    glist = []
    try:
        for _ in range(days_of_lists):
            shifts_dict = create_shifts_dict(
                glist_data['hours_per_shift'], 
                glist_starting_user_id, 
                glist_data['num_of_gards'], 
                glist_data['daily_guard_hours'], 
                glist_data['gaurd_start_time'],
                glist_data['position_id']
            )
            gurading_list = {
                'position_id': glist_data['serialized_position'],
                'list_date': glist_date.strftime('%Y-%m-%d'),  # convert datetime object back to string
                'list_day':glist_day,
                'shifts':shifts_dict
                }
            glist_date += timedelta(days=1)  # Increase date by one day
            glist_day = english_to_hebrew_days[glist_date.strftime('%A')]  # Update glist_day to the new day name in Hebrew
            serialize_data = SetGuardingListSerializer(data=gurading_list)
            if serialize_data.is_valid():
                serialized_data = serialize_data.data
                loggr.info(f'GUARDING LIST BEEN SERIALIZED')
                glist.append(serialized_data)
            else:
                errors = serialize_data.errors
                loggr.error(f'ERROR---create_list_funcs.create_guarding_list(): {errors}')
                return JsonResponse({'status': 'ERROR----create_list_funcs.create_guarding_list()', 'details': errors}, status=400)
        return glist
    
    except Exception as e:
        loggr.error(f'ERROR---create_list_funcs.create_guarding_list(): {e}')
        return JsonResponse({'status:': 'ERROR----create_list_funcs.create_guarding_list()', 'details:': str(e)}, status=500, safe=False)

# create hours list by the shift hours
def hourslist(hours_per_shift, guarding_hours, start_hour):
    
    shift_hours = guarding_hours / hours_per_shift
    hours_list = []

    for i in range (int(shift_hours)):
        hour = i * hours_per_shift
        hours_list.append('{start_hour}:00'.format(hour))

    loggr.info(f'hours list: {hours_list}')
    return hours_list

# create user id list from a given model maches to a given shift hours    
def id_list( num_of_shifts, num_of_gards, starting_user_id,model):
    loggr.info('got to create_list_funcs.id_list()')
    try:
        model_list = dal.table_objects_list(model=model)
        if isinstance(model_list, JsonResponse):
            errlogger.error('problem with getting the id_list at create_list_funcs.id_list()')
            return model_list
        loggr.info(f'got model_list at create_list_funcs.id_list():{model_list} ')
        id_list = []

        # Find the starting index in model_list
        start_index = 0
        for index, obj in enumerate(model_list):
            if obj.id == starting_user_id:
                start_index = index
                break
        loggr.info(f'start index:{obj.id} --index:{index}-- at create_list_funcs.id_list()')
        # Loop through num_of_shifts * num_of_guards times
        for i in range(num_of_shifts * num_of_gards):
            # Get the index considering looping back to the beginning if needed
            index = (start_index + i) % len(model_list)
            id_list.append(model_list[index].id)
        loggr.info(f'got id_list at create_list_funcs.id_list():{id_list} ')
        return id_list

    except Exception as e:
        return JsonResponse({'status:': 'ERROR----create_list_funcs.id_list()', 'details': str(e)}, status=500, safe=False) 


# create a shift dict for guarding list
def create_shifts_dict(hours_per_shift, starting_user_id, num_of_gards, daily_guard_hours, gaurd_start_time, position_id):
    loggr.info('got to create_list_funcs.create_shifts_dict()')
    # total number of shifts
    num_of_shifts = int(daily_guard_hours / int(hours_per_shift))
    loggr.info(f'num of shifts:{num_of_shifts}')
    # hour for shift
    gaurd_start_datetime = datetime.strptime(gaurd_start_time, "%H:%M")
    hour = datetime(1900, 1, 1, gaurd_start_datetime.hour, gaurd_start_datetime.minute)  
    loggr.info(f'HOUR:{hour}')
    #datetime(1900, 1, 1, 0, 0)  # for 00:00
    num_objects=int(num_of_shifts) * int(num_of_gards)
    loggr.info(f'num_objects:{num_objects}')
    model=Families
    guards_list = dal.set_table_object_list(model, num_objects, starting_id=int(starting_user_id) )
    if isinstance(guards_list, JsonResponse):
            errlogger.error(f'error got no id list:{guards_list}')
            return guards_list
    loggr.info(f'got guards_list at create_list_funcs.create_shifts_dict()--{guards_list}  ')
    shifts = {}

    # Loop through each shift hour
    for shift in range(num_of_shifts):
        shift_hour = hour# hour for shift
        position = Position.objects.get(position_id=position_id)
        serialized_position = PositionSerializer(position).data

        shift_dict = {
            'shift_num': shift + 1, 
            'shift_hour': shift_hour.strftime("%H:%M"), 
            'guards': [],              # hour format^
            'position_id':serialized_position
            }
                                                                        
        hour = hour + timedelta(hours=int(hours_per_shift))  # hour for shift
        
   
   
        # Generate IDs for guards for this shift
        for guard_num in range(int(num_of_gards)):
            # Check if there are still guards available
            if guards_list:
                guard_id = guards_list.pop(0)  # remove and get the first id from id_list
                loggr.info(f'<><><>guard id{guard_id}')
                serialized_guard = FamiliesSerializer(guard_id).data
                shift_dict['guards'].append(serialized_guard) # appending the guard/s to shift dict on ['guards']
                

            else:
                loggr.error("No more guards available!")
                # Handle the error accordingly, either by breaking out of the loop or returning an error response
                # For example:
                # return JsonResponse({'error': 'No more guards available!'}, status=500)
        shifts[shift + 1] = shift_dict 
    loggr.info(f'SHIFT DICT HOURS : {shift_dict} ')  
    loggr.info(f'shift_dict guards been set to shift dict. SHIFT LIST: {shifts}')
    return shifts
        
def save_shift_details(request, shifts):
    loggr.info('<>OK move to create_list_funcs.save_shift_details()')
    try:
        shift_num = 0
        for i in shifts:
            shift_num = shift_num +1
            str_shift_num = str(shift_num)
            shift_hour = shifts[i]['shift_hour']
            loggr.info(f'------shift_hour:{shift_hour}')
            shift_date = request.data.get('list_date')
            loggr.info(f'------shift_date:{shift_date}')
            shift_day = request.data.get('list_day')
            loggr.info(f'------shift_day:{shift_day}')
            
            position_id = request.data.get('shifts').get(str_shift_num).get('position_id')
            loggr.info(f'------position_id:{position_id}')
            #get the position instance
            position_id = Position.objects.get(position_id=position_id['position_id'])

            # gets the family id via guards dict
            guards = request.data.get('shifts').get(str_shift_num).get('guards')
            loggr.info(f'------guards:{guards}')
            
            
            shift = dal.creat_new(
                model=Shift, 
                position_id=position_id, 
                shift_hour=shift_hour, 
                shift_date=shift_date, 
                shift_day=shift_day, 
            )
            for guard in guards:
                family_id = guard['family_id']
                loggr.info(f'------family_id:{family_id}')
                
                # get family instance and add it to the shift
                family_instance = Families.objects.get(pk=family_id)
                shift.family_id.add(family_instance)
                # add family instance shift's family_id ManyToManyField
                
            
            loggr.info(f'------shift_details:{shift}')
        loggr.info('------O.K: SHIFTS DETAILS SAVED SUCCESSFULLY')
    except Exception as e:
        loggr.error(f'ERROR at create_list_funcs.save_shift_details(): {e} ')
        return shift
            
