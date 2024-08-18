import logging
import os
import sys
from termcolor import colored


class LoggingProxy:
    def __init__(self, target_object, logger_name):
        # Get the directory where the script is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the full path to the error.log file in the same directory
        self.error_log_path = os.path.join(self.script_dir, "error.log")
        self.info_log_path = os.path.join(self.script_dir, "info.log")

        self._target = target_object
        self.logger_err = logging.getLogger(f"{logger_name}_error")
        self.logger_info = logging.getLogger(f"{logger_name}_debug")
        self.logger_stdout = logging.getLogger(f"{logger_name}_stdout")
        self._setup_logger()

    def _setup_logger(self):
        if os.path.exists(self.error_log_path):
            os.remove(self.error_log_path)
        if os.path.exists(self.info_log_path):
            os.remove(self.info_log_path)

        # Handlers for logging to stdout and a file
        stdoutHandler = logging.StreamHandler()
        try:
            errHandler = logging.FileHandler(self.error_log_path)
            infoHandler = logging.FileHandler(self.info_log_path)
        except Exception as e:
            raise e
        # errHandler = logging.FileHandler("error.log")

        # Set log levels
        self.logger_stdout.setLevel(logging.INFO)
        self.logger_err.setLevel(logging.ERROR)
        self.logger_info.setLevel(logging.INFO)

        # Format for the logs
        error_fmt = logging.Formatter(
            "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
        )
        std_fmt = logging.Formatter(
            "%(name)s: %(asctime)s >>> %(message)s"
        )
        info_fmt = logging.Formatter(
            "%(name)s: %(asctime)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
        )

        # Set the format on the handlers
        stdoutHandler.setFormatter(std_fmt)
        errHandler.setFormatter(error_fmt)
        infoHandler.setFormatter(info_fmt)

        # Add the handlers to the logger
        self.logger_stdout.addHandler(stdoutHandler)
        self.logger_err.addHandler(errHandler)
        self.logger_info.addHandler(infoHandler)

        # Prevent propagation to parent loggers
        self.logger_err.propagate = False
        self.logger_info.propagate = False
        self.logger_stdout.propagate = False

    def __getattr__(self, name):
        # Dynamically retrieve attributes from the target object
        attr = getattr(self._target, name)

        if callable(attr):
            def wrapper(*args, **kwargs):
                # Log the method call at the DEBUG level
                self.logger_info.info(f"Calling method {name} with args: {args}, kwargs: {kwargs}")

                try:
                    result = attr(*args, **kwargs)
                    return result
                except Exception as e:
                    # Log the exception with traceback at the ERROR level
                    self.logger_err.error(f"Exception in method {name}: {e}", exc_info=True)

                    # Log instructions for reporting the issue
                    github_link = colored("https://github.com/hetari/pyutube/issues", color='blue', attrs=['underline'])
                    message = (
                        colored(
                            "An error occurred. Please report this issue to the support team by creating an issue on GitHub at ",
                            color='red', attrs=[]
                        ) +
                        github_link +  # Insert the colored GitHub link
                        colored(
                            ". Include the ",  # Add a space after 'Include the'
                            color='red'
                        ) +
                        colored(
                            "'error.log' ",  # Add a space after 'error.log'
                            color='green', attrs=['bold']
                        ) +
                        colored(
                            "file located at ",  # Add a space after 'file located at'
                            color='red'
                        ) +
                        colored(
                            f"{self.error_log_path}.",  # Comma added here
                            color='green', attrs=['bold']
                        )
                    )

                    self.logger_stdout.info(message)
                    sys.exit(1)

            return wrapper
        else:
            return attr
