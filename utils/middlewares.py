from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


class DoesNotExistMiddleware:
    def __init__(self, get_response, model=None):
        self.get_response = get_response
        self.model = model

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            model = str(exception).split(" ")[0]
            return JsonResponse({"response": f"{model} not found!"}, status=404)
