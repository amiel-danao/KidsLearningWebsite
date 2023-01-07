import django_tables2 as tables
from system.models import Score
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return f"Total: {sum(bound_column.accessor.resolve(row) for row in table.data)}"


class ScoreTable(tables.Table):
    # total = tables.Column(footer=total_footer)
    score = SummingColumn()
    time = SummingColumn()

    class Meta:
        orderable = False
        model = Score
        orderable = True
        template_name = "partials/_custom_table.html"
        empty_text = _("No Progress Data")
        fields = ('user', 'date', 'lesson_name', 'score', 'time', 'session_no', 'summary')
        attrs = {'class': 'table table-hover table-light table-bordered'}
        
    def render_user(self, value, record):
        url = format_html('<a href="{}?user={}" >{}</a>', reverse('system:progress'), record.user.pk, value)
        return url