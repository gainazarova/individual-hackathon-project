from cinema.celery import app
from django.core.mail import send_mail


@app.task
def send_activation_code(email, code):
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email = email
    send_mail(
        'Здравствуйте, активируйте свой аккаунт!',
        f' Чтобы активировать ваш аккаунт нужно перейти по ссылке: {full_link} ', 'from@example.com', [to_email, ],
        fail_silently=False,
    )
