import json
from pathlib import Path
import os

from flask import Response

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ERROR_MESSAGE = {'Error': 'Bad Request'}
SUCCESS_MESSAGE = {'message': 'success'}


# class ToolsHandler:
#     ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#     ERROR_MESSAGE = {'Error': 'Bad Request'}
#     SUCCESS_MESSAGE = {'message': 'success'}


#     def __init__(self):
#         self.success_message = __class__.SUCCESS_MESSAGE
#         self.error_message = __class__.ERROR_MESSAGE
#         self.allowed_extensions = __class__.SUCCESS_MESSAGE

#     def deal_with_message(self, rate: int):
#         if rate > 0:
#             return f'Giving SUCCESS MESSAGE - {self.SUCCESS_MESSAGE}'
#         return f'Giving ERROR MESSAGE - {self.ERROR_MESSAGE}'
    
#     def check_if_extension_allowed(self, filename):
#         return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

def make_directory():
    path = Path(__file__).resolve().parent.parent
    folder = os.path.join(path, 'upload_directory')
    exists = os.path.exists(folder)
    if not exists:
        os.makedirs(folder)
    return folder


def auth_user(request):
    my_username = 'testUsername'
    my_password = 'testPassword'
    passed_username = request.args.get('client_id')
    passed_password = request.args.get('client_secret')
    return my_username == passed_username and my_password == passed_password


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Handler:
    def __init__(self, response, status, mimetype):
        self.response = response
        self.status = status
        self.mimetype = mimetype
    
    def send_error_message(self):
        return Response(response=self.response, status=self.status, mimetype=self.mimetype)

# th = ToolsHandler()
# print(th.deal_with_message(0))