import azure.functions as func
from cfgparser import CustomConfigParser
from modules.OSINTProcess import Sherlock
import logging
import json  # Importer le module json pour le traitement JSON

# Créer l'application pour la fonction Azure
app = func.FunctionApp()
# Mapping du fichier de configuration pour chaque service
cfg = CustomConfigParser()
# Configurer le niveau de logging
logging.basicConfig(level=logging.INFO)

@app.route(route="sherlock", auth_level=func.AuthLevel.ANONYMOUS)
def SherlockFunction(req: func.HttpRequest) -> func.HttpResponse:
    # Logique de traitement pour SherlockFunction
    user = str(req.params.get('user'))
    
    # Vérifiez si l'utilisateur est fourni
    if not user:
        return func.HttpResponse("Veuillez fournir un utilisateur.", status_code=400)

    # Initialiser le processus Sherlock
    sherlock_process = Sherlock(user)
    
    # Exécuter le processus et récupérer les résultats
    cmd_result = sherlock_process.execute()

    # Vérifier si cmd_result est valide
    if cmd_result is not None:
        # Renvoyer les résultats sous forme de JSON
        return func.HttpResponse(
            json.dumps(cmd_result),
            status_code=200,
            mimetype="application/json"  # Définir le type MIME comme application/json
        )
    else:
        return func.HttpResponse("Une erreur s'est produite lors de l'exécution de la commande.", status_code=500)


"""
@app.route(route="harvester", auth_level=func.AuthLevel.ANONYMOUS)
def HarvesterFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    domain = req.params.get('domain')
    limit = req.params.get('limit')
    if not domain:
        return func.HttpResponse(f"You should have a domain argument to do a request.")
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    if domain:
        try:
            cmd = "python3 /opt/theHarvester/theHarvester.py -d " + str(domain) 
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="Sherlock", auth_level=func.AuthLevel.ANONYMOUS)
def Sherlock(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

"""