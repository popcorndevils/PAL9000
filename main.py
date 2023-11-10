from configparser import ConfigParser
from pal9000 import Pal9000

config = ConfigParser()
config.read("pal.ini")

client = Pal9000(config)
client.run()
