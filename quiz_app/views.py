from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views import View

from quiz_app.models import Quiz, Category


class QuizListView(View):
    def get(self, request, category_slug=None):
        quiz_list = Quiz.objects.all()
        categories = Category.objects.all()
        category = None
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            quiz_list = quiz_list.filter(category=category)
        paginator = Paginator(quiz_list, 6)
        page = request.GET.get('page', 1)
        try:
            quizzes = paginator.page(page)
        except PageNotAnInteger:
            quizzes = paginator.page(1)
        except EmptyPage:
            quizzes = paginator.page(paginator.num_pages)

        return render(request, 'quizzes/quiz_list.html', {
            'quizzes': quizzes,
            'category': category,
            'categories': categories,
            # 'page': page
        })
