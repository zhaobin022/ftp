__author__ = 'zhaobin022'
import os
import sys
import json
from conf import settings
def fetch_account(username,password):
    mod = sys.modules[__name__]
    if hasattr(mod,  '%s_auth' % settings.ACCOUNT_DB.get('type')):
        func = getattr(mod, '%s_auth' % settings.ACCOUNT_DB.get('type'))
        return func(username,password)



def authenticate(username,password):
    return  fetch_account(username,password)



def file_auth(username,password):
    file_name = settings.ACCOUNT_DB.get('filename')
    file_path = os.path.join(settings.BASE_DIR,'conf%s%s' % (os.path.sep,file_name))
    with open(file_path,'r') as f:
        account_dic = json.load(f)
    if account_dic.get(username):
        if account_dic[username]['password'] == password:
            return True,'login successfull',account_dic[username]['quotation']
        else:
            return False,'Please input the rightpassword !'
    else:
        return False,'Please input th right username '

if __name__ == '__main__':
    print authenticate('lisi','123')