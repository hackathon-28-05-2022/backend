from django.utils import timezone
from random import randrange


class LastVisitedHandle:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.last_time_gained_pulse + timezone.timedelta(hours=24) < timezone.now():
                request.user.last_time_gained_pulse = timezone.now()
                request.user.set_pulse(request.user.pulse + 10 * request.user.day_visited_in_a_row)  # TODO: remove hardcode
                request.user.day_visited_in_a_row += 1
                if randrange(1000 // request.user.day_visited_in_a_row) == 0:  # TODO: remove hardcode
                    request.user.set_electricity(request.user.electricity + 100)  # TODO: remove hardcode
                request.user.save()
        response = self._get_response(request)
        return response
