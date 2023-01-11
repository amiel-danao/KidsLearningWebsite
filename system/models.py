from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from kidslearning.context_processors import MAX_LESSON1_LEVELS, MAX_LESSON2_LEVELS, MAX_LESSON3_LEVELS
from kidslearning.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
import os
from dotenv import load_dotenv

load_dotenv()


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


def gen_session_no(lesson_name=None, user=None) -> int:
    today = timezone.now()

    if lesson_name is not None and user is not None:
        filter = Score.objects.filter(user=user, lesson_name=lesson_name)
        max = filter.aggregate(Max('session_no'))
        maximum = max['session_no__max']
        count = filter.count()
        if lesson_name == 'Learn ABC':
            if count > int(os.getenv(MAX_LESSON1_LEVELS, "6")):
                return maximum + 1
        elif lesson_name == 'Spelling':
            if count > int(os.getenv(MAX_LESSON2_LEVELS, "7")):
                return maximum + 1
        else:
            if count > int(os.getenv(MAX_LESSON3_LEVELS, "2")):
                return maximum + 1
    return 1

    
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

    def save(self, *args, **kwargs):
        self.session_no = gen_session_no(self.lesson_name, self.user)
        super().save(*args, **kwargs)  # Call the "real" save() method.