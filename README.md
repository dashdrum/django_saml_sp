#Django SAML SP

Packaged and maintained by Dan Gentry - dan@dashdrum.com

Based on django_saml_example by Matthew Rich - https://bitbucket.org/technivore/django-saml-example/

This basic library does just what is needed and nothing more.  Enterprising developers can extend to add additional SAML2 features.

Requires python3-saml for Python 3 projects. Will also work with python-saml for Python 2 projects.

Setup

    SAML/ -- folder  contains:
    	settings.json
    	advanced_settings.json
    	certs/  -- (Keep certs out of VCS)
    		sp.crt
    		sp.key

--------------------------------------------------------------------------------------------------

settings.json:

    {
        "strict": true,
        "debug": true,
        "sp": {
            "entityId": "http://myapp.example.com",
            "assertionConsumerService": {
                "url": "https://myapp.example.com/saml2/complete-login/",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"
        },
        "my_idp": {
            "entityId": "https://myidp.example.com/metadata_url",
            "singleSignOnService": {
                "url": "https://myidp.example.com/saml2/sso",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "singleLogoutService": {
                "url": "https://myidp.example.com/saml2/slo",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "x509cert": "Insert IDP cert text here"
        }
    }

--------------------------------------------------------------------------------------------------

advanced_settings.py:

Set security to match the configuration of your IDP.

    {
        "security": {
            "nameIdEncrypted": false,
            "authnRequestsSigned": false,
            "logoutRequestSigned": false,
            "logoutResponseSigned": false,
            "signMetadata": false,
            "wantMessagesSigned": false,
            "wantAssertionsSigned": false,
            "wantNameIdEncrypted": false,
            "signatureAlgorithm": "http://www.w3.org/2000/09/xmldsig#rsa-sha1",
            "metadataValidUntil": "",
            "metadataCacheDuration": "P10D"
        },
        "contactPerson": {
            "technical": {
                "givenName": "My Name",
                "emailAddress": "tech_guy@example.com"
            },
            "support": {
                "givenName": "Another Name",
                "emailAddress": "support_gal@example.com"
            }
        },
        "organization": {
            "en-US": {
                "name": "Your Org",
                "displayname": "Organization Long Name",
                "url": "http://example.com/"
            }
        }
    }

--------------------------------------------------------------------------------------------------

urls.py:

    from django.conf.urls import include

    url(r'^saml2/', include('django_saml_sp.urls')),

--------------------------------------------------------------------------------------------------

settings.py:

    ## Django SAML Example Settings

    LOGIN_URL = 'saml2/initiate-login/'

    LOGIN_REDIRECT_URL = '/'

    # Path to the SAML folder that contains certs and settings #
    SAML_FOLDER = os.path.join(BASE_DIR, 'saml')

    # Default AUTHENTICATION_BACKENDS should be explicitly defined for project in settings.py as:
    #   AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',] <- Default value as of Django v1.9
    #   AUTHENTICATION_BACKENDS = []   <- blank list

    # Insert the SAML authentication backend first in the list
    AUTHENTICATION_BACKENDS.insert(0,'django_saml_sp.backends.SAMLServiceProviderBackend')

    # SAML App
    INSTALLED_APPS.append('django_saml_sp')

--------------------------------------------------------------------------------------------------