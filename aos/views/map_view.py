from django.shortcuts import render_to_response

def show_map(request):
    return render_to_response('map.html')
