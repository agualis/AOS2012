from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template

handler500 = 'aos.views.errors_view.show_500'
handler404 = 'aos.views.errors_view.show_404'
handler403 = 'aos.views.errors_view.show_403'

urlpatterns = patterns('',

    #User administator functions
    (r'^admin/init$', 'aos.api.web_admin_api.init_app'),
    
    #API
    (r'^api/talks', 'aos.api.phone_api.get_talks'),
    
    #views
    (r'^timetable/?$', 'aos.views.timetable_view.show_timetable'),
	(r'^attendant/?$', 'aos.views.attendant_view.create_attendant'),
	(r'^attendant/avatar/?$', 'aos.views.attendant_view.get_avatar'),
	(r'^talk/new/(?P<hour>(\d+))/(?P<room_id>(\d+))/?$', 'aos.views.talk_view.create_talk'),
	(r'^talk/(?P<talk_id>(\d+))/?$', 'aos.views.talk_view.edit_talk'),
	(r'^talk/?$', 'aos.views.talk_view.edit_talk'),

    #login functions
    (r'login(?P<return_url>/[\w_/]{0,50})?$', 'aos.lib.security.authentication.login'),
    (r'logout/?$', 'aos.lib.security.authentication.logout'),
    (r'^/?$', 'aos.views.timetable_view.show_timetable'),
)
