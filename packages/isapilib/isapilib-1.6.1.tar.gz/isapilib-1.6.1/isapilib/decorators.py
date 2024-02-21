import traceback

from django.http import JsonResponse
from rest_framework.request import Request

from app import settings
from isapilib.utilities import insert_log


def safe_method(view_func):
    def wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            if settings.DEBUG:
                print(traceback.format_exc())

            return JsonResponse({
                'type': str(type(e)),
                'message': str(e)
            }, status=500)

    return wrapped_view


def logger(interfaz, tipo, log_all=False):
    def decorador(func):
        def wrapper(*args, **kwargs):
            request = next((arg for arg in args if isinstance(arg, Request)), None)

            try:
                response: JsonResponse = func(*args, **kwargs)
                if (hasattr(response, 'status_code') and response.status_code not in range(200, 300)) or log_all:
                    insert_log(request=request, response=str(response.content), interfaz=interfaz, tipo=tipo)
                return response
            except Exception as e:
                insert_log(request=request, response=str(e), interfaz=interfaz, tipo=tipo)
                raise e

        return wrapper

    return decorador
