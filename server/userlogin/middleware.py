from django import http
from django.contrib.gis.geoip2 import GeoIP2

class IpBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            g = GeoIP2()
            remote_addr = request.META['REMOTE_ADDR']
            country = g.country_code(remote_addr)
            if country != "TW":
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        except:
            # 給本機測試用
            if "192" not in remote_addr:
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')

        response = self.get_response(request)


        return response