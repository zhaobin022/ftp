__author__ = 'zhaobin022'
import os

ACCOUNT_DB = {
    'type':'file',
    'filename':'accounts.json',
}

USER_BASE='%s\%s'% (os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'upload')
BASE_DIR = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))