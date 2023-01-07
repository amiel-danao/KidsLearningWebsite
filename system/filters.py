import django_filters
from system.models import Score
from django_filters import DateRangeFilter,DateFilter
from django_filters.widgets import RangeWidget


class ScoreFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    # start_date = DateFilter(field_name='date',lookup_expr='gt') 
    # end_date = DateFilter(field_name='date',lookup_expr='lt')
    # date_range = DateRangeFilter(field_name='date')
    # summary = django_filters.CharFilter(lookup_expr='icontains')
    score_less_than = django_filters.CharFilter(field_name='score', lookup_expr='lt')
    score_greater_than = django_filters.CharFilter(field_name='score', lookup_expr='gt')
    lesson_name = django_filters.CharFilter(lookup_expr='icontains')
    session_no = django_filters.NumberFilter(label="Session No.")

    class Meta:
        model = Score
        fields = ('user', 'date', 'lesson_name', 'score', 'time', 'session_no', 'summary')
