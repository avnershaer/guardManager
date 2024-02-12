from dal.dviews import Dal
from utils.operations_funcs import serialize_data


dal = Dal()


# retrieve a list of objects from the database using the data access layer (dal)
def api_get_list(instance_model, model_serializer):
    
    try:
        # get a list of objects using the data access layer (dal)
        objects_list = dal.table_objects_list(model=instance_model)

        # no errors - serialize the data 
        obj_list = serialize_data(model_serializer=model_serializer, instance_model=instance_model, objects=objects_list, many=True)
        # return jsonresponse with object list
        return obj_list
    
    # handle any exceptions that occur during processing this method      
    except Exception as e:
        return (f'ERROR:{e}')