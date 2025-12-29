from typing import Any, Optional


class ApiResponse:
    def __init__(self, success: bool, data: Any = None, error: Optional[str] = None, error_code: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error
        self.error_code = error_code

    def to_dict(self) -> dict[str, Any]:
        response: dict[str, Any] = {
            "success": self.success,
        }
        if self.data is not None:
            response["data"] = self.data

        if self.error:
            response["error"] = self.error

        if self.error_code:
            response["error_code"] = self.error_code

        return response

    def to_json(self) -> str:
        import json

        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )
