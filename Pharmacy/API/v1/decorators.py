

from Pharmacy.models import Store, StoreLocation



def store_location_url_decorator(views_function):
    def inner(request, *args, **kwargs):
        store_id = kwargs.get('store_id', None)
        location_id = kwargs.get('location_id', None)

        if not all([store_id, location_id]):
            raise Exception('Invalid Data')
        
        try:
            store = Store.objects.get(id = store_id)
            store_location = StoreLocation.objects.get(id = location_id)
        except Store.DoesNotExist:
            raise Exception('Invalid Store ID')
        except StoreLocation.DoesNotExist:
            raise Exception('Invalid Location ID')
        except Exception as err:
            raise Exception(f'Internal Server Error : {str(err)}')
        else:
            request.store = store
            request.store_location = store_location

        return views_function(request, *args, **kwargs)
    
    return inner

    