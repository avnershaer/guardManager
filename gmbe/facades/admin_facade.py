from api.serislizers_views import api_get_list
from dal.models import Families
from api.serializers import FamiliesSerializer

class AdminFacade():#(AnonymousFacade)
    
    def get_all_families(self, request): #(request for @require_role)
            
            try:
                # get list of all families
                families_list = api_get_list(instance_model=Families, model_serializer = FamiliesSerializer)

                # success reponse with list of families.  
                return families_list 

            # handle any exceptions that occur during getting the list 
            except Exception as e:
                return (f'ERROR:{e}')