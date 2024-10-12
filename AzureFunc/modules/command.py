import subprocess
import logging

class Command:
    def __init__(self, command):
        """Initialise la classe Cmd avec la commande à exécuter."""
        self.command = command

    def execute(self):
        """Exécute la commande et attend qu'elle se termine."""
        try:
            logging.info(f"Exécution de la commande : {self.command}")
            result = subprocess.run(self.command, shell=True, check=True, text=True, capture_output=True)

            logging.info("La commande a été exécutée avec succès.")
            logging.info("Sortie : %s", result.stdout.strip())
            return result.stdout.strip()  # Retourne la sortie standard de la commande

        except subprocess.CalledProcessError as e:
            logging.error("Une erreur est survenue lors de l'exécution de la commande : %s", e)
            logging.error("Sortie d'erreur : %s", e.stderr.strip())
            raise  # Lever l'exception pour la gestion d'erreur au niveau supérieur
        except Exception as e:
            logging.error("Une erreur inattendue est survenue : %s", e)
            raise  # Lever l'exception pour la gestion d'erreur au niveau supérieur
