from bs4 import BeautifulSoup
import requests
import json
import csv
#url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {

    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
} #Притворяемся человеком
#req = requests.get(url, headers=headers) #Получаем данные по ссылке

#src = req.text
#print(src)

#with open("new_index.html", "w", encoding='utf-8') as file: #'w' - запускаем на запись
#    file.write(src)

#with open("new_index.html", encoding='utf-8') as file: #Открываем файл для чтения
#    src = file.read()

#soup = BeautifulSoup(src, 'lxml')
#all_products_href=soup.find_all(class_='mzr-tc-group-item-href') #Находим общее у всех ссылок которые нам нужны

#all_categories = {}

#for i in all_products_href: #Проходимся по элементам циклом и вычленяем
#    item_text = i.text
#    item_href ='https://health-diet.ru' + i.get('href')
#    all_categories[item_text] = item_href #добавляем в словарь название:ссылка

#with open('all_categories_dict.json', 'w', encoding='utf-8') as file: #Запихали в отдельный файл
#    json.dump(all_categories, file, indent=4, ensure_ascii=False)
#print(all_categories)
#print(all_products_href)


with open("all_categories_dict.json", encoding='utf-8') as file:
    all_categories = json.load(file)
iteration_count = int(len(all_categories))
count = 0

for category_name, category_href in all_categories.items():
    count += 1
    rep = [',', " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')
#    print(category_name)
#
#    req = requests.get(url=category_href, headers=headers)
#    src = req.text
#    Создаем html файлы
#    with open(f"data/{count}{category_name}.html", "w", encoding='utf-8') as file:
#        file.write(src)
        #Лазаем по html
    with open(f"data/{count}{category_name}.html",  encoding='utf-8') as file:
        src = file.read()

        #Заводим суп и ищем в нем заголовки
    soup = BeautifulSoup(src, "lxml")
        #Проверка есть ли в файле то что нам надо
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th") #Ищем заголовки
    product = table_head[0].text
    callories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    yglevodi = table_head[4].text
        #После того как нашли тексты заголовков Создаем csv файл и втыкаем в него значения
    with open(f"data/{count}{category_name}.csv", "w", encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow((product, callories, proteins, fats, yglevodi))

    products_data = soup.find(class_="mzr-tc-group-table").find('tbody').find_all("tr")  #находим заголовки
    for item in products_data:   #Проходимся по заголовкам и присваем значения
        product_tds = item.find_all('td')

        product = product_tds[0].find('a').text
        callories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        yglevodi = product_tds[4].text

        with open(f"data/{count}{category_name}.csv", "a", encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow((product, callories, proteins, fats, yglevodi))
    print(f'# Итерация {count}. {category_name} записан')
    iteration_count -= 1
    print(f'{iteration_count} осталось')
        #Ищем заголовки