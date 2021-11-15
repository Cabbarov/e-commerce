from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied



class FilterIpMiddleware(MiddlewareMixin):

    Blocked_IP_List = ['123.123.123.123']

    def process_view(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        if ip in self.Blocked_IP_List:
            raise PermissionDenied
        return None