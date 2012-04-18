from aos.lib.timetable.timetable import Timetable
from aos.lib.common_utils.json_utils import JsonResponse
from aos.models.attendant_model import Attendant

import logging

def get_talks(request):
    return JsonResponse(Timetable().get_talks_json())
    
def get_speakers(request):
    return JsonResponse(Attendant.get_speakers_json())