import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from kidslearning.context_processors import MAX_LESSON1_LEVELS, MAX_LESSON2_LEVELS, MAX_LESSON3_LEVELS
from system.forms import NewUserForm
from django.contrib import messages
from rest_framework import viewsets, mixins, generics
from system.mixins import SuperuserRequiredMixin
from system.models import CustomUser, Score
from system.serializers import ScoreSerializer
from django.views.generic import ListView
from django_tables2.config import RequestConfig
from system.tables import ScoreTable
from .filters import ScoreFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django.db.models import Max
from django.contrib.auth.views import LoginView


@login_required
def index(request):
    context = {}
    return render(request, 'pages/lessons.html', context)

@login_required
def play(request):
    context = {}
    return render(request, 'index.html', context)

class MyLoginView(LoginView):
    # form_class=LoginForm
    redirect_authenticated_user=True
    template_name='registration/login.html'

    def get_success_url(self):
        # write your logic here
        if self.request.user.is_superuser:
            return '/progress/'
        return '/'


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


class ScoreListView(LoginRequiredMixin, SuperuserRequiredMixin, SingleTableView, FilterView):
    model = Score
    table_class = ScoreTable
    template_name = 'pages/progress.html'
    filterset_class = ScoreFilter
    table_pagination = {
        'per_page': 10,
    }
    strict=False

    def get_queryset(self):
        qs = super().get_queryset()

        user = self.request.GET.get('user', None)
        if user is None or len(user) == 0:
            return qs
        else:
            return qs.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super(ScoreListView, self).get_context_data(**kwargs)
        user = self.request.GET.get('user', None)
        species=self.get_queryset()
        f = self.filterset_class(self.request.GET, queryset=species)
        context['filter'] = f
        table = self.table_class(f.qs)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context['table'] = table

        session_no = self.request.GET.get('session_no', "")
        if len(session_no) == 0:
            session_no = 1
        context['session_progress_lesson1'] = get_progress(user, session_no, MAX_LESSON1_LEVELS, 'Learn ABC')
        context['session_progress_lesson2'] = get_progress(user, session_no, MAX_LESSON2_LEVELS, 'Spelling')
        context['session_progress_lesson3'] = get_progress(user, session_no, MAX_LESSON3_LEVELS, 'Math')

        max = 1
        
        if user is None or len(user) == 0:
            max = Score.objects.all().aggregate(Max('session_no'))
        else:
            max = Score.objects.filter(user=user).aggregate(Max('session_no'))
        if not 'session_no__max' in max:
            max = 1
        else:
            max = max['session_no__max']
        context['max_sessions'] = range(max)

        return context

def get_progress(user, session_no, lesson_max_name, lesson_name):
    if user is None:
        return 0
    progress = 0
    try:
        max = int(os.getenv(lesson_max_name))
        current = Score.objects.filter(user=user, session_no=session_no, lesson_name=lesson_name).count()
        
        progress = (current / max) * 100
    except Exception:
        pass

    return round(progress, 2)
