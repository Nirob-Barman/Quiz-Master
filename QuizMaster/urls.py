"""
URL configuration for QuizMaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, quiz_view, quiz_result, quiz_history, leaderboard, rate_quiz, rating_history, delete_rating, remove_user, QuizCreationContestView, generate_certificate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # path('category/<slug:category_slug>/', home, name='category_wise_quiz'),

    # path('quiz/<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('quiz/<slug:category_slug>/', quiz_view, name='quiz_view'),
    path('quiz/<int:quiz_id>/result/', quiz_result, name='quiz_result'),
    path('quiz_history/<str:username>/', quiz_history, name='quiz_history'),
    path('quiz/<int:quiz_id>/rate/', rate_quiz, name='rate_quiz'),
    path('rating_history/', rating_history, name='rating_history'),
    path('delete_rating/<int:rating_id>/', delete_rating, name='delete_rating'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('quiz_creation_contest/', QuizCreationContestView.as_view(),
         name='quiz_creation_contest'),
    path('generate_certificate/<int:history_id>/', generate_certificate, name='generate_certificate'),
    path('remove_user/<int:user_id>/', remove_user, name='remove_user'),
    path('accounts/', include('accounts.urls')),
    # path('core/', include('core.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
