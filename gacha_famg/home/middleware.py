from db.models import HomeUser


class HomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_home(self, user):
        try:
            home = HomeUser.objects.get(user=user).home
        except HomeUser.DoesNotExist:
            # TODO: ホームを作成するページに飛ばす
            home = HomeUser.objects.none()
        return home

    def set_request_attribute(self, request, hid=None, home=None):
        request.hid = hid
        request.home = home

    def __call__(self, request):
        if not request.user.is_authenticated:
            self.set_request_attribute(request)
            return self.get_response(request)
        home = self.get_home(request.user)
        if home:
            hid = home.hid
        else:
            hid = None
        self.set_request_attribute(request, hid, home)
        response = self.get_response(request)
        return response
