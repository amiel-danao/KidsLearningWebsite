from django.contrib import admin
from system.models import Announcement, CustomUser, Download, Score
from django.contrib.auth.models import Group
from django_reverse_admin import ReverseModelAdmin
from admin_interface.models import Theme

admin.site.unregister((Group, Theme))
exempted_models = (Group, Theme)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):

    list_filter = ('user', 'date', 'session_no', 'score', 'lesson_name', 'summary')
    readonly_fields = ('user', 'date', 'session_no', 'score', 'lesson_name', 'summary')
    fields = ('user', 'date', 'session_no', 'score', 'lesson_name', 'summary')
    list_display = ('user', 'date', 'session_no', 'score', 'lesson_name', 'summary')

    def has_add_permission(self, request):
        return False

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    fields = ('title',
    'description',
    'file',
    'date',
    'downloadable')

    list_filter = ('title', 'downloadable')

    list_display = ('title',
    'description',
    'file',
    'downloadable')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    fields = ('title',
    'description',
    'content',
    'thumbnail',
    'date_valid',
    'active')

    list_filter = ('date_valid', 'active')

    list_display = ('title',
    'description',
    'content',
    'thumbnail',
    'date_valid',
    'active')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'is_superuser', 'last_login', 'is_active', 'date_joined')
    readonly_fields = ('password', 'date_joined', 'last_login', 'email', 'scores')
    fields = ('email', 'is_superuser', 'last_login', 'is_active', 'date_joined', 'scores')
    list_display = ('email', 'is_superuser', 'last_login', 'is_active', 'date_joined')

    def scores(self, obj):
        my_scores = Score.objects.filter(user=obj)
        return ', '.join([c.summarize() for c in my_scores])
        # return ', '.join(map( str, my_scores ))


# @admin.register(CustomUser)
# class CustomUserAdmin(ReverseModelAdmin):
#     readonly_fields = ('password', 'date_joined', 'last_login', 'email')
#     fields = ('email', 'is_superuser', 'last_login', 'is_active', 'date_joined')
#     list_display = ('email', 'is_superuser', 'last_login', 'is_active', 'date_joined')
#     inline_type = 'tabular'
#     inline_reverse = ['email', 'is_superuser', 'last_login', 'is_active', 'date_joined',
#                       ('user', {'fields': ['date', 'session_no', 'score', 'lesson_name', 'summary']}),
#                       ]


admin.site.site_header = "CVSU - Kids Learning"
admin.site.site_title = "CVSU - Kids Learning System"
admin.site.index_title = "Welcome to CVSU Kids Learning Teacher's Panel"
