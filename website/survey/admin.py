# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Survey,questions

# Register your models here.

admin.site.register(Survey)
admin.site.register(questions)