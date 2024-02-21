from rest_framework.exceptions import APIException


class RegistrationFailException(APIException):
    status_code = 405
    default_detail = 'Error in user registration.'
    default_code = 'registration_fail'
