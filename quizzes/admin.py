from django.contrib import admin
from .models import Category, Quiz, QuizRating, Question, Choice, UserQuizHistory

# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizRating)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ChoiceAdmin(admin.StackedInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceAdmin]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

admin.site.register(UserQuizHistory)

# from django.contrib import admin
# from .models import Category, Question, Answer

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('category_name',)}
# admin.site.register(Category, CategoryAdmin)


# class AnswerAdmin(admin.StackedInline):
#     model = Answer

# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [AnswerAdmin]

# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Answer)
