from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from kidslearning.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    picture = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def username(self):
        return self.email

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"


def gen_session_no() -> int:
    today = timezone.now()
    count = Score.objects.filter(date = today.replace(hour=0,minute=0,second=0)).count()
    return count + 1

    
class Score(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    lesson_name = models.CharField(max_length=50)
    time = models.FloatField(default=0)
    summary = models.CharField(max_length=256)

    session_no = models.PositiveIntegerField(default=gen_session_no)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def summarize(self):
        return f"Date: {self.date}, Lesson Name: {self.lesson_name}, Score: {self.score}, Time: {self.time}, Session No. {self.session_no}, Summary: {self.summary}"
