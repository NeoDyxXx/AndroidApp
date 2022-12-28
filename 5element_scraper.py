import requests as r
from bs4 import BeautifulSoup
import json


header = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx GX)'
}


def get_link_to_category(url):
    response = r.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    return list(map(lambda item: {
            'name': item.find('a').text, 
            'url': 'https://5element.by' + item.find('a')['href']
        },
        soup.find('div', class_='carousel-slider').find_all('div', class_='swiper-slide')[1:]))


def get_link_to_subcategory(url, name):
    response = r.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')

    return list(map(lambda item: {
            'category': name, 
            'sub_category': item.find('a').text, 
            'url': 'https://5element.by' + item.find('a')['href']
        }, 
        soup.find('div', class_='filters-body').find_all('li')))


def get_all_items(param):
    list_item = []


    for i in range(1, 5):
        try:
            response = r.get(param['url'] + 'page=' + str(i), headers=header)

            if response.status_code == 200:
                try:
                    soup = BeautifulSoup(response.text, 'lxml')
                    list_item.extend(list(map(lambda item: {
                        'category': param['category'], 
                        'sub_category': param['sub_category'],
                        'name': item.find('a', class_='c-text').text,
                        'details': item.find('div', class_='c-details').text.replace('                                    ', ' ')\
                            .replace('\xa0', ''),
                        'price': item.find('div', class_='c-price').text,
                        'discount': "".join(item.find('div', class_='c-discount').text.split()).replace('-', ' -'),
                        'url': 'https://5element.by' + item.find('a', class_='c-image')['href']
                    }, soup.find_all('div', class_='card-product-full'))))
                    print('item' + str(i))
                except:
                    pass
            else:
                print('Not Found.')
                break
        except:
            pass

    return list_item


def main():
    list_of_category = get_link_to_category('https://5element.by')
    list_of_items = []

    for category in list_of_category:
        list_of_subcategory = get_link_to_subcategory(category['url'], category['name'])

        for subcategory in list_of_subcategory:
            list_of_items.extend(get_all_items(subcategory))


    with open("list_of_item.json", "w") as fp:
        json.dump(list_of_items , fp) 

if __name__ == '__main__':
    main()