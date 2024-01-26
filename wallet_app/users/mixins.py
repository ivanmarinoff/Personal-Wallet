from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect

UserModel = get_user_model()


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')  # Use reverse lookup for login URL

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user != self.get_user(request, *args, **kwargs):
            return self.handle_no_permission()
        # elif not request.user.is_active:
        #     return self.handle_no_permission()
        elif request.user.pk != kwargs.get('pk'):
            # Optionally, you can raise Http404 or redirect to a different page
            raise Http404("You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect(self.login_url)

    def get_user(self, request, *args, **kwargs):
        # Override this method to customize how the user associated with the request is obtained
        return request.user


class ErrorRedirectMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('landing'))
