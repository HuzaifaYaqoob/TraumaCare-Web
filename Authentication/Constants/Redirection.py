



def NextRedirect(request):
    next_url = request.GET.get('next', None)
    query = '?'

    if next_url:
        redirect_auto_login = request.GET.get('redirect_auto_login', None)
        if redirect_auto_login :
            if request.user.is_authenticated:
                quries = {
                    'user_id' : f'{request.user.id}',
                    'auth_token' : f'{request.user.auth_token}',
                }
                for key in quries:
                    query += f'{key}={quries[key]}&'
            else:
                next_url = 'usernotauth'
        else:
            next_url = '/redirect_auto_login'
            
        return f'{next_url}{query}'
    else:
        # next_url = None
        next_url = '/'
    
    return next_url


def getQueryParams(request):
    data = request.GET

    query = '?'
    for key, value in data.items():
        query += f'{key}={value}&'
    
    return query