import pytest


@pytest.mark.django_db
def test_list_quizzes(client, set_up):
    response = client.get('/')
    assert response.status_code == 200
    assert len(set_up[0]) == len(response.context['categories'])
    assert len(set_up[1]) == len(response.context['quizzes'])
