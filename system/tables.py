import django_tables2 as tables
from system.models import Announcement, Score
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
import datetime

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return f"Total: {sum(bound_column.accessor.resolve(row) for row in table.data)}"

class SummingTimeColumn(tables.Column):
    def render_footer(self, bound_column, table):
        time = str(datetime.timedelta(seconds=sum(bound_column.accessor.resolve(row) for row in table.data))).split(".")[0]
        return f"Total: {time}"

class AnnouncementTable(tables.Table):
    class Meta:
        model = Announcement

class ScoreTable(tables.Table):
    # total = tables.Column(footer=total_footer)
    score = SummingColumn()
    time = SummingTimeColumn()

    class Meta:
        orderable = False
        model = Score
        orderable = True
        template_name = "partials/_custom_table.html"
        empty_text = _("No Progress Data")
        fields = ('user', 'date', 'lesson_name', 'score', 'time', 'session_no', 'summary')
        attrs = {'class': 'table table-hover table-bordered'}
        
    def render_user(self, value, record):
        url = format_html('<a href="{}?user={}" >{}</a>', reverse('system:progress'), record.user.pk, value)
        return url

    def render_time(self, value, record):
        formatted_seconds = str(datetime.timedelta(seconds=value)).split(".")[0]
        return formatted_seconds