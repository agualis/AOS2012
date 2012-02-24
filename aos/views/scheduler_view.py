import logging
from aos.lib.scheduler import Scheduler
from google.appengine.ext import db
from django.shortcuts import render_to_response
from aos.lib.schedule_grid import ScheduleGrid

def create_schedule():
    pass
    
"""
def show_schedule(request):
    rooms = Scheduler.get_rooms()
    return render_to_response('show_talks.html', {'rooms': rooms})
"""
def show_schedule(request):
    grid = ScheduleGrid().grid
    rooms = Scheduler.get_rooms()
    hours = Scheduler.get_schedule_hours()
    return render_to_response('show_schedule.html', {'rooms': rooms, 'hours': hours, 'grid': grid})