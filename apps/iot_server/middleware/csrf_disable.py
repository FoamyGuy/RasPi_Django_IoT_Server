from django.urls import resolve


# django2


class DisableCSRF(object):
    """Middleware for disabling CSRF in an specified app name.
    """

    def process_request(self, request):
        """Preprocess the request.
        """
        app_name = "iot_server"
        if resolve(request.path_info).app_name == app_name:
            setattr(request, '_dont_enforce_csrf_checks', True)
        else:
            pass  # check CSRF token validation
