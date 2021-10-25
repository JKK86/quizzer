from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from quiz_app.models import Result
from users.forms import RegistrationForm, EditProfileForm

User = get_user_model()


class RegistrationView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email']
        )
        messages.success(self.request, "Użytkownik został pomyślnie zarejestrowany")
        return super().form_valid(form)


class UserProfileView(View):
    def get(self, request):
        user = request.user
        results = Result.objects.filter(user=user)
        return render(request, 'user_profile.html', {'results': results})


class EditProfileView(View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'registration/edit_profile.html', {'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('user_profile')