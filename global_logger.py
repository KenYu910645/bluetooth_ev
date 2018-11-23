import logging 

##################
####  logger   ###
##################
# Set up logger
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger('BLUETOOTH')
logger.setLevel(logging.DEBUG)


# Print out logging message on console
h_console = logging.StreamHandler()
h_console.setFormatter(formatter)
h_console.setLevel(logging.INFO)
logger.addHandler(h_console)

# Record logging message at logging file
h_file = logging.FileHandler("BLUETOOTH.log")
h_file.setFormatter(formatter)
h_file.setLevel(logging.INFO)
logger.addHandler(h_file)

