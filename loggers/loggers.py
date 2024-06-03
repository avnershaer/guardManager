import logging
import os

def logger():
    # create a logger instance with a specific name
    logger = logging.getLogger('generalLogger')
    
    # if no handlers are present (avoid adding duplicate handlers)
    if not logger.handlers:

        # set logger level to info 
        logger.setLevel(logging.INFO)

        # define the path for the log file
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.log')

        # add a file handler to the logger
        fileHandler = logging.FileHandler(log_file_path)
        
        # sets the logging level for file handler to "INFO".
        fileHandler.setLevel(logging.INFO)
        
        # define the format for log messages displayed in the log file.
        fileFormatter = logging.Formatter(
            '%(asctime)s - %(name)s - model: %(module)s - func: %(funcName)s - line: %(lineno)d - %(levelname)s - %(message)s'
        )
        
        # add the file handler to logger
        fileHandler.setFormatter(fileFormatter)
        
        # add fileHandler
        logger.addHandler(fileHandler)
    
        # create a stream handler for logging to the console and set its level
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        
        # define the format of stream for logs on console
        streamFormatter = logging.Formatter(
            '%(asctime)s - %(name)s - model: %(module)s - func: %(funcName)s - line: %(lineno)d - %(levelname)s - %(message)s'
        )
        streamHandler.setFormatter(streamFormatter)
        
        # add streamHandler
        logger.addHandler(streamHandler)
    
    return logger

def err_logger():
    # create a logger instance with a specific name
    errorLogger = logging.getLogger('errorLogger')

    # if no handlers are present (avoid adding duplicate handlers)
    if not errorLogger.handlers:

        # set logger level to error 
        errorLogger.setLevel(logging.ERROR)

        # define the path for the log file
        error_log_file_path = os.path.join(os.path.dirname(__file__), 'errorLogs.log')
        
        # add a file handler to the logger
        errorHandler = logging.FileHandler(error_log_file_path)
        
        # define the format for error log messages displayed in the error log file.
        errorFormatter = logging.Formatter(
            '%(asctime)s - %(name)s - model: %(module)s - func: %(funcName)s - line: %(lineno)d - %(levelname)s - %(message)s'
        )
        
        # add the file handler to error logger
        errorHandler.setFormatter(errorFormatter)
        errorLogger.addHandler(errorHandler)
        
        # create a stream handler for logging to the console and set its level
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.ERROR)
        
        # define the format of stream for logs on console
        streamFormatter = logging.Formatter(
            '%(asctime)s - %(name)s - model: %(module)s - func: %(funcName)s - line: %(lineno)d - %(levelname)s - %(message)s'
        )
        streamHandler.setFormatter(streamFormatter)
        
        # add streamHandler
        errorLogger.addHandler(streamHandler)
    
    return errorLogger