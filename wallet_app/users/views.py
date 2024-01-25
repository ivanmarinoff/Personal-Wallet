from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins, get_user_model
from django.views.generic import TemplateView

from wallet_app.users.forms import RegisterUserForm, LoginUserForm
from django.contrib.auth import authenticate, login, logout

UserModel = get_user_model()


# data_to_cache = {'key': 'value'}
# cache.set('my_key', data_to_cache)
#
# # Retrieve data from the cache
# cached_data = cache.get('my_key')
#
# if cached_data is None:
#     # Data not in cache, fetch from database or perform calculation
#     # and store it in cache
#     cached_data = {'key': 'value'}
#     cache.set('my_key', cached_data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         # Log the user in after registration
#         login(request, user)
#         return Response(serializer.data, status=status.HTTP_302_FOUND)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LoginApiUserView(ObtainAuthToken):
#     authentication_classes = [TokenAuthentication]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key, 'user_id': user.id})
#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ProfileApiDetailsView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
#
#     def get(self, request, *args, **kwargs):
#         user = self.request.user
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


class OnlyAnonymousMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard', kwargs={'pk': request.user.pk})
        return super().dispatch(request, *args, **kwargs)


class LandingView(OnlyAnonymousMixin, TemplateView):
    template_name = "landing.html"


class RegisterUserView(views.CreateView):
    model = UserModel
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login_user')
    class_name = 'signup'

    def form_valid(self, form):
        valid = super(RegisterUserView, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

    # def form_invalid(self, form):
    #     form.errors.clear()
    #     form.add_error(None, '   Invalid Email or Password')
    #     return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={'pk': self.object.pk})


class LoginUserView(auth_views.LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')
    class_name = 'login'
    redirect_authenticated_user = True

    def form_valid(self, form):
        result = form.cleaned_data.get('username')
        if not result:
            self.request.session.clear()
            self.request.session.set_expiry(0)

        return super().form_valid(form)

    def form_invalid(self, form):
        form.errors.clear()
        form.add_error(None, '   Invalid Username or Password')
        return super().form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.pk})


class LogoutUserView(auth_mixins.LoginRequiredMixin, views.View):
    def get(self, request):
        logout(request)
        return redirect("/")
    # next_page = reverse_lazy('landing')

    # def get_next_page(self):
    #     next_page = self.request.GET.get('next')
    #     if next_page:
    #         return next_page
    #     return self.next_page

    # def post(self, request, *args, **kwargs):
    #     # Perform any custom actions before logout, if needed
    #     # For example, saving user activity or updating user status
    #
    #     # Call the parent class's post method to perform the logout
    #     response = super().post(request, *args, **kwargs)
    #     if response.status_code == 302:
    #         response.delete_cookie('csrftoken')
    #     elif response.status_code == 200:
    #         response.delete_cookie('csrftoken')

    # Perform any additional actions after logout, if needed

    # Redirect to the next page after logout
    # return HttpResponseRedirect(self.get_next_page())

# class ProfileDetailsView(ErrorRedirectMixin, auth_mixins.LoginRequiredMixin, views.DetailView):
#     template_name = 'users/profile-details.html'
#     model = UserModel
#     form_class = UserEditForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.object
#
#     def get_success_url(self):
#         return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})
#
#
# class ProfileEditView(ErrorRedirectMixin, auth_mixins.LoginRequiredMixin, views.UpdateView):
#     template_name = 'users/profile-edit-page.html'
#     model = UserModel
#     form_class = UserEditForm
#
#     def get_success_url(self):
#         return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         save_changes = self.request.GET.get('save_changes')
#         if save_changes:
#             self.object.save()
#         return result
#
#
# class PasswordChangeView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
#     form_class = UserPasswordChangeForm
#     template_name = 'users/profile_password_change.html'
#
#
# class PasswordChangeDoneView(ErrorRedirectMixin, auth_views.PasswordChangeDoneView):
#     template_name = 'users/password_change_done.html'
#     success_url = reverse_lazy('password_change_done')
#
#     def get_success_url(self):
#         return self.request.POST.get('next', self.success_url)
#
#
# class ProfileDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
#     model = UserModel
#     template_name = 'users/profile-delete-page.html'
#     next_page = reverse_lazy('home_page')
#
#     def post(self, *args, pk):
#         self.request.user.delete()
#
#         return HttpResponseRedirect(self.next_page)
