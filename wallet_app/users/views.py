from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins, get_user_model
from django.views.generic import TemplateView
from wallet_app.users.forms import RegisterUserForm, LoginUserForm
from django.contrib.auth import authenticate, login, logout

from wallet_app.users.mixins import CustomLoginRequiredMixin

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


class LandingView(TemplateView):
    template_name = "landing.html"


class RegisterUserView(OnlyAnonymousMixin, views.CreateView):
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
