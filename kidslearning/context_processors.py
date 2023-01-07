from django.contrib import admin

from dotenv import load_dotenv
import os

load_dotenv()
MAX_LESSON1_LEVELS = "MAX_LESSON1_LEVELS"
MAX_LESSON2_LEVELS = "MAX_LESSON2_LEVELS"
MAX_LESSON3_LEVELS = "MAX_LESSON3_LEVELS"

def global_context(request):
    return {
        MAX_LESSON1_LEVELS: os.getenv(MAX_LESSON1_LEVELS),
        MAX_LESSON2_LEVELS: os.getenv(MAX_LESSON2_LEVELS),
        MAX_LESSON3_LEVELS: os.getenv(MAX_LESSON3_LEVELS),
    }


