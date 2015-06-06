from iniconf import MyIni
from my_logger import debug_logging, online_logging
from clean_worker import CleanWorker
from app import app
from models import User, Users, Package
import views

__version__ = '3.6.0'
