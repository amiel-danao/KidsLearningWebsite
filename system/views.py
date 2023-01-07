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


# class ScoreListView(LoginRequiredMixin, SingleTableView):
#     model = Score
#     filterset_class = ScoreFilter

#     table_class = ScoreTable
#     template_name = 'pages/progress.html'
#     # filterset_class = OrderServiceFilter
#     per_page = 8

#     def get_table_data(self):
#         user = self.request.GET.get('user', None)
#         if user is None:
#             return Score.objects.all()
#         else:
#             return Score.objects.filter(user=self.request.GET)

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
        if user is None:
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

        session_no = self.request.GET.get('session_no', 1)
        context['session_progress_lesson1'] = get_progress(user, session_no, MAX_LESSON1_LEVELS, 'Learn ABC')
        context['session_progress_lesson2'] = get_progress(user, session_no, MAX_LESSON2_LEVELS, 'Spelling')
        context['session_progress_lesson3'] = get_progress(user, session_no, MAX_LESSON3_LEVELS, 'Math')


        max = Score.objects.filter(user=user).aggregate(Max('session_no'))
        if user is None:
            max = Score.objects.all().aggregate(Max('session_no'))
        context['max_sessions'] = range(max['session_no__max'])

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
