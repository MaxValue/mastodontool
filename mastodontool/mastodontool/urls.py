from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static
from mastodontool import views

# Loading plotly Dash apps script
import uptime.dash_app_code
import uptime.instancestable

#from django_plotly_dash.views import add_to_session

urlpatterns = [
    path('admin/', admin.site.urls),
	
	path('', include('django.contrib.auth.urls')),
	url('^dash_plot$', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
	url('^dash_table$', TemplateView.as_view(template_name='instances.html'), name="dash_table"),
	url('^django_plotly_dash/', include('django_plotly_dash.urls')),
	path('', TemplateView.as_view(template_name='home.html'), name='home'),
	path('about', TemplateView.as_view(template_name='about.html'), name='about'),
	url("instance/", views.instance_info, name ="instance_info"),
	url('^instance/(?P<id>\w+?)/$', TemplateView.as_view(template_name='instance_info.html'), name ="instance_info")
]