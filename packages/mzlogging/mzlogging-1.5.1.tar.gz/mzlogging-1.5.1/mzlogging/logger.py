import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from ._consts import *
from ._mysql_connector import MySQLConnector


# TODO: check if table exists and create it if not
# TODO: get table name from schema file or from the class (input parameter)
class MZLogging:

    def __init__(self, logger_name: str, log_level=logging.DEBUG, log_file: str = None,
                 db_type: str = SUPPORTED_DATABASES[0], db_credentials: dict = None, daily_log_file: bool = False):
        """
        Create an instance of MZLogging.

        Parameters:
            logger_name (str): The logger name.
            log_level (int): The logger level, default is logging.DEBUG.
            log_file (str, optional): Path to the log file.
            db_type (str, optional): Database type, see on _consts.py for supported databases.
            db_credentials (dict, optional): Database credentials, dict must contain host, user, password, and database.
            daily_log_file (bool, optional): If True, a new log file will be created every day.
        """
        self.logger = logging.getLogger(logger_name)
        self.log_level = log_level
        self.logger.setLevel(log_level)

        if db_type not in SUPPORTED_DATABASES:
            raise ValueError(f"Invalid db_type: {db_type}, supported databases: {SUPPORTED_DATABASES}")

        self.db_type = db_type
        self.db_credentials = db_credentials

        self.formatter = logging.Formatter('[%(asctime)s - %(name)s] %(levelname)s - %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')

        if log_file:
            self.log_file = log_file
            self._setup_file_logger(log_file)
            if daily_log_file:
                self._setup_daily_logger(f'{os.path.splitext(log_file)[0]}-{datetime.now().strftime("%y%m%d")}.log')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_logger(self, log_file):
        # Crea un handler per il log base
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def _setup_daily_logger(self, daily_log_file):
        # Crea un handler per il log giornaliero
        daily_log_handler = TimedRotatingFileHandler(
            filename=daily_log_file, when="midnight", interval=1, backupCount=30
        )
        daily_log_handler.setFormatter(self.formatter)
        self.logger.addHandler(daily_log_handler)

    def _check_db_credentials(self):
        """
        Check if db_credentials are valid.

        Raises:
            ValueError: If db_credentials are missing required keys.
        """
        if not self.db_credentials:
            raise ValueError("Missing DB credentials")
        for key in REQUIRED_DB_KEYS:
            if key not in self.db_credentials:
                raise ValueError(f"Missing required DB credential key: {key}")

    def set_db_credentials(self, db_credentials: dict):
        """
        Set database credentials.

        Parameters:
            db_credentials (dict, optional): Database credentials, dict must contain host, user, password, database and port.

        Raises:
            ValueError: If db_credentials are missing required keys.
        """
        self.db_credentials = db_credentials
        self._check_db_credentials()

    def log(self, log_level: int, log_message: str, exc_info: bool = False, stop_on_error: bool = False):
        """
        Log a message.

        Parameters:
            log_level (int): Log level, can be debug (0), info (1), warning (2), error (3), exception (4) or critical (5).
            log_message (str): Message to log.
            exc_info (bool, optional): If True, exception info will be logged.
            stop_on_error (bool, optional): If True, an exception will be raised if log_level is error or exception or critical.

        Raises:
            ValueError: If log_level is invalid.

            Exception: If stop_on_error is True and log_level is error or exception or critical.
        """
        if log_level not in LOG_LEVELS:
            raise ValueError(f"Invalid log_level: {log_level}, supported log levels: {LOG_LEVELS}")

        if log_level == 0:
            self.logger.debug(log_message)
        elif log_level == 1:
            self.logger.info(log_message)
        elif log_level == 2:
            self.logger.warning(log_message)
        elif log_level == 3:
            self.logger.error(log_message, exc_info=exc_info)
            if stop_on_error:
                raise Exception(log_message)
        elif log_level == 4:
            self.logger.exception(log_message, exc_info=exc_info)
            if stop_on_error:
                raise Exception(log_message)
        else:  # log_level == 'critical' or log_level == 5
            self.logger.critical(log_message, exc_info=exc_info)
            if stop_on_error:
                raise Exception(log_message)

    def log_db(self, log_level: int, log_message: str, severity_level: int,
               script_name: str = None, function_name: str = None, line_number: int = None,
               error_code: int = None, user_id: int = None, user_name: str = None,
               log_details: str = None, ip_address: str = None, session_id: str = None,
               environment: str = None, source: str = None, custom_data: dict = None,
               other_database_cols: dict = None, exc_info: bool = False, stop_on_error: bool = False):
        """
        Log a message.

        Parameters:
            log_level (int): Log level, can be debug (0), info (1), warning (2), error (3), exception (4) or critical (5).
            log_message (str): Message to log.
            severity_level (int, optional): Severity level. See _consts.py for supported severity levels.
            script_name (str, optional): Script name.
            function_name (str, optional): Function name.
            line_number (int, optional): Line number.
            error_code (int, optional): Error code.
            user_id (int, optional): User id.
            user_name (str, optional): User name.
            log_details (str, optional): Log details.
            ip_address (str, optional): IP address.
            session_id (str, optional): Session id.
            environment (str, optional): Environment.
            source (str, optional): Source.
            custom_data (dict, optional): Custom data to save on database.
            other_database_cols (dict, optional): Other columns to save on database, only if schema is different from the default.
            exc_info (bool, optional): If True, exception info will be logged.
            stop_on_error (bool, optional): If True, an exception will be raised if log_level is error or exception or critical.

        Raises:
            ValueError: If log_level is invalid.
                        If db_data is not empty and table_name or columns (inside db_data) are missing.
                        If columns (inside db_data) is not a dict.

            Exception: If stop_on_error is True and log_level is error or exception or critical.

            mysql.connector.errors.Error: If there is an error connecting to the database.
        """
        if not log_level or not log_message or not severity_level:
            raise ValueError("Missing required parameters")

        self.log(log_level, log_message, exc_info, stop_on_error)

        self._check_db_credentials()

        data = other_database_cols if other_database_cols else {}

        data["log_level"] = LOG_LEVELS[log_level]
        data["log_message"] = log_message
        data["severity_level"] = SEVERITY_LEVELS[severity_level]
        data["script_name"] = script_name
        data["function_name"] = function_name
        data["line_number"] = line_number
        data["error_code"] = error_code
        data["user_id"] = user_id
        data["user_name"] = user_name
        data["log_details"] = log_details
        data["ip_address"] = ip_address
        data["session_id"] = session_id
        data["environment"] = environment
        data["source"] = source
        data["custom_data"] = custom_data

        db_conn = MySQLConnector(self.db_credentials)
        # TODO: get right table name
        db_conn.insert('mz_logs', data)
        db_conn.close()
