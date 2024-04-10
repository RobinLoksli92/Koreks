from django.contrib import admin
from .models import *


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(TestResult)
class AnswerAdmin(admin.ModelAdmin):
    pass
