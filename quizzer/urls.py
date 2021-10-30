"""quizzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from quiz_app import views as quiz_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('users.urls')),

    path('', quiz_views.QuizListView.as_view(), name="quiz_list"),

    path('manage/', quiz_views.ManageQuizListView.as_view(), name="quiz_manage_list"),
    path('create/', quiz_views.CreateQuizView.as_view(), name="quiz_create"),
    path('edit/<int:pk>/<slug:slug>/', quiz_views.UpdateQuizView.as_view(), name="quiz_edit"),
    path('delete/<int:pk>/<slug:slug>/', quiz_views.DeleteQuizView.as_view(), name="quiz_delete"),

    path('quiz/<int:pk>/<slug:slug>/questions/', quiz_views.QuizQuestionsUpdateView.as_view(),
         name="quiz_questions_update"),

    path('<slug:category_slug>/', quiz_views.QuizListView.as_view(), name="quiz_list_by_category"),
    path('<int:quiz_id>/<slug:quiz_slug>/', quiz_views.QuizDetailView.as_view(), name="quiz_detail"),
    path('<int:quiz_id>/<slug:quiz_slug>/data', quiz_views.QuizDataView.as_view(), name="quiz_data"),
    path('<int:quiz_id>/<slug:quiz_slug>/save', quiz_views.QuizDataSaveView.as_view(), name="quiz_save"),
]
