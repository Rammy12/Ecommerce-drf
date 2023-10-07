def get_current_host(request):
    protocal=request.is_secure() and 'https' or 'http'
    host=request.get_host()
    return "{protocal}://{host}".format(protocal=protocal,host=host)