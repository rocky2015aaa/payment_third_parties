# from dotenv import load_dotenv
from .constants import AUTHORIZE_NET_API_LOGIN_ID, \
                      AUTHORIZE_NET_TRANSACTION_KEY
import os

# Get env Variables from the docker file for prod or dev.
# dotenv_path = Path(os.environ["ENV_FILE_PATH"])
# load_dotenv(dotenv_path=dotenv_path)

# authorize.net sandbox account
# API_LOGIN_ID = os.getenv(AUTHORIZE_NET_API_LOGIN_ID, '3KCs26vrNdU')
# TRANSACTION_KEY = os.getenv(AUTHORIZE_NET_TRANSACTION_KEY,
#                             '29ZbGxA788a2679V')
API_LOGIN_ID = os.getenv(AUTHORIZE_NET_API_LOGIN_ID, '5KP3u95bQpv')
TRANSACTION_KEY = os.getenv(AUTHORIZE_NET_TRANSACTION_KEY, '346HZ32z3fP4hTG2')

MONGO_DB_LINK = os.getenv('MONGO_DB_LINK', 'mongodb+srv://root:X88xpI12d0bsViVA@plc1.zps94.mongodb.net/plc1?retryWrites=true&w=majority')  # noqa
