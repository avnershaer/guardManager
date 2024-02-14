from ..api.serislizers_views import api_get_list
from ..dal.models import Families, User
from ..api.serializers import FamiliesSerializer, UserSerializer
from django.http import JsonResponse
from loggers.loggers import logger, err_logger


loggr = logger()
errlogger = err_logger()


class AdminFacade():#(AnonymousFacade)
    
    def get_all_families(self, request): #(request for @require_role)
            loggr.info('OK ------------got test 2')
            try:
                # get list of all families
                families_list = api_get_list(instance_model=Families, model_serializer = FamiliesSerializer)

                # success reponse with list of families.  
                return families_list 

            # handle any exceptions that occur during getting the list 
            except Exception as e:
                return JsonResponse({'status:':'ERROR at admin_facade.AdminFacade.get_all_families','details:':str(e)}, status=500, safe=False)
            
    def get_all_users(self, request):
         
        try:
            users_list = api_get_list(instance_model=User, model_serializer=UserSerializer)
            return users_list
        
        except Exception as e:
            return JsonResponse({'status:':'ERROR at admin_facade.AdminFacade.get_all_users()','details:':str(e)}, status=500, safe=False)