
from dotenv import find_dotenv,load_dotenv
import os
from requests import session
import logging


username = os.environ.get('KAGGLE_USERNAME')
password = os.environ.get('KAGGLE_PASSWORD')
payload = { 'action' : 'LOGIN',
          'username' : username,
          'password' : password}


def extract_data(url , file_path):
    '''
    Extract data and write to file
    '''
    
    curr_path = os.path.abspath(file_path)
    print(curr_path)
    with session() as c:
        c.post('https://www.kaggle.com/account/login', data=payload)
        with open(file_path , 'wb') as handlefile:
            response = c.get(url , stream = True)
            for block in response.iter_content(1024):
                handlefile.write(block)
                

def main(project_dir):
    
    # get Logger
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')
    
    # set data path
    raw_data_path = os.path.join(project_dir,'data','raw')
    train_data_path = os.path.join(raw_data_path,'train.csv')
    test_data_path = os.path.join(raw_data_path,'test.csv')

    # init urls
    train_url = 'https://www.kaggle.com/c/titanic/download/train.csv'
    test_url = 'https://www.kaggle.com/c/titanic/download/test.csv'

    # extract data
    extract_data(train_url , train_data_path)
    extract_data(test_url , test_data_path)
    
    logger.info('Data Fetch Completed')
    
if __name__ == '__main__':
    
    # root directory
    project_dir = os.path.join(os.path.dirname(__name__),os.pardir)
    
    #logging format
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO , format=log_fmt)
    
    #load .env
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    main(project_dir)
    
    
