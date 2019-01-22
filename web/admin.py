from django.contrib import admin

from . import models


class MiddleSurveyAdmin(admin.ModelAdmin):

    filter_horizontal = ("surveys", )


admin.site.register(models.ClassList)
admin.site.register(models.SurveyItem)
admin.site.register(models.SurveyRecord)
admin.site.register(models.Survey)
admin.site.register(models.SurveyChoices)
admin.site.register(models.SurveyCode)
admin.site.register(models.MiddleSurvey, MiddleSurveyAdmin)
