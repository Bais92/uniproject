from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Question)
admin.site.register(Experiment)
admin.site.register(QuestionExperiment)
admin.site.register(Error)
admin.site.register(Results)
admin.site.register(Nudge)
admin.site.register(Benutzer)


