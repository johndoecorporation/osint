import configparser
import os
from pathlib import Path

class CustomConfigParser:
    def __init__(self, config_file="config/config.ini"):
        """Initialise le CustomConfigParser avec le fichier de configuration spécifié."""
        self.config = configparser.ConfigParser()
        self.config_file = Path.cwd() / config_file
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Le fichier de configuration '{config_file}' n'existe pas.")
        
        self.config.read(config_file)

    def get(self, section, option, fallback=None):
        """Récupère la valeur d'une option dans une section donnée.
        
        :param section: Section dans le fichier de configuration.
        :param option: Option dont on veut récupérer la valeur.
        :param fallback: Valeur par défaut à retourner si l'option n'existe pas.
        :return: Valeur de l'option ou valeur par défaut.
        """
        if self.config.has_section(section):
            if self.config.has_option(section, option):
                return self.config.get(section, option, fallback=fallback)
            else:
                raise ValueError(f"L'option '{option}' n'existe pas dans la section '{section}'.")
        else:
            raise ValueError(f"La section '{section}' n'existe pas dans le fichier de configuration.")

    def get_all_sections(self):
        """Retourne toutes les sections du fichier de configuration."""
        return self.config.sections()

    def get_all_options(self, section):
        """Retourne toutes les options d'une section donnée.
        
        :param section: Section dont on veut récupérer les options.
        :return: Liste des options dans la section.
        """
        if self.config.has_section(section):
            return self.config.options(section)
        else:
            raise ValueError(f"La section '{section}' n'existe pas dans le fichier de configuration.")

    def set(self, section, option, value):
        """Définit une valeur pour une option dans une section donnée.
        
        :param section: Section dans le fichier de configuration.
        :param option: Option dont on veut définir la valeur.
        :param value: Valeur à définir.
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        
    def save(self):
        """Sauvegarde les modifications dans le fichier de configuration."""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
