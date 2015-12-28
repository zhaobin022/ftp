__author__ = 'zhaobin022'

import json

account = {
    'lisi': {
                'password':'123',
                'quotation': 50,
                },
    'zhangsan': {
            'password':'456',
            'quotation': 10,
            },
}

with open('accounts.json','wb') as f:
    json.dump(account,f)