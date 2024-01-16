from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from quizzes.models import Quiz, Category, Question, Choice, UserQuizHistory
from django.contrib.auth.models import User
from django.core.mail import send_mail
from QuizMaster.settings import EMAIL_HOST_USER


def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # print(quiz)
    questions = Question.objects.filter(quiz=quiz)
    # print(questions)

    if request.method == 'POST':
        # Handle form submission for each question
        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(
                f'question_{question.id}_choice')
            print(
                f"Question ID: {question.id}, Selected Choice ID: {selected_choice_id}")
            
            # Print the IDs of all choices for debugging
            for choice in question.choice_set.all():
                print(f"Choice ID: {choice.id}")

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


def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_quiz_history = UserQuizHistory.objects.filter(
        user=request.user, quiz=quiz).latest('completed_at')

    context = {
        'quiz': quiz,
        'user_quiz_history': user_quiz_history,
    }
    return render(request, 'quiz_result.html', context)


def quiz_history(request, username):
    user = get_object_or_404(User, username=username)
    quiz_history = UserQuizHistory.objects.filter(
        user=user).order_by('-completed_at')

    context = {
        'user': user,
        'quiz_history': quiz_history,
    }

    return render(request, 'quiz_history.html', context)

def home(request, category_slug=None):
    categories = Category.objects.all()
    selected_category = None
    quizzes = Quiz.objects.all()

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        quizzes = Quiz.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'quizzes': quizzes,
        'selected_category': selected_category,
    }

    return render(request, 'home.html', context)

def home(request, category_slug=None):
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