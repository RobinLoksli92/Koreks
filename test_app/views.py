from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from rest_framework import viewsets

from .models import Test, Question, TestResult, User
from .serializers import TestSerializer, QuestionSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


def register(request):
    # Для ввода username`а.

    return render(request, template_name='register.html')


def get_test(request, test_number):
    # Прохождение теста, сохраняем промежуточную информацию в сессии пользователя.

    test = get_object_or_404(Test, test_number=test_number)
    questions = Question.objects.filter(test=test)

    if not 'username' in request.session:
        redirect('/')

    if not questions:
        request.session.clear()
        return HttpResponse('В тесте нет вопросов')

    if not 'question_number' in request.session:
        request.session['question_number'] = 0
        request.session['correct_answers'] = 0

    if len(questions) == request.session['question_number']:
        username = User.objects.get_or_create(username=request.session['username'])
        toughest_question = get_toughest_question(questions)
        result = TestResult(
            test=test,
            username=username[0],
            toughest_question=toughest_question
        )

        if questions[request.session['question_number'] - 1].answer == request.POST['answer']:
            request.session['correct_answers'] += 1
        succes_rate = request.session['correct_answers'] / len(questions) * 100
        result.succes_rate = succes_rate
        result.pass_number += 1
        result.save()
        request.session.clear()
        return HttpResponse('Конец Теста')

    current_question = questions[request.session['question_number']]

    if request.method == 'POST':
        user_answer = request.POST['answer']
        if user_answer in ['Yes', 'No']:
            if questions[request.session['question_number']].answer == user_answer:
                request.session['correct_answers'] += 1
            request.session['question_number'] += 1
    return render(
        request,
        template_name='test.html',
        context={
            'test_number': test_number,
            'question': current_question
        })

    
def get_tests(request):
    # Выводит список всех тестов, возможно только после ввода username.

    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        usernames = User.objects.values_list('username', flat=True)
        username = request.POST['username']
        if username in usernames:
            return redirect('/')
        User.objects.create(username=username)
        request.session['username'] = username
        return render(
            request,
            template_name='tests.html',
            context={'tests': Test.objects.all()}
        )
 

def get_toughest_question(questions):
    for index, question in enumerate(questions):
        if len(questions) == index:
            return toughest_question
        if index == 0:
            toughest_question = question
        elif question.level >= questions[index-1].level:
            toughest_question = question
        else:
            toughest_question = questions[index-1]

    return toughest_question


