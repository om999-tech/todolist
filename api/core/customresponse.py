from fastapi.responses import JSONResponse
import datetime
from fastapi import HTTPException,status
from fastapi import Request
from typing import Optional,Dict,Any
import pytz
import datetime as dt

class CustomResponse(JSONResponse):
    """
    A custom JSONResponse for FastAPI that allows including additional response data 
    and handling error messages with specific flags.
    """

    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
        status: Optional[int] = 400,
        headers: Optional[Dict[str, str]] = None,
        already_exist: Optional[bool] = False,
        validate_errors: Optional[bool] = False,
        extra_params: Optional[Dict[str, Any]] = None,
        success: Optional[bool] = False,
    ):
        if status==200:
            success = True
        # Prepare the response body
        response_content = {
            "status_code": status,
            "message": message or "",
            "data": data if data else None,
            "status": not (validate_errors or already_exist),
            "success":success,
            "currentTimeStamp": pytz.utc.localize(dt.datetime.utcnow()).isoformat(),
        }
      

        # Handle validation errors or already existing records
        if validate_errors or already_exist:
            response_content["status"] = False
            if isinstance(data, dict):
                error_messages = [str(value[0]) for value in data.values() if isinstance(value, list)]
                response_content["message"] = "; ".join(error_messages) if error_messages else message

        # Add any extra parameters to the response
        if extra_params:
            response_content.update(extra_params)

        # Pass the response content to JSONResponse
        super().__init__(content=response_content, status_code=status, headers=headers)
