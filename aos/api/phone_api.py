from aos.lib.timetable.timetable import Timetable
import logging
from aos.lib.common_utils.json_utils import JsonResponse

def get_talks(request):
    return JsonResponse(Timetable().get_talks_json())
    