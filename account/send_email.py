from django.core.mail import send_mail


def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    to_email = user.email
    send_mail(
        'Hi, please activate your account!',
        f'Follow the link to activate: {full_link}',
        'cinema_db@cinema_db.com',
        [to_email],
        fail_silently=False,
    )


def send_reset_password_email(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        'Password reset',
        f'Your code: {code}',
        'cinema_db@cinema_db.com',
        [to_email],
        fail_silently=False,
    )
