from flask import jsonify
# 200 OK: 請求成功。
# 201 Created: 請求成功並建立了新的資源。
# 400 Bad Request: 客戶端發送的請求有誤（如參數錯誤、格式不正確等）。
# 401 Unauthorized: 用戶端未經授權，無法存取資源。
# 403 Forbidden: 客戶端被禁止存取資源。
# 404 Not Found: 請求的資源未找到。
# 500 Internal Server Error: 伺服器發生內部錯誤。

class ApiResponse:
    """
    用於構建標準化的API回應，包括成功回應和錯誤回應。
    """

    @staticmethod
    def success(data=None, message="Success", code=None, status_code=200):
        """
        構建成功回應。

        :param data: 返回的數據，可以是字典或列表。
        :param message: 描述性消息，默認為 "Success"。
        :param code: 自定義的應用級別錯誤代碼，默認為 None。
        :param status_code: HTTP 狀態碼，默認為 200。
        :return: 標準化的 JSON 回應和 HTTP 狀態碼。
        """
        response = {
            "code": code or status_code,
            "status": "success",
            "message": message,
            "data": data
        }
        return jsonify(response), status_code

    @staticmethod
    def error(code=None, message="An error occurred", status_code=400):
        """
        構建錯誤回應。

        :param message: 錯誤消息，默認為 "An error occurred"。
        :param code: 自定義的應用級別錯誤代碼，默認為 None。
        :param status_code: HTTP 狀態碼，默認為 400。
        :return: 標準化的 JSON 回應和 HTTP 狀態碼。
        """
        response = {
            "code": code or status_code,
            "status": "error",
            "message": message,
        }
        return jsonify(response), status_code

    @staticmethod
    def custom(status, message, data=None, code=None, status_code=200):
        """
        構建自定義回應。

        :param status: 回應的狀態，可以是 "success" 或 "error"。
        :param message: 描述性消息。
        :param data: 返回的數據，可以是字典或列表。
        :param code: 自定義的應用級別錯誤代碼或狀態代碼，默認為 None。
        :param status_code: HTTP 狀態碼，默認為 200。
        :return: 標準化的 JSON 回應和 HTTP 狀態碼。
        """
        response = {
            "code": code or status_code,
            "status": status,
            "message": message,
            "data": data,
        }
        return jsonify(response), status_code

    """
    用於構建標準化的API回應，包括成功回應和錯誤回應。
    """

    @staticmethod
    def Success(data=None, message="Success", code=None, status_code=200):
        """
        構建成功回應。

        :param data: 返回的數據，可以是字典或列表。
        :param message: 描述性的消息，默認為 "Success"。
        :param status_code: HTTP 狀態碼，默認為 200。
        :return: 標準化的 JSON 回應和 HTTP 狀態碼。
        """
        response = {
            "code": code or status_code,
            "status": "success",
            "message": message,
            "data": data
        }
        return jsonify(response), status_code

    @staticmethod
    def error(message="An error occurred", code=None, status_code=400):
        """
        構建錯誤回應。

        :param message: 錯誤消息，默認為 "An error occurred"。
        :param code: 錯誤代碼，用於標識特定的錯誤類型。
        :param errors: 詳細錯誤信息，可以是字典或列表。
        :param status_code: HTTP 狀態碼，默認為 400。
        :return: 標準化的 JSON 回應和 HTTP 狀態碼。
        """
        response = {
            "code": code or status_code,
            "status": "error",
            "message": message,
            }
        return jsonify(response), status_code

    @staticmethod
    def custom(status, message, data=None, code=None, status_code=200):
        """
        構建自定義回應。

        :param status: 回應的狀態，可以是 "success" 或 "error"。
        :param message: 描述性的消息。
        :param data: 返回的數據，可以是字典或列表。
        :param code: 錯誤代碼或狀態代碼。
        :param errors: 詳細錯誤信息，可以是字典或列表。
        :param status_code: HTTP 狀態碼，默認為 200。
        :return: 標準化的 JSON 回應和 HTTP 狀態碼。
        """
        response = {
            "code": code or status_code,
            "status": status,
            "message": message,
            "data": data,
            }
        return jsonify(response), status_code
