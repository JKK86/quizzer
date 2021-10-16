from django.contrib import admin

from quiz_app.models import Category, Quiz, Question, QuestionOrder, Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    prepopulated_fields = {'slug': ('name', )}


class QuestionOrderAdminInline(admin.TabularInline):
    model = QuestionOrder
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'time', 'author', 'created', 'updated']
    exclude = ['created', 'updated', ]
    prepopulated_fields = {'slug': ('title', )}
    inlines = [QuestionOrderAdminInline, ]
    list_filter = ['category', 'author']
    search_fields = ['title', 'description', ]
    list_editable = ['time', ]
    ordering = ['-created']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['content', 'category' ]
    fields = ['content', 'image', 'category', ]
    inlines = [AnswerInline, ]
    search_fields = ['content', ]
    list_filter = ['category', ]