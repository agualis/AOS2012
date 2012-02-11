from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template

handler500 = 'points_of_sale.views.errors_view.show_500'
handler404 = 'points_of_sale.views.errors_view.show_404'
handler403 = 'points_of_sale.views.errors_view.show_403'

urlpatterns = patterns('',

    #User administator functions
    (r'^admin/?$', 'aos.views.home_view.get_homepage'),
    (r'^admin/create_admin_user$', 'aos.web_admin.web_admin_api.create_admin_user'),
    (r'^admin/init_web_security?$', 'aos.web_admin.web_admin_api.init_all'),

    #example functions
    (r'^shout$', 'aos.views.shout_view.shout'),
    (r'^post$', 'aos.views.shout_view.post'),


    #login functions
    (r'login(?P<return_url>/[\w_/]{0,50})?$', 'aos.users.authentication.login'),
    (r'logout/?$', 'aos.users.authentication.logout'),
    (r'^/?$', 'aos.views.home_view.get_homepage'),
)
