from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .constants import RATING_RANGE
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
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='quizzes/media/uploads', null=True,
                              blank=True, help_text='Upload an image for the quiz')
    banner = models.ImageField(upload_to='quizzes/media/uploads', null=True,blank=True)

    def __str__(self):
        return self.title
        # return f'{self.title} - {self.questions.count()} questions'
    
    # def clean(self):
    #     # Ensure the quiz has at least 5 and at most 50 questions
    #     min_questions = 5
    #     max_questions = 50
        
    #     if self.questions.count() < min_questions:
    #         raise ValidationError(f'A quiz must have at least {min_questions} questions.')
    #     if self.questions.count() > max_questions:
    #         raise ValidationError(f'A quiz cannot have more than {max_questions} questions.')



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
        return f'{self.question.quizQuestion} --||-- {self.quizAnswer}'


class UserQuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    totalMarks = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    selected_choices = models.ManyToManyField(
        Choice, related_name='selected_choices', blank=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return self.user.username
