from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import json
from .models import Contact
from datetime import datetime

# Create your views here.


def render_react(request):
    return render(request, "index.html")


class FetchUserDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user

        return Response({
            'username': user.username,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'email_validation': user.email_validation,
            'phone': user.phone,
            "organization_name": user.organization.organization_name,
            "organization_name": user.organization.organization_name,
            "organization_id": user.organization.organization_id,
            "subscription_active": user.organization.is_subscrition_active,
            "subscription_start_date": user.organization.subscription_start_date,
            "subscription_end_date": user.organization.subscription_end_date
        })


class UpdateUserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        body = json.loads(request.body)
        first_name = body["first_name"]
        last_name = body["last_name"]
        email = body["email"]
        phone = body["phone"]
        mail_changed = body["mail_changed"]
        updated_by = body["updated_by"]

        user = Token.objects.get(key=request.auth.key).user

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone = phone
            user.email_validation = False if mail_changed else user.email_validation
            user.updated_by = updated_by
            user.updated_at = datetime.utcnow()
            user.save()
        except:
            return Response(status=400, data={
                'message': 'Error in updation.'
            })

        return Response({
            'message': 'Updated Successfully.'
        })


class AddContactDetails(APIView):
    def post(self, request):
        body = json.loads(request.body)
        first_name = body["first_name"]
        last_name = body["last_name"]
        email = body["email"]
        phone = body["phone"]
        company = body["company"]
        projectTypeProduct = body["projectTypeProduct"]
        message = body["message"]
        subscription = body["subscribed"]

        try:
            Contact.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                   product=projectTypeProduct, company=company, message=message, monthly_subscription=subscription)
        except:
            return Response(status=400, data={
                'message': 'Error in saving data.'
            })

        return Response({
            'message': 'Your message saved successfully.'
        })
