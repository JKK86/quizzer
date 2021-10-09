import random

import pytest
from django.contrib.auth import get_user_model

from quiz_app.models import Category, Quiz

User = get_user_model()


@pytest.fixture
def create_test_user():
    return User.objects.create_user('Test_user', 'user@test.com', 'test')


@pytest.fixture
def set_up():
    quizzes = []
    categories = []

    for i in range(3):
        categories.append(Category.objects.create(
            name=f"Kategoria testowa {i}",
            slug=f"kategoria-testowa-{i}"
        ))

    for i in range(5):
        quizzes.append(Quiz.objects.create(
            category=random.choice(categories),
            title=f"Quiz testowy {1}",
            description=f"Opis quizu testowego {1}",
            number_of_questions=random.randint(1, 10),
            time=random.randint(60, 120),
            author=create_test_user,
        ))

    return [categories, quizzes]
