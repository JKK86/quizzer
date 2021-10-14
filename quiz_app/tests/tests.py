import pytest


@pytest.mark.django_db
def test_list_quizzes(client, set_up):
    response = client.get('/')
    assert response.status_code == 200
    assert len(set_up[0]) == len(response.context['categories'])
    assert len(set_up[1]) == len(response.context['quizzes'])


@pytest.mark.django_db
def test_list_quizzes_by_category(client, set_up):
    category = set_up[0][0]
    response = client.get(f'/{category.slug}/')
    assert response.status_code == 200
    assert category.quizzes.count() == len(response.context['quizzes'])