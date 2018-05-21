import sys
import os
       
if not os.path.exists('./logs'):
    os.makedirs('./logs')
   
from status import run_status


def main(method):
    methods = ['status']
    method = method.strip('--')

    if method not in methods:
        print('ERROR: Invalid method. Please include a valid method.')
        sys.exit(1)
    elif method == 'status':  
        run_status()
    

if __name__ == '__main__':
        
    method = sys.argv[1]
    main(method)
