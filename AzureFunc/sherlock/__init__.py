import azure.functions as func
from function_app import SherlockFunction

def main(req: func.HttpRequest) -> func.HttpResponse:
    return SherlockFunction(req)