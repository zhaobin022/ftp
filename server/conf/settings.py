__author__ = 'zhaobin022'
import os

ACCOUNT_DB = {
    'type':'file',
    'filename':'accounts.json',
}

USER_BASE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'upload')
BASE_DIR = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))

BIND_HOST='0.0.0.0'
BIND_PORT=8010