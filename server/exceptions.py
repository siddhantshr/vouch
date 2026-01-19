from rest_framework.exceptions import APIException


class ConflictError(APIException):
    status_code = 409
    default_detail = "Conflict with current resource state."
    default_code = "conflict"
