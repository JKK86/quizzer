from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from .fields import OrderField

from quizzer import settings


class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name', ]

    def get_absolute_url(self):
        return reverse('quiz_list_by_category', args={self.slug})


class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True)
    description = models.TextField()
    time = models.SmallIntegerField(default=0, help_text="Duration of the quiz [s]")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name="quizzes_created")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created', ]

    def get_absolute_url(self):
        return reverse('quiz_detail', args=[self.id, self.slug])

    @property
    def number_of_questions(self):
        return self.questions.count()

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #         super().save(*args, **kwargs)


@receiver(pre_save, sender=Quiz)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions", blank=True, null=True)
    content = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/%Y/%m/%d')
    quizzes = models.ManyToManyField(Quiz, related_name="questions", through="QuestionOrder")

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"Question: {self.question}, answer: {self.content}, is_correct: {self.is_correct}"


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.DecimalField(max_digits=3, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wynik użytownika {self.user.username} w quizie {self.quiz}: {self.score}"

    def get_score_percentage(self):
        return f'{self.score:.0%}'

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'quiz'], name='unique_result')]


class Comment(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created', ]


class QuestionOrder(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['quiz'])

    class Meta:
        ordering = ['quiz', 'order', ]

    def __str__(self):
        return f"{self.order}.{self.question}"
