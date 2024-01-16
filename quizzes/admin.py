from django.contrib import admin
from .models import Category, Quiz, QuizRating, Question, Choice, UserQuizHistory

# Register your models here.


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'question_count')

    def question_count(self, obj):
        return obj.questions.count()

    question_count.short_description = 'Number of Questions'

admin.site.register(Quiz, QuizAdmin)


admin.site.register(QuizRating)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ChoiceAdmin(admin.StackedInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceAdmin]
    extra = 1  # Number of choices to display for each question
    list_display = ('category', 'quizQuestion', 'quizMark')
    ordering = ('quiz__category__name', 'id')

    def category(self, obj):
        # return obj.question.quiz.category.name
        return obj.quiz.category


admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    # list_display = ('category', 'question', 'quizAnswer', 'is_correct')
    list_display = ('category', 'question', 'quizAnswer')
    list_filter = ('is_correct',)
    ordering = ('question__quiz__category__name', 'question__id')

    def category(self, obj):
        # return obj.question.quiz.category.name
        return obj.question.quiz.category

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_correct=True)
    
    category.admin_order_field = 'question__quiz__category__name'


admin.site.register(Choice, ChoiceAdmin)

admin.site.register(UserQuizHistory)

