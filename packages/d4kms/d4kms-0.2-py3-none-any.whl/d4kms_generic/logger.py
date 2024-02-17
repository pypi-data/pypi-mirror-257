import logging
import traceback

class Logger():

  FORMAT = '{levelname:<9s} {message}'
  
  def __init__(self, level=logging.DEBUG):
    logging.basicConfig(format=self.FORMAT, style='{')
    self.logger = logging.getLogger("application") 
    self.logger.setLevel(level)

  def debug(self, message):
    self.logger.debug(message)

  def info(self, message):
    self.logger.info(message)

  def warning(self, message):
    self.logger.warning(message)

  def error(self, message):
    self.logger.error(message)

  def exception(self, message, e, exception=None):
    self.logger.error(f"{message}\n\nDetails: '{e}'\n\nTrace:\n\n{traceback.format_exc()}")
    if exception:
      raise exception(message)
  
application_logger = Logger()