from django.forms import inlineformset_factory, formset_factory

from quiz_app.models import Quiz, Question, Answer

QuestionFormSet = inlineformset_factory(Quiz, Question,
                                        fields=['content', 'image'],
                                        extra=4,
                                        can_delete=True)

AnswerFormSet = inlineformset_factory(Question, Answer,
                                      fields=['content', 'is_correct'],
                                      extra=3,
                                      can_delete=True)
