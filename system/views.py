from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from system.forms import NewUserForm
from django.contrib import messages

@login_required
def index(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('/accounts/login/')
    context = {}
    return render(request, 'index.html', context)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("system:index")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})
