import asyncio
import telegram
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect

from OnlineStore.settings import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from checkout.models import Order
from .forms import CreationForm, FeedbackForm, ProfileForm
from .models import Feedback


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


@login_required
def user_orders(request):
    """
    Представление списка заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'users/user_orders.html', context)


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('store:home')
    template_name = 'users/signup.html'


async def send_telegram_message(message):
    """
    Асинхронная функция для отправки сообщения в ТГ.
    """
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    chat_id = TELEGRAM_CHAT_ID
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except telegram.TelegramError as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


@csrf_protect
def feedback_processing(request):
    """
    Представление приема и обработки для обратной связи.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                feedback_name=form.cleaned_data['feedback_name'],
                feedback_email=form.cleaned_data['feedback_email'],
                feedback_message=form.cleaned_data['feedback_message'],
            )
            feedback.save()

            # Отправка сообщения
            message = f"Новое сообщение от {feedback.feedback_name} ({feedback.feedback_email}): {feedback.feedback_message}"
            asyncio.run(send_telegram_message(message))

            return render(request, 'users/feedback_success.html')
    else:
        form = FeedbackForm()
    return render(request, 'users/feedback_failed.html', {'form': form})