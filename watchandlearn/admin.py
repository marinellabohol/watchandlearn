from django.contrib import admin
from watchandlearn.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# User: admin
# Password: adminpassword
# Email: admin@admin.com


class WordResource(resources.ModelResource):

    class Meta:
        model = Word

class WordAdmin(ImportExportModelAdmin):
    resource_class = WordResource

class EpisodeResource(resources.ModelResource):

    class Meta:
        model = Episode

class EpisodeAdmin(ImportExportModelAdmin):
    resource_class = EpisodeResource

class SeriesResource(resources.ModelResource):

    class Meta:
        model = Series

class SeriesAdmin(ImportExportModelAdmin):
    resource_class = SeriesResource

class QuizResource(resources.ModelResource):

    class Meta:
        model = Quiz

class QuizAdmin(ImportExportModelAdmin):
    resource_class = QuizResource

class QuestionResource(resources.ModelResource):

    class Meta:
        model = Question

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

class TopicResource(resources.ModelResource):

    class Meta:
        model = Topic

class TopicAdmin(ImportExportModelAdmin):
    resource_class = TopicResource

class InterestResource(resources.ModelResource):

    class Meta:
        model = Interest

class InterestAdmin(ImportExportModelAdmin):
    resource_class = InterestResource


# Register your models here.

admin.site.register(Profile)
admin.site.register(Word, WordAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Interest, InterestAdmin)

