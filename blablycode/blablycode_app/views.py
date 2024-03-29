from cProfile import Profile
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, TemplateView
from .forms import *
from django.contrib import messages
from  django.contrib.auth import login, logout
from django.urls import reverse_lazy
from .models import *


class Index(CreateView):
    '''Главная страница'''
    template_name = 'blablycode_app/index.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def register_page(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request=request, template_name='blablycode_app/register.html', context=context)


def login_page(request):
    '''Страница авторизации'''
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(request=request, template_name='blablycode_app/login.html', context=context)


def logout_page(request):
    '''Функция выхода из аккаунта'''
    logout(request)
    return redirect('home')


def courses_page(request):
    '''Страница курсов'''
    courses = Course.objects.all()
    categories = Category.objects.all()
    age = Age.objects.all()

    context = {'courses': courses, 'categories': categories, 'age': age}

    return render(request=request, template_name='blablycode_app/courses.html', context=context)


def get_courses_category(request, category_id):
    '''Страница для сортировки курсов по категориям'''
    courses = Course.objects.filter(course_category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    age = Age.objects.all()

    context = {'courses': courses, 'categories': categories, 'age': age, 'category': category}

    return render(request=request, template_name='blablycode_app/courses_category.html', context=context)


def get_courses_age(request, age_id):
    '''Страница для сортировки курсов по категориям'''
    courses = Course.objects.filter(course_age_id=age_id)
    categories = Category.objects.all()
    ages = Age.objects.all()
    age = Age.objects.get(pk=age_id)

    context = {'courses': courses, 'categories': categories, 'age': age, 'ages': ages}

    return render(request=request, template_name='blablycode_app/courses_age.html', context=context)


def open_course_page(request, course_id):
    '''Страница с уроками курса'''
    courses = Course.objects.all()
    course = Course.objects.get(pk=course_id)
    #lessons = Lesson.objects.all()
    lessons = Lesson.objects.filter(lesson_сourse_id=course_id)

    context = {'courses': courses, 'course': course, 'lessons': lessons}

    return render(request=request, template_name='blablycode_app/open_course.html', context=context)


class GetLesson(DetailView):
    '''Страница урока'''
    model = Lesson
    template_name = 'blablycode_app/lesson.html'
    context_object_name = 'lesson'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

def homework_page(request):
    '''Страница для подкрепления домашнего задания'''
    error = ''
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            new_homework = form.save(commit=False)
            new_homework.homework_author = request.user
            new_homework.save()
        else:
            error = 'Форма была неверной.'
    form = HomeworkForm()

    data = {
        'form': form,
        'error': error,    
    }
    return render(request=request, template_name='blablycode_app/homework.html', context=data)


class Compiler(TemplateView):
    '''Страница онлайн-компилятора'''
    template_name = "blablycode_app/compiler.html"


class PracticeMenu(TemplateView):
    '''Страница мобильной навигации для модуля практики'''
    template_name = "blablycode_app/practice_menu.html"


def exercises_page(request):
    '''Страница с задачими'''
    exercise = Exercise.objects.all()

    context = {'exercise': exercise,}

    return render(request=request, template_name='blablycode_app/exercise_list.html', context=context)


class GetExercise(DetailView):
    '''Страница с открытой задачей'''
    model = Exercise
    template_name = 'blablycode_app/exercise.html'
    context_object_name = 'exercise'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

def interview_page(request):
    '''Страница с задачими для собеседования'''
    interview = InterviewExercise.objects.all()

    context = {'interview': interview,}

    return render(request=request, template_name='blablycode_app/interview_list.html', context=context)


class GetInterview(DetailView):
    '''Страница с открытой задачей для собеседования'''
    model = InterviewExercise
    template_name = 'blablycode_app/interview.html'
    context_object_name = 'interview'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

def tech_task_page(request):
    '''Страница с техническими заданиями'''
    tech_task = TechTask.objects.all()

    context = {'tech_task': tech_task,}

    return render(request=request, template_name='blablycode_app/tech_task_list.html', context=context)


class GetTechTask(DetailView):
    '''Страница с открытым техническим заданием'''
    model = TechTask
    template_name = 'blablycode_app/tech_task.html'
    context_object_name = 'tech_task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    
    

def articles_page(request):
    '''Страница со статьями'''
    articles = Article.objects.all()

    context = {'articles': articles,}

    return render(request=request, template_name='blablycode_app/articles.html', context=context)


class GetArticle(DetailView):
    '''Страница с открытой статьей'''
    model = Article
    template_name = 'blablycode_app/article.html'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    