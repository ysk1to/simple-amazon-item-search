import os
import urllib
import re
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from bottlenose import Amazon
from bs4 import BeautifulSoup
from retry import retry

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_ASSOCIATE_TAG = os.environ.get('AWS_ASSOCIATE_TAG')


@retry(urllib.error.HTTPError, tries=10, delay=5)
def search(amazon, k, i):
    print('get products...')
    return amazon.ItemSearch(Keywords=k, SearchIndex=i)
    

def main():
    amazon = Amazon(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG, Region='JP',
                    Parser=lambda text: BeautifulSoup(text, 'xml')
                    )
    
    keyword = input('keyword? >> ')
    
    df_category = pd.read_csv('categorys.csv')
    indexs = range(df_category.shape[0])
        
    while True:
        # show category
        for i, v in df_category.iterrows():
            print(str(i) + '. ' + v['DispName'])
        print('')
        
        num = input('category number? [None : All] >> ')
        if not num:
            category = 'All'
            break
        elif re.match('[\d]', num):
            num = int(num)
            if num in indexs:
                category = df_category.loc[num, 'SearchIndex']
                break

    response = search(amazon, keyword, category)
    
    for item in response.find_all('Item'):
        print(item.Title.string)


if __name__ == '__main__':
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    
    main()
