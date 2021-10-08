from django.db import models

from quizzer import settings


class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name', ]


class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=128)
    description = models.TextField()
    number_of_questions = models.SmallIntegerField(default=1)
    time = models.SmallIntegerField(default=100, help_text="Duration of the quiz [s]")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes_created")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created', ]


class Question(models.Model):
    content = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/%Y/%m/%d')
    quizzes = models.ManyToManyField(Quiz, related_name="questions")
    order = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['order']


class Answer(models.Model):
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"Question: {self.question}, answer: {self.content}, is_correct: {self.is_correct}"


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()

    def __str__(self):
        return f"Wynik użytownika {self.user.username} w quizie {self.quiz}: {self.score}"


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
