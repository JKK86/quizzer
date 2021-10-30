from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.base import TemplateResponseMixin

from quiz_app.forms import QuestionFormSet
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

        return render(request, 'quizzes/quiz/quiz_list.html', {
            'quizzes': quizzes,
            'category': category,
            'categories': categories,
            # 'page': page
        })


class QuizDetailView(View):
    def get(self, request, quiz_id, quiz_slug):
        quiz = get_object_or_404(Quiz, pk=quiz_id, slug=quiz_slug)
        return render(request, 'quizzes/quiz/quiz_detail.html', {'quiz': quiz})


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
                answer_selected = data.get(q.content.replace('"', ''))
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
            Result.objects.update_or_create(quiz=quiz, user=user,
                                            defaults={
                                                'score': (score / quiz.number_of_questions),
                                                'date': timezone.now()})
            return JsonResponse({'results': results, 'score': score})


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OwnerQuizMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Quiz
    fields = ['category', 'title', 'description', 'time']
    success_url = reverse_lazy('quiz_manage_list')


class OwnerQuizEditMixin(OwnerQuizMixin, OwnerEditMixin):
    template_name = 'quizzes/manage/quiz/form.html'


class ManageQuizListView(OwnerQuizMixin, ListView):
    template_name = 'quizzes/manage/quiz/list.html'
    permission_required = 'quiz_app.view_quiz'
    context_object_name = 'quizzes'


class CreateQuizView(OwnerQuizEditMixin, CreateView):
    permission_required = 'quiz_app.add_quiz'


class UpdateQuizView(OwnerQuizEditMixin, UpdateView):
    permission_required = 'quiz_app.change_quiz'


class DeleteQuizView(OwnerQuizEditMixin, DeleteView):
    template_name = 'quizzes/manage/quiz/delete.html'
    permission_required = 'quiz_app.delete_quiz'


class QuizQuestionsUpdateView(TemplateResponseMixin, View):
    template_name = 'quizzes/manage/questions/formset.html'
    quiz = None

    def get_formset(self, data=None):
        return QuestionFormSet(instance=self.quiz,
                             data=data)

    def dispatch(self, request, pk, slug):
        self.quiz = get_object_or_404(Quiz, id=pk, slug=slug, author=request.user)
        return super().dispatch(request, pk, slug)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'quiz': self.quiz,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('quiz_manage_list')
        return self.render_to_response({'quiz': self.quiz,
                                        'formset': formset})


