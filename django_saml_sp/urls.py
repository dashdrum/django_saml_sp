from django.conf.urls import include, url
from .views import metadata, initiate_login, complete_login, complete_logout

urlpatterns = [
    url(r'^initiate-login/$', initiate_login, name="saml_sp_initiate_login"),
    url(r'^complete-login/$', complete_login, name="saml_sp_complete_login"),
    url(r'^complete-logout/$', complete_logout, name="saml_sp_complete_logout"),
    url(r'^metadata/$', metadata, name="saml_sp_metadata"),
]
