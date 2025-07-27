from django.contrib import admin
from .models import Problem
from .testcases_model import TestCase
admin.site.register(Problem)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'input_data', 'expected_output')