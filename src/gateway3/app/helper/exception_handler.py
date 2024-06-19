from ..helper.custom_response import CustomResponse


def handle_exception_function(error):
    if hasattr(error, 'code'):  # HTTPException
        response = CustomResponse(
            succeeded=False, message=str(error), status=500)
    else:  # Non-HTTP exceptions
        response = CustomResponse(
            succeeded=False, message=str(error), status=500)
    return response
