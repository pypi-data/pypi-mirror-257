# @title Load and Handle Data

import pickle
import os
import logging

class PickleHandler:
    def __init__(self, folder_path, file_name, none_on_error:bool = True):
        """
        Initialize PickleHandler.

        Args:
            folder_path (str): The path to the folder where the data and log files are stored.
            file_name (str): The name of the data file.
            none_on_error (bool): If True, return None on errors. If False, raise exceptions.
        """
        self.folder_path = folder_path
        self.file_path = os.path.join(self.folder_path, file_name)
        self.file_log_path = os.path.join(self.folder_path, f'''log_{file_name.replace('.','_')}.log''')
        self._error_return_None = none_on_error

        # Ensure directory
        self._ensure_dir(self.folder_path)

        # Configure logging
        self.file_logger = logging.getLogger(f'PickleHandler_{file_name}')
        self._configure_logger()
        
    def _configure_logger(self):
        """
        Configure the logger for the PickleHandler.
        """
        self.file_logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.file_log_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.file_logger.addHandler(file_handler)

    def _ensure_dir(self, directory):
        """
        Ensure the directory exists, creating it if necessary.
        
        Args:
        directory (str): Path to the directory.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)


    def save(self, data):
        """
        Save data to the specified file.

        Args:
            data: The data to be saved.
        """
        with open(self.file_path, 'wb') as file:
            pickle.dump(data, file)
        print(f'Data saved to {self.file_path}')
        self.file_logger.info(f'Data saved to {self.file_path}')

    def load(self):
        """
        Load data from the specified file.

        Returns:
            The loaded data.
        """
        try:
            with open(self.file_path, 'rb') as file:
                data = pickle.load(file)
            print(f'Data loaded from {self.file_path}')
            self.file_logger.info(f'Data loaded from {self.file_path}')
            return data
            
        except FileNotFoundError:
            print(f'File not found at {self.file_path}. Returning None.')
            self.file_logger.error(f'File not found at {self.file_path}. Returned None')
            if self._error_return_None: return None
            raise FileNotFoundError
            
        except pickle.UnpicklingError:
            print(f'Error loading data [Unpickling] from {self.file_path}. Returning None.')
            self.file_logger.error(f'Error loading data [Unpickling] from {self.file_path}. Returning None.')
            if self._error_return_None: return None
            raise

    def load_logs(self):
        """
        Load log entries from the log file.

        Returns:
            A list of log entries.
        """
        if not os.path.exists(self.file_log_path):
            print(f'Log file not found at {self.file_log_path}.')
            return []
    
        with open(self.file_log_path, 'r') as file:
            logs = file.readlines()
            
        return logs
            
    def print_logs(self):
        """
        Print log entries to the console.
        """
        logs = self.load_logs()
        for log in logs:
            print(log.strip())
