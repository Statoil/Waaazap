from django.conf.urls import patterns, include, url
from django.contrib import admin

from webfront import views as webfrontviews
from views import HappynessRegistrationViewSet
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from DjangoRESTServicesTOSL import views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'happyness_registrations', HappynessRegistrationViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoRESTServicesTOSL.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', webfrontviews.hello),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^happyness_reg/$', views.happyness_reg_list),
    url(r'^happyness_reg/(?P<pk>[0-9]+)/$', views.happyness_reg_detail),
    url(r'^happyness_status/$', views.happyness_status),

)
