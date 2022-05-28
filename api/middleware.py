from django.utils import timezone


class LastVisitedHandle:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        request.user.last_login = timezone.now()
        response = self._get_response(request)
        return response
