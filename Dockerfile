# Utiliser l'image Azure Functions avec support pour SSH et débogage
FROM mcr.microsoft.com/azure-functions/python:4-python3.10-appservice

# Configurer les variables d'environnement pour Azure Functions
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Installer les dépendances système
RUN apt-get update && apt-get install -y git dnsutils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt et installer les dépendances Python
COPY AzureFunc/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Installer TheHarvester et Sherlock
RUN git clone https://github.com/laramies/theHarvester.git /opt/theHarvester \
    && pip install --no-cache-dir -r /opt/theHarvester/requirements.txt \
    && pip install --no-cache-dir sherlock-project

# Copier le code de la fonction dans le répertoire de travail Azure Functions
COPY AzureFunc/ /home/site/wwwroot/

# Définir le répertoire de travail pour la fonction
WORKDIR /home/site/wwwroot

# Commande par défaut pour exécuter la fonction Azure
ENTRYPOINT ["/azure-functions-host/Microsoft.Azure.WebJobs.Script.WebHost", "--host"]
