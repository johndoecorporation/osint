import json
import logging
import tempfile
import os
import re
from modules.command import Command  # Assurez-vous d'importer la classe Command depuis le bon module
from cfgparser import CustomConfigParser
from abc import ABC, abstractmethod

# Configurer le logging au niveau du module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OSINTProcess(ABC):
    def __init__(self):
        """Initialise le processus OSINT avec les paramètres nécessaires."""
        self.config = CustomConfigParser()

    @abstractmethod
    def execute(self):
        """Méthode abstraite pour exécuter le processus OSINT."""
        pass

    @abstractmethod
    def get_command(self):
        """Méthode abstraite pour obtenir la commande à exécuter."""
        pass

class Sherlock(OSINTProcess):
    def __init__(self, user):
        """Initialise le processus Sherlock avec l'utilisateur spécifié."""
        super().__init__()  # Appelle le constructeur de la classe parente
        self.user = user
        logger.info(f"Initialisation de Sherlock pour l'utilisateur: {user}")

    def get_command(self):
        """Retourne la commande à exécuter pour Sherlock."""
        cmd_template = self.config.get('sherlock', 'cmd')
        logger.debug(f"Commande obtenue du template: {cmd_template}")
        return cmd_template.format(user=self.user)

    def create_temp_folder(self):
        """Crée un dossier temporaire et retourne son chemin."""
        temp_dir = tempfile.TemporaryDirectory()
        logger.info(f"Dossier temporaire créé: {temp_dir.name}")
        return temp_dir

    def parse_results(self, output_file_path):
        """Parse les résultats du fichier de sortie et retourne un dictionnaire JSON."""
        results = []

        with open(output_file_path, 'r') as f:
            for line in f:
                # Utilisation d'une expression régulière pour extraire le nom du site et l'URL
                match = re.search(r'\[\+\] (.+?): (.+)', line.strip())
                if match:
                    site_name = match.group(1)
                    site_url = match.group(2)
                    results.append({"site": site_name, "url": site_url})

        logger.info(f"Résultats analysés: {results}")
        return results

    def execute(self):
        """Exécute la commande pour Sherlock et retourne les résultats en JSON."""
        with self.create_temp_folder() as temp_dir:
            command_str = self.get_command()
            # Créer le chemin du fichier texte dans le dossier temporaire
            output_file_path = os.path.join(temp_dir, f"{self.user}.txt")
            # Modifier la commande pour rediriger la sortie vers le fichier texte
            command_str += f" > {output_file_path}"

            logger.info(f"Exécution de la commande: {command_str}")

            try:
                command = Command(command_str)  # Crée une instance de Command avec la commande
                command.execute()  # Exécute la commande
                logger.info(f"Commande exécutée avec succès, résultats enregistrés dans: {output_file_path}")

                # Analyser les résultats et les retourner en JSON
                return self.parse_results(output_file_path)
            except Exception as e:
                logger.error(f"Erreur lors de l'exécution de la commande: {str(e)}")
                return None  # Vous pouvez aussi lever l'exception si vous préférez
