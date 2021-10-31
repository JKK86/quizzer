from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory, BaseFormSet, BaseInlineFormSet

from quiz_app.models import Quiz, Question, Answer


class BaseAnswerInlineFormset(BaseInlineFormSet):
    def clean(self):
        """Checks that only one answer is correct"""
        if any(self.errors):
            return
        correct_answers = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            is_correct = form.cleaned_data.get('is_correct')
            if is_correct:
                correct_answers.append(is_correct)
        if len(correct_answers) != 1:
            raise ValidationError("Jako poprawną należy oznaczyć jedną odpowiedź")


QuestionFormSet = inlineformset_factory(Quiz, Question,
                                        fields=['content', 'image'],
                                        extra=4,
                                        can_delete=True)

AnswerFormSet = inlineformset_factory(Question, Answer,
                                      formset=BaseAnswerInlineFormset,
                                      fields=['content', 'is_correct'],
                                      extra=4,
                                      can_delete=True)
