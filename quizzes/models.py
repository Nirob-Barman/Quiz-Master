from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    has_time_limit = models.BooleanField(default=False)

    def __str__(self):
        return self.title


RATING_RANGE = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
]

class QuizRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # rating = models.PositiveIntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(7)])
    rating = models.PositiveIntegerField(choices=RATING_RANGE)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - {self.rating}'


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions', default=1)
    quizQuestion = models.CharField(max_length=255)
    quizMark = models.IntegerField(default=1)

    def __str__(self):
        return self.quizQuestion


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quizAnswer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        # return self.quizAnswer
        return f'{self.question.quizQuestion} - {self.quizAnswer}'


class UserQuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
