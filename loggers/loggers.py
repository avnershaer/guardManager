import logging
import logging.config
import os


def logger():
    
    # create a logger instance 
    logger = logging.getLogger(__name__)
    
    # if no handlers are present (avoid adding duplicate handlers)
    if not logger.handlers: 

        logger.setLevel(logging.INFO)

        # define the path for the log file
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.log')

        # add a file handler to the logger
        fileHandler = logging.FileHandler(log_file_path)
        
        # sets the logging level for file handler to "INFO".
        fileHandler.setLevel(logging.INFO)
        
        # format for log messages
        fileFormatter = logging.Formatter(
            '%(levelname)s - %(message)s'
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
            '%(levelname)s - %(message)s'
            )
        streamHandler.setFormatter(streamFormatter)
        
        # add streamHandler
        logger.addHandler(streamHandler)
    
    return logger

def err_logger():

    # create a logger instance
    error_logger = logging.getLogger()

    # if no handlers are present (avoid adding duplicate handlers)
    if not error_logger.handlers:

        # set logger level to error 
        error_logger.setLevel(logging.ERROR)

        # define the path for the log file
        error_log_file_path = os.path.join(os.path.dirname(__file__), 'errorLogs.log')
        
        # add a file handler to the logger
        errorHandler = logging.FileHandler(error_log_file_path)
        
        # define the format for error log messages displayed in the error log file.
        errorFormater = logging.Formatter(
            '%(levelname)s - %(message)s'
            )
        
        # add the file handler to error logger
        errorHandler.setFormatter(errorFormater)
        error_logger.addHandler(errorHandler)
        
        # create a stream handler for logging to the console and set its level
        streamHandler = logging.StreamHandler()
        errorHandler.setLevel(logging.ERROR)
        
        # set level for stream handler
        streamHandler.setLevel(logging.ERROR)
        
        # define the format of stream for logs on console
        streamFormatter = logging.Formatter(
            '%(levelname)s - %(message)s'
            )
        streamHandler.setFormatter(streamFormatter)
        
        # add streamHandler
        error_logger.addHandler(streamHandler)
    
    return error_logger

