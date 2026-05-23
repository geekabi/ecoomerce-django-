class UserIPMiddleware():

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        ip = request.META.get('REMOTE_ADDR')
        request.user_ip = ip
        return self.get_response(request)