from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from quizzes.models import Quiz, Category, Question, Choice, UserQuizHistory
from django.contrib.auth.models import User
from django.core.mail import send_mail
from QuizMaster.settings import EMAIL_HOST_USER
from django.db.models import Count, Q
from quizzes.forms import QuizRatingForm
from quizzes.models import QuizRating
from django.contrib.auth.decorators import login_required, user_passes_test


def quiz_view(request, category_slug):
    # Assuming you have a Category model with a 'slug' field
    category = get_object_or_404(Category, slug=category_slug)

    # Assuming you have a Quiz model with a 'category' field
    quiz = get_object_or_404(Quiz, category=category)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        # Handle form submission for each question
        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(
                f'question_{question.id}_choice')

            selected_choice = get_object_or_404(Choice, id=selected_choice_id)

            # Check if the selected choice is correct
            if selected_choice.is_correct:
                score += 1

        # Save user quiz history
        user_quiz_history = UserQuizHistory(
            user=request.user, quiz=quiz, score=score)
        user_quiz_history.save()

        # Send email to the user
        subject = 'Quiz Completion'
        message = f'Thank you for completing the quiz "{quiz.title}". Your score is {score}/{len(questions)}.'
        from_email = EMAIL_HOST_USER
        recipient_list = [request.user.email]

        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        return redirect('quiz_result', quiz_id=quiz.id)

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz.html', context)

# def quiz_view(request, quiz_id):
#     quiz = get_object_or_404(Quiz, id=quiz_id)
#     print(quiz)
#     questions = Question.objects.filter(quiz=quiz_id)
#     print(questions)

#     if request.method == 'POST':
#         # Handle form submission for each question
#         score = 0
#         for question in questions:
#             selected_choice_id = request.POST.get(
#                 f'question_{question.id}_choice')
#             print(
#                 f"Question ID: {question.id}, Selected Choice ID: {selected_choice_id}")

#             # Print the IDs of all choices for debugging
#             for choice in question.choice_set.all():
#                 print(f"Choice ID: {choice.id}")

#             selected_choice = get_object_or_404(Choice, id=selected_choice_id)

#             # Check if the selected choice is correct
#             if selected_choice.is_correct:
#                 score += 1

#         # Save user quiz history
#         user_quiz_history = UserQuizHistory(
#             user=request.user, quiz=quiz, score=score)
#         user_quiz_history.save()

#         # Send email to the user
#         subject = 'Quiz Completion'
#         message = f'Thank you for completing the quiz "{quiz.title}". Your score is {score}/{len(questions)}.'
#         from_email = EMAIL_HOST_USER
#         recipient_list = [request.user.email]

#         send_mail(subject, message, from_email,
#                   recipient_list, fail_silently=False)

#         return redirect('quiz_result', quiz_id=quiz.id)

#     context = {
#         'quiz': quiz,
#         'questions': questions,
#     }
#     return render(request, 'quiz.html', context)


def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_quiz_history = UserQuizHistory.objects.filter(
        user=request.user, quiz=quiz).latest('completed_at')

    context = {
        'quiz': quiz,
        'user_quiz_history': user_quiz_history,
    }
    return render(request, 'quiz_result.html', context)


@login_required
def rate_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuizRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            QuizRating.objects.create(
                user=request.user, quiz=quiz, rating=rating)
            # return redirect('quiz_view', quiz_id=quiz.id)
            return redirect('rating_history')
    else:
        form = QuizRatingForm()

    context = {
        'quiz': quiz,
        'form': form,
    }

    return render(request, 'rate_quiz.html', context)


def rating_history(request):
    # Get all ratings
    all_ratings = QuizRating.objects.all()

    context = {
        'all_ratings': all_ratings,
    }

    return render(request, 'rating_history.html', context)


@user_passes_test(lambda u: u.is_staff)
def delete_rating(request, rating_id):
    rating = get_object_or_404(QuizRating, id=rating_id)
    rating.delete()
    return redirect('rating_history')

def quiz_history(request, username):
    user = get_object_or_404(User, username=username)
    quiz_history = UserQuizHistory.objects.filter(
        user=user).order_by('-completed_at')

    context = {
        'user': user,
        'quiz_history': quiz_history,
    }

    return render(request, 'quiz_history.html', context)


def leaderboard(request):
    # Get top scores from UserQuizHistory
    top_scores = UserQuizHistory.objects.order_by('-score')[:10]

    context = {
        'top_scores': top_scores,
    }

    return render(request, 'leaderboard.html', context)


def remove_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Perform any additional logic before deleting the user

    user.delete()
    return redirect('list_profiles')

# def home(request, category_slug=None):
#     categories = Category.objects.all()
#     selected_category = None
#     quizzes = Quiz.objects.all()

#     if category_slug:
#         selected_category = get_object_or_404(Category, slug=category_slug)
#         quizzes = Quiz.objects.filter(category=selected_category)

#     context = {
#         'categories': categories,
#         'quizzes': quizzes,
#         'selected_category': selected_category,
#     }

#     return render(request, 'home.html', context)


def home(request, category_slug=None):

    # Filter categories with at least one quiz having both title and description
    customizeCategories = Category.objects.annotate(
        quiz_count=Count('quiz', filter=Q(
            quiz__title__isnull=False, quiz__description__isnull=False))
    ).filter(quiz_count__gt=0)
    print(customizeCategories)

    categories = Category.objects.all()
    quizzes = Quiz.objects.all()

    selected_category = None
    if category_slug:
        # print(category_slug)
        selected_category = Category.objects.get(slug=category_slug)
        print(selected_category)
        quizzes = quizzes.filter(category=selected_category)

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
        'customizeCategories': customizeCategories,
        'quizzes': quizzes,
        # 'quizzes': quiz_data,
        'selected_category': selected_category,
    }
    # context = {
    #     'categories': categories,
    #     'quizzes': quizzes,
    #     # 'quizzes': quiz_data,
    #     'selected_category': selected_category,
    # }

    return render(request, 'home.html', context)
