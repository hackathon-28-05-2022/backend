from django.utils import timezone


class LastVisitedHandle:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.last_time_gained_pulse + timezone.timedelta(hours=24) < timezone.now():
                request.user.last_time_gained_pulse = timezone.now()
                request.user.set_pulse(request.user.pulse + 10 * request.user.day_visited_in_a_row)  # TODO: remove hardcode
                request.user.day_visited_in_a_row += 1
                request.user.save()
        response = self._get_response(request)
        return response
