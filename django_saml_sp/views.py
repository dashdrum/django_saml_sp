from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
import logging

logger = logging.getLogger('django_saml_sp')

def initiate_login(request):
    req = get_request_details(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    return HttpResponseRedirect(auth.login(return_to=return_url))

@csrf_exempt
def complete_login(request):
    req = get_request_details(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)

    auth.process_response()
    errors = auth.get_errors()
    if not errors:
        if auth.is_authenticated():
            user = authenticate(saml_authentication=auth)
            login(request, user)
            if 'RelayState' in req['post_data'] and \
                        OneLogin_Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']:
                return HttpResponseRedirect(auth.redirect_to(req['post_data']['RelayState']))
            else:
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            raise PermissionDenied()
    else:
        logger.error('Error in django_saml_sp.views.complete_login: %s' % (auth.get_last_error_reason()))
        logger.error('Errors: %s' % (', '.join(errors)))
        return HttpResponseBadRequest("Error when processing SAML Response: %s" % (', '.join(errors)))

def metadata(request):
    req = get_request_details(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)

    saml_settings = auth.get_settings()

    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if errors:
        return HttpResponseServerError(content=', '.join(errors))
    else:
        return HttpResponse(content=metadata, content_type='text/xml')

def complete_logout(request):
    pass

def get_request_details(request):
    return {
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META.get('HTTP_X_FORWARDED_PORT', request.META['SERVER_PORT']),
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy()
    }
