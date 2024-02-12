from django.shortcuts import render, redirect
from .models import Category, Movie
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.db import IntegrityError


# Create your views here.

# Основная страница
def home(request):
    # Поисковая строка
    search_bar = forms.SearchForm()
    # Получение всех категорий
    category = Category.objects.all()
    # Получение всех фильмов
    movie = Movie.objects.all()
    context = {
        'form': search_bar,
        'category': category,
        'movie': movie
    }
    return render(request, 'home.html', context)


# Получение информации о категориях
def exact_category(request, pk):
    all_category = Category.objects.get(id=pk)
    movies = Movie.objects.filter(category=all_category)
    context = {
        'movies': movies
    }
    return render(request, 'category.html', context)


# Получение информации о фильмах
def exact_movie(request, pk):
    # Получения всех фильмов
    all_movie = Movie.objects.get(id=pk)
    context = {
        'movie': all_movie
    }
    return render(request, 'movie.html', context)


# Информация о контактах
def contact(request):
    return render(request, 'contact.html')


# Информация о проекте
def about(request):
    return render(request, 'about.html')


# Поиск фильмов
def search_engine(request):
    if request.method == 'POST':
        get_movie = request.POST.get('search_engine')
        try:
            specific_movie = Movie.objects.get(name__icontains=get_movie)
            return redirect(f'/movie/{specific_movie.id}')
        except:
            return redirect('/error')


# Страница ошибки
def error(request):
    return render(request, 'error.html')


# # Регистрация
# class Register(View):
#     template_name = 'registration/register.html'
#
#     # Отправка формы регистрации
#     def get(self, request):
#         context = {'form': UserCreationForm}
#         return render(request, self.template_name, context)
#
#     # Добавление в БД
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('/')
#         context = {'form': UserCreationForm}
#         return render(request, self.template_name, context)


# Функция для logout
def logout_view(request):
    logout(request)
    return redirect('/')


# # Функция для Login
# def login_page(request):
#     # Проверка отправки данных
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password1')
#
#         # Проверяем существует ли пользователь
#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, "Пользователь не существует! Зарегистрируйтесь!")
#
#         # Проверка введенных данных
#         user = authenticate(request, username=username, password=password)
#
#         # Регистрация
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             messages.error(request, "Имя пользователя или пароль не совпадают")
#
#     context = {}
#     return render(request, 'registration/login.html', context)


# Для регистрации пользователя или входа в их аккаунт
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверка пользователя в базе
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html',
                          {'error': 'Хм! Я думаю вы уже зарегистрированы. Попробуйте войти!'})

        try:
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user)
            authenticated_user = authenticate(request, username=username, password=password)
            login(request, authenticated_user)
            return redirect('/')
        except IntegrityError:
            return render(request, 'registration/register.html',
                          {'error': 'Данные введены неправильно! Попробуйте ещё раз!'})
    return render(request, 'registration/register.html')
