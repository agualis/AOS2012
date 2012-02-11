# coding=UTF-8
from django.views.generic.simple import direct_to_template
import sys
import logging
import traceback

def show_500(request):
    exception = sys.exc_info()[0]
    traceback.print_exc()
    error_number = '500'
    error_title = 'Error interno del servidor.'
    error_explanation = 'Lo sentimos, ha ocurrido un error no esperado.'
    return show_error_page(request, error_number, error_title, error_explanation)

def show_404(request):
    error_number = '404'
    error_title = 'Página no encontrada.'
    error_explanation = 'Lo sentimos, la página que has intentado abrir no existe o no está disponible.'
    return show_error_page(request, error_number, error_title, error_explanation)

def show_403(request):
    error_number = '403'
    error_title = 'No tienes permisos.'
    error_explanation = 'Lo sentimos, no tienes permisos para acceder a la página que has intentado abrir.'
    return show_error_page(request, error_number, error_title, error_explanation)

def show_error_page(request, error_number, error_title, error_explanation):
    return direct_to_template(request, 'error.html', extra_context={'number': error_number, 'title': error_title, 'explanation': error_explanation}) 
