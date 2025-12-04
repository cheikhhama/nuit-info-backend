# # users/utils.py
# from django.core.mail import send_mail
# from django.conf import settings
# from django.urls import reverse
# from django.core.signing import dumps

# #def send_verification_email(user, request):
#     #
#     #token = dumps({'user_id': user.pk}, salt='email-confirm')
#     # بناء رابط التفعيل — تأكدي من domain/port إذا تعملين محليًا
#     #verify_path = reverse('users:verify-email')  # سنعرف هذا الurl لاحقًا
#     #url = f"{request.scheme}://{request.get_host()}{verify_path}?token={token}"
#     #subject = 'Activate your app account'
#    # message = f"Hi {user.username},\n\nPlease click the link below to verify your email and activate your account:\n\n{url}\n\nIf you didn't request this, ignore this email."
#     #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)