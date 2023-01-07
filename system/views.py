from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from system.forms import NewUserForm
from django.contrib import messages
from rest_framework import viewsets, mixins, generics
from system.models import CustomUser, Score
from system.serializers import ScoreSerializer


@login_required
def index(request):
    context = {}
    return render(request, 'pages/lessons.html', context)

@login_required
def play(request):
    context = {}
    return render(request, 'index.html', context)


def register_request(request):
    context = {}
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("system:index")
        context['form_errors'] = form.errors
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context["register_form"] = form
    return render(request=request, template_name="registration/register.html", context=context)


class ScoreViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer