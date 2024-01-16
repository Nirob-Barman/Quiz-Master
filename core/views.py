from django.shortcuts import render, redirect
from quizzes.models import Quiz, Category, Question, Choice, UserQuizHistory


def home(request, category_slug=None):
    categories = Category.objects.all()
    quizzes = Quiz.objects.all()
    # question = Question.objects.all()
    # quizzes = Quiz.objects.none()
    # print(question)

    # for quiz in quizzes:
    #     print('quiz',quiz.category.name)

    selected_category = None
    if category_slug:
        # print(category_slug)
        selected_category = Category.objects.get(slug=category_slug)
        print(selected_category)
        quizzes = quizzes.filter(category=selected_category)

    # Get all questions and choices for the quizzes
    quiz_data = []
    for quiz in quizzes:
        quiz_questions = Question.objects.filter(quiz=quiz)
        questions_data = []

        for question in quiz_questions:
            choices_data = Choice.objects.filter(question=question)
            questions_data.append({
                'question_text': question.quizQuestion,
                'choices': choices_data
            })

        quiz_data.append({
            'quiz_title': quiz.title,
            'quiz_description': quiz.description,
            'questions': questions_data
        })

    context = {
        'categories': categories,
        # 'quizzes': quizzes,
        'quizzes': quiz_data,
        'selected_category': selected_category,
    }
    # context = {
    #     'categories': categories,
    #     'quizzes': quizzes,
    #     # 'quizzes': quiz_data,
    #     'selected_category': selected_category,
    # }

    return render(request, 'home.html', context)
