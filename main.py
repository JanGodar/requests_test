import requests
from bs4 import BeautifulSoup
import csv


with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Комнатность', 'Площадь', 'Жилой комплекс', 'Район', 'Этаж', 'Срок сдачи', 'Номер дома', 'Стоимость квартиры', 'Стоимость одного метра'])



def get_soup(url):
    response = requests.get(url=url)
    if response.status_code != 200:
        return False
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


def get_text(index=None, list=None, tag=None):
    if list:
        tag = list[index]
    return tag.text.strip()

soup = get_soup('https://www.domostroynn.ru/kvartiry?page=1')
val = int(''.join(soup.find('a', 'filter-menu__item filter-menu__item--active').text[:-9].split()))
end_val = val // 40 + 1
print(end_val)

for page in range(1, end_val+1):
    url = f"https://www.domostroynn.ru/kvartiry?page={page}"

    if soup:= get_soup(url):
        list_of_apart = soup.select('div#w2 > a')

        for apart in list_of_apart:

            block_middle_top = apart.find('div', 'search-grid__cell search-grid__cell--rooms')
            list_block_middle_top = block_middle_top.find_all('div')

            rooms_num, square = get_text(0, list_block_middle_top).split(', ')
            square = square.replace('.', ',').split()[0]
            residential_complex = get_text(1, list_block_middle_top)
            district = list_block_middle_top[2].text

            floor = get_text(tag=apart.find('div', 'search-grid__cell search-grid__cell--area-kitchen'))[3:]
            
            list_build_date = apart.find('div', 'search-grid__cell search-grid__cell--time').get_text('|').split('|')
            if len(list_build_date) == 2:
                date, house_num = list_build_date
            else:
                date = list_build_date[0]
                house_num = None

            price = ''.join(get_text(tag=apart.find('div', 'search-grid__price'))[:-2].split())
            price_per_m = ''.join(get_text(tag=apart.find('div', 'search-grid__price-per-m'))[:-8].split())

            with open('res.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
    
                flatten = rooms_num, square, residential_complex, district, floor, date, house_num, price, price_per_m
                writer.writerow(flatten)
    
    else:
        break
