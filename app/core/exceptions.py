from typing import Any, Dict, Optional

from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(
            self,
            status_code: int,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:

        if isinstance(detail, str):
            new_detail = {
                'type': 'custom_error',
                'code': status_code,
                'msg': detail
            }
        else:
            new_detail = detail

        super().__init__(status_code=status_code, detail=new_detail,
                         headers=headers)
