from django.contrib import admin

from quiz_app.forms import BaseAnswerInlineFormset
from quiz_app.models import Category, Quiz, Question, Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    prepopulated_fields = {'slug': ('name', )}


class QuestionAdminInline(admin.TabularInline):
    model = Question
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'time', 'author', 'created', 'updated']
    exclude = ['created', 'updated', ]
    prepopulated_fields = {'slug': ('title', )}
    inlines = [QuestionAdminInline, ]
    list_filter = ['category', 'author']
    search_fields = ['title', 'description', ]
    list_editable = ['time', ]
    ordering = ['-created']


class AnswerInline(admin.TabularInline):
    model = Answer
    formset = BaseAnswerInlineFormset
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['content', ]
    fields = ['content', 'image', 'quiz', ]
    inlines = [AnswerInline, ]
    search_fields = ['content', ]
    list_filter = ['quiz', ]
