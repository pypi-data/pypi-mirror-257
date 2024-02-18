import logging
import logging.config

from configparser import ConfigParser

from util.FileUtil import FileUtil

class LoggerUtil:
    """
    LoggerUtil is a utility class that provides static methods to create and retrieve logger instances.
    """

    @staticmethod
    def getLogger(logging_config_file_path):
        """
        Creates and returns a logger instance based on the logging configuration file provided.

        The logging configuration file should define handlers, formatters, and loggers to set up
        the logging infrastructure.

        Parameters:
        logging_config_file_path (str): The path to the logging configuration file.

        Returns:
        logging.Logger: A configured Logger instance.
        """
        logging.config.fileConfig(logging_config_file_path)
        logger = logging.getLogger(__name__)
        return logger

    @staticmethod
    def getLogger_defaults():
        """
        Creates and returns a logger instance with default configuration.

        The default logging configuration is expected to be in a file named 'logging.conf' located
        in the '/config' directory at the project's root path.

        Returns:
        logging.Logger: A Logger instance configured with default settings.
        """
        default_logging_config_file_path = FileUtil.getProjectRootPath() + '/config/logging.conf'
        return LoggerUtil.getLogger(default_logging_config_file_path)

class PropertiesUtil:
    """
    The PropertiesUtil class offers utility methods for reading properties from
    a properties configuration file. It provides functionality to read configurations
    both from a specified path and from a default configuration file.

    Static methods:
        - read_properties_file: Reads properties from a specified configuration file.
        - read_properties_file_defaults: Reads properties from the default configuration file.
    """
    @staticmethod
    def read_properties_file(config_path):
        """
        Reads a properties file from the given path and returns a dictionary of
        configuration properties.

        The method reads the default section of the configuration file and returns
        the properties as key-value pairs. Sections within the file are ignored.
        The method assumes the configuration file format is similar to the INI format,
        where properties are not explicitly assigned to any section.

        :param config_path: The path to the configuration file.
        :type config_path: str
        :return: A dictionary containing the configuration properties.
        :rtype: dict
        """
        # Create a ConfigParser object
        config = ConfigParser()

        # Read the properties file
        config.read(config_path)

        # Fetch all the properties
        properties = {}
        if config.defaults():
            for key in config.defaults():
                properties[key] = config.defaults()[key]

        return properties

    @staticmethod
    def read_properties_file_defaults():
        """
        Reads the default properties file from the predefined path and returns a
        dictionary of configuration properties.

        This method utilizes read_properties_file internally, pointing it to the
        default configuration file located in the 'config' directory of the project's
        root. It assumes the configuration file is named 'config.properties'.

        :return: A dictionary containing the configuration properties from the default file.
        :rtype: dict
        """
        # Define the path to the default configuration file
        default_config_path = FileUtil.getProjectRootPath() + '/config/config.properties'

        # Read properties from the default configuration file
        return PropertiesUtil.read_properties_file(default_config_path)
