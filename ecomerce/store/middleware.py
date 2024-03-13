from typing import Any
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ecomerce.ecomerce import settings

class DDoSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_window = 60 #60 seconds
        self.request_limit = 5
    
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        cache_key = f'ddos:{ip_address}'

        request_count = cache.get(cache_key, 0)
        request_count += 1

        if request_count > self.request_limit:
            #Too many requests within the time window, forbid the request
            return HttpResponseForbidden("Request Limit exceeded .Please try again later.")
        
        #set or update the cache with the incrementeed request count.
        cache.set(cache_key, request_count,self.time_window)

        return None
    
    def __call__(self, request) :
        return self.process_request(request) or self.get_response(request)
    
class BruteForceProtection:
    def __init__(self, get_response):

        self.get_response = get_response
    
    def __call__(self, request) :
        response = self.get_response(request)
        print(response)
        #check if the request is for the login page
        if request.path == settings.LOGIN_URL and request.method == "POST":
            #get the IP address of the client
            ip_address = request.META.get("REMOTE_ADDR")

            #increment the failed login attempt count for this IP address
            cache_key = f"login_attempts:{ip_address}"
            login_attempts = cache.get(cache_key, 0)
            if response.status_code != 200:
                cache.set(cache_key, login_attempts + 1, timeout=settings.BRUTE_FORCE_TIMEOUT)

                #If the login attempts exceed the threshold, block further attempts
            if login_attempts >= settings.BRUTE_FORCE_THRESHOLD:
                return HttpResponseForbidden(f"Too many login attempts. Please try again later after {settings.BRUTE_FORCE_TIMEOUT} seconds.")
            
        return response