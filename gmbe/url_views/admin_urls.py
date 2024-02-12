from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from facades.admin_facade import AdminFacade

admin_facade = AdminFacade()


@csrf_exempt
@api_view(['GET'])
def families_list(request):
    
    if request.method != 'GET':
        return ('ERROR: GET requests only!')

    try:
        # get list of all administrators  
        families_list = admin_facade.get_all_families(request)
        
        # successful response with the list of customers or an error response 
        return families_list
    
    # handle any exceptions that occur while fetching the customers list
    except Exception as e:
        return (f'ERROR:{e}')