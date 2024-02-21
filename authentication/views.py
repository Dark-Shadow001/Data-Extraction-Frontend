from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from rest_framework import status
from django.contrib.auth import authenticate, login
from user.models import CustomUser
import json
import requests
import uuid
from .exceptions import RegistrationFailException
import smtplib
from email.mime.text import MIMEText
from .models import OTP
from argon_drf_server.settings import BASE_URL, sender_email, sender_password
from django.contrib.auth.hashers import make_password

# Create your views here.


def checkValidEmail(email):
    api_key = "010030fd16074f02afa169eace9f581e"
    try:
        response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}")

        if response.status_code == 200:
            data = response.json()
            return data["deliverability"] == "DELIVERABLE" and data["is_valid_format"]["value"] == True and data["is_disposable_email"]["value"] == False
        
        else:
            return False
            
    except:
        return False
    # return True


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    # msg['To'] = ', '.join(recipients)
    msg['To'] = recipients
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


class DemoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello! This is a Demo!'}
        return Response(content)


class LoginView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        username = body["username"]
        password = body["password"]

        if not username or not password:
            raise exceptions.AuthenticationFailed('No credentials found')

        try:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
            else:
                raise exceptions.AuthenticationFailed('No such user')
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return Response({
            'token': token.key,
            'username': user.username
        })


class RegistrationView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        username = body["username"]
        email = body["email"]
        password = body["password"]

        if not username or not password or not email:
            raise Exception('Not adequate data to register user.')

        try:
            if checkValidEmail(email):
                users = CustomUser.objects.filter(username=username)
                if len(users) > 0:
                    return Response({'statusText': 'Registration Failed.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                CustomUser.objects.create_user(
                    username=username, email=email, password=password, is_superuser=False, updated_by=username)
            else:
                return Response({
                    'message': 'Email associated with this account is not valid. Please contact customer support.'
                }, status=status.HTTP_403_FORBIDDEN)
        except:
            Response({
                'statusText': 'Registration Failed.'
            }, status=status.HTTP_409_CONFLICT)

        return Response({
            'message': 'User registered successfully.'
        })


class ResetPasswordEmailView(APIView):

    def post(self, request):
        body = json.loads(request.body)
        username = body["username"]
        # to generate the email for the user to reset password, need to validate email
        subject = "Campaign Kart Account Password Reset"
        message = "Link to reset your password : {link}"

        try:
            user = CustomUser.objects.filter(username=username)
            if len(user) == 0:
                raise 'No user found with given username.'

            if checkValidEmail(user.email):
                send_email(subject,
                        message.format(BASE_URL+'/resetpasswordform/'+username),
                        sender_email,
                        user.email,
                        sender_password)
            else:
                return Response({
                    'message': 'Email associated with this account is not valid. Please contact customer support.'
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({
                'message': 'Error while sending email.'
            }, status=status.HTTP_409_CONFLICT)

        return Response({
            'message': 'Reset password email sent.'
        })


class ResetPasswordFormView(APIView):

    def get(self, request, username):
        return render(request, 'resetPassword.html', {'username': username, 'BASE_URL': BASE_URL})


class ResetPasswordView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        username = body["username"]
        password = body["password"]

        try:
            user = CustomUser.objects.filter(username=username)[0]
            user.password = make_password(password)
            user.save()
        except:
            return Response({
                "status": 400,
                'message': 'Error resetting Password.'
            })

        return Response({
            'message': 'Password resetted successfully.'
        })


class GenerateOTP(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        print('---', user)
        try:
            key = str(uuid.uuid4())
            OTP.objects.create(otp_key=key, user_id=user.userId)
        except:
            return Response({
                "status": 400,
                'message': "Error creating OTP."
            })

        message = "Your email verification link : {link}"
        subject = "Campaign Kart Account Verification"
        print('hello')
        try:
            if checkValidEmail(user.email):  # condition to check email valid or not
                send_email(subject,
                        message.format(link=BASE_URL+'/validateOTP/'+key),
                        sender_email,
                        user.email,
                        sender_password)
            else:
                return Response({
                    'message': 'Please Enter a valid email.'
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception:
            return Response({
                "status": 400,
                'message': "Error while sending email."
            })

        return Response({
            'message': "Email Sent Successfully."
        })


class ValidateOTP(APIView):

    def get(self, request, otpId):
        try:
            otpObject = OTP.objects.filter(otp_key=otpId)[0]
            userId = otpObject.user_id
            user = CustomUser.objects.filter(
                userId=userId)[0]
            user.email_validation = True
            user.save()
            otpObject.delete()
        except Exception:
            return render(request, 'emailValidationFailed.html')

        return render(request, 'emailValidationSuccess.html')
