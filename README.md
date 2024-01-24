# MindMazeQuiz

## Overview

This project aims to implement a comprehensive Quiz Management System with user authentication, quiz creation, quiz taking, user progress tracking, quiz categories and filtering, and quiz ratings. The system is designed to provide a seamless experience for both administrators and users.

## Features

### User Authentication

- **Registration:**
  - Users can register for an account.
  - Email verification is required for account activation.

- **Login:**
  - Registered users can log in to their accounts securely.

- **Logout:**
  - Users can log out of their accounts.

- **Profile Management:**
  - Admins and viewers have access to user profile management.

### Quiz Creation (Admin)

- **Create Quizzes:**
  - Admins can create quizzes with titles, descriptions, and categories.
  <!-- - Option to set a time limit for quizzes. -->

- **Add Questions:**
  - Admins can add multiple-choice questions to quizzes.
  - Each quiz should have at least 5 and at most 50 questions.
  - Each question should have 2 to 10 multiple-choice fields.

- **Specify Correct Answers:**
  - Admins can specify correct answers and point values for each question.

### Quiz Taking

- **Browse and Select Quizzes:**
  - Users can browse and select quizzes to take.

- **Take Quizzes:**
  - Questions are displayed one at a time for multiple-choice questions.
  - Immediate feedback on correct/incorrect answers is provided.

- **Calculate and Display Final Score:**
  - The system calculates and displays the final score at the end of the quiz.

- **Email Quiz Information:**
  - Users receive an email with quiz information, including the quiz score.

### User Progress

- **Track Quiz History:**
  - Display a user's quiz history, including completed quizzes and scores.

- **Progress Indicators:**
  - Show progress indicators for ongoing quizzes (progress bar or numerical).

- **Leaderboards:**
  - Display leaderboards for top scores in quizzes.

### Quiz Categories and Filtering

- **Categorize Quizzes:**
  - Quizzes are categorized by different topics or subjects.

- **Filter Quizzes:**
  - Users can filter quizzes based on categories.

### Quiz Ratings

- **Leave Ratings:**
  - Users can leave ratings for quizzes.

- **Display Average Ratings:**
  - Average ratings are displayed for each quiz.

- **Sort Quizzes by Rating:**
  - Quizzes can be sorted based on user ratings (from 1 to 7).
