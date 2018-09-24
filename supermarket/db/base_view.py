from django.utils.decorators import method_decorator
from django.views import View

from login.common_def import verify_login_required


class BaseVerifyVeiw(View):
    @method_decorator(verify_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
