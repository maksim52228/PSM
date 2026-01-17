from django.shortcuts import render, redirect
from .models import News
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import  get_object_or_404

from django.contrib import messages as django_messages
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from .models import ChatMessage
from django.views.generic import ListView, DetailView
from .models import Employee,Works
from django.core.paginator import Paginator
from .forms import ChatMessageForm

def about(request):
    # Расчет времени работы компании
    foundation_date = datetime(2016, 5, 15)
    current_date = datetime.now()
    delta = current_date - foundation_date

    context = {
        'years': delta.days // 365,
        'months': (delta.days % 365) // 30,
        'days': (delta.days % 365) % 30,
        'total_days': delta.days
    }
    return render(request, "myapp/home.html", context)



def send_application_to_admin(application):
    try:
        email = EmailMessage(
            subject=f'Новая заявка от {application.name}',
            body=f"""
            Имя: {application.name}
            Email: {application.email}
            Сообщение:
            {application.description}

            Дата: {application.created_at.strftime("%d.%m.%Y %H:%M")}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
            reply_to=[application.email],
        )
        email.send()
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False


def send_admin_message(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        email = request.POST.get('email', '').strip()

        if message and email:
            try:
                send_mail(
                    'Сообщение от пользователя',
                    f'Email: {email}\n\nСообщение:\n{message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                django_messages.success(request, 'Ваше сообщение отправлено администратору!')
            except Exception as e:
                django_messages.error(request, f'Ошибка отправки: {str(e)}')

        return redirect('chat')
def home(request):
    # Получаем последние 3 новости
    latest_news = News.objects.all().order_by('-date_posted')[:3]
    # Получаем опубликованные работы
    works = Works.objects.filter(is_published=True).order_by('order', '-created_at')  # например, последние 6 работ

    # Получаем опубликованных сотрудников
    employees = Employee.objects.filter(is_published=True).order_by('order')[:3]  # например, первых 3 сотрудника
    # Расчет времени работы компании
    foundation_date = datetime(2016, 5, 15)
    current_date = datetime.now()
    delta = current_date - foundation_date

    context = {
        'works': works,
        'employees': employees,
        'latest_news': latest_news,
        'years': delta.days // 365,
        'months': (delta.days % 365) // 30,
        'days': (delta.days % 365) % 30,
        'total_days': delta.days
    }
    return render(request, "myapp/home.html", context)

def news_list(request):
    news = News.objects.all().order_by('-date_posted')
    return render(request, 'myapp/news_list.html', {'news': news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'myapp/news_detail.html', {'news': news_item})


from .models import ChatMessage
from .forms import ChatMessageForm


def chat(request):
    # берём последние 50 сообщений (самые новые)
    messages_qs = ChatMessage.objects.all().order_by('-timestamp')[:50]

    # разворачиваем, чтобы в шаблоне были от старых к новым
    messages = reversed(messages_qs)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if 'chat_username' in request.session:
                message.username = request.session['chat_username']
                message.save()
                return redirect('chat')
    else:
        form = ChatMessageForm()

    return render(request, 'myapp/chat.html', {
        'messages': messages,
        'form': form
    })


def set_chat_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if len(username) >= 2:
            request.session['chat_username'] = username
            return redirect('chat')
    return redirect('chat')




def team_view(request):
    employees = Employee.objects.filter(is_published=True).order_by('order')
    return render(request, 'myapp/home.html', {'employees': employees})
def works(request):
    works = Works.objects.filter(is_published=True).order_by('order', '-created_at')
    paginator = Paginator(works, 100)  # По 9 работ на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/works.html', {
        "works": page_obj,
        "page_obj": page_obj  # Для пагинации
    })
from django.http import HttpResponse
def yandex_verification(request):
    return HttpResponse(
        "Verification: ff639d9ed0973929",
        content_type="text/plain"
    )