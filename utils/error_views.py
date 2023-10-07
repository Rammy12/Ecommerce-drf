from django.http import JsonResponse


def handle404(request,exception):
    message=('Route not found')
    responce=JsonResponse(data={'error':message})
    responce.status_code=404
    return responce