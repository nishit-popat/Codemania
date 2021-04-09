from django.contrib import admin

from .models import Contest, Problem, Profile, ProblemSolved

admin.site.register(Contest)
admin.site.register(Problem)
admin.site.register(Profile)
admin.site.register(ProblemSolved)

