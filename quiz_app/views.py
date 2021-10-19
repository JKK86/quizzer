from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from quiz_app.models import Quiz, Category, Result


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


class QuizDetailView(View):
    def get(self, request, quiz_id, quiz_slug):
        quiz = get_object_or_404(Quiz, pk=quiz_id, slug=quiz_slug)
        return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})


class QuizDataView(View):
    def get(self, request, quiz_id, quiz_slug):
        quiz = get_object_or_404(Quiz, pk=quiz_id, slug=quiz_slug)
        questions = []
        for question in quiz.questions.all():
            answers = []
            for answer in question.answers.all():
                answers.append(answer.content)
            questions.append({str(question): answers})
        return JsonResponse({'questions': questions})


class QuizDataSaveView(View):
    def post(self, request, quiz_id, quiz_slug):
        if request.is_ajax():
            quiz = get_object_or_404(Quiz, pk=quiz_id, slug=quiz_slug)
            user = request.user
            data = request.POST

            results = []
            score = 0

            for q in quiz.questions.all():
                answer_selected = data.get(q.content)
                q_answers = q.answers.all()
                for answer in q_answers:
                    if answer.is_correct:
                        correct_answer = answer.content
                        if answer_selected:
                            if answer_selected == correct_answer:
                                score += 1
                            results.append({str(q): {
                                'correct_answer': correct_answer,
                                'selected_answer': answer_selected
                            }})
                        else:
                            results.append({str(q): {
                                'correct_answer': correct_answer,
                                'selected_answer': 'Brak odpowiedzi'}})
            Result.objects.create(quiz=quiz, user=user, score=(score / quiz.number_of_questions))
            return JsonResponse({'results': results, 'score': score})
