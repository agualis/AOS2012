from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template

handler500 = 'points_of_sale.views.errors_view.show_500'
handler404 = 'points_of_sale.views.errors_view.show_404'
handler403 = 'points_of_sale.views.errors_view.show_403'

urlpatterns = patterns('',

    #User administator functions
    (r'^admin/?$', 'aos.views.home_view.get_homepage'),
    (r'^admin/init$', 'aos.web_admin.web_admin_api.init_app'),
    (r'^admin/init_web_security?$', 'aos.web_admin.web_admin_api.init_all'),
    (r'^admin/create_example_talks?$', 'aos.web_admin.web_admin_api.create_example_talks'),

    #example functions
    (r'^shout$', 'aos.views.shout_view.shout'),
    (r'^post$', 'aos.views.shout_view.post'),

    #views
	(r'^attendant$', 'aos.views.attendant_view.create_attendant'),
	(r'^timetable$', 'aos.views.timetable_view.show_timetable'),
	(r'^talk/new/(?P<hour>(\d+))/(?P<room_id>(\d+))/?$', 'aos.views.talk_view.create_talk'),
	(r'^talk/(?P<talk_id>(\d+))$', 'aos.views.talk_view.edit_talk'),
	(r'^talk$', 'aos.views.talk_view.edit_talk'),

    #login functions
    (r'login(?P<return_url>/[\w_/]{0,50})?$', 'aos.users.authentication.login'),
    (r'logout/?$', 'aos.users.authentication.logout'),
    (r'^/?$', 'aos.views.home_view.get_homepage'),
)
