'''
    все объявления: main class = vacancy-serp-content
    одно объявление: div class = vacancy-serp-item-body
    1) href:  tag_name  h3 -> tag_name "a"  bloko-header-section-3
    2) зарплата: span class = bloko-header-section-2
    3) город: "div.vacancy-serp-item__info > div.bloko-text"
    4) компания: (in vacance) span, class_="vacancy-company-name
    5) ключевые навыки: (in vacance: list [str]) "div", class_="bloko-tag-list"
'''
import json
import random
import re

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import os

from d_2 import logger

path = 'log_d_3.log'


# @logger(path)
def gen_headers():
    browser = random.choices(["chrome", "firefox", "opera"])[0]
    os = random.choices(["win", "mac", "lin"])[0]
    headers = Headers(browser=browser, os=os)
    return headers.generate()


# @logger(path)
def search_for_vacancies():
    global count, title, response, pattern, f
    
    main_html = response.text
    main_soup = BeautifulSoup(main_html, "lxml")
    vacancies_list_tag = main_soup.find("main", class_="vacancy-serp-content")
    vacancies_tags = vacancies_list_tag.find_all(class_="vacancy-serp-item-body")
    vacancies_parsed = []
    count = 0
    for vacance_tag in vacancies_tags:
        h3_tag = vacance_tag.find("h3", class_="bloko-header-section-3")
        a_tag = h3_tag.find("a")
        link_1 = a_tag["href"]
        print('link:', link_1)
        title = h3_tag.text.strip() if h3_tag else "название vacance не загрузилось"
        salary_tag = vacance_tag.find("span", class_="bloko-header-section-2")
        salary = salary_tag.text.strip().replace('\u202f', '').replace('\xa0',
                                                                       '') if salary_tag else "Зарплата не указана"
        city_tag = vacance_tag.select("div.vacancy-serp-item__info > div.bloko-text")
        city = (city_tag[0].text).split(',')[0]
        
        response = requests.get(link_1, headers=gen_headers())
        
        if response.status_code == 200:
            get_vacance(city, link_1, response, salary, title, vacancies_parsed)
        else:
            print(f"проблемная ссылка на вакансию {title}")
    print(f"Найдено {count} вакансий для ключевых навыков django или flask")
    print('в файл загружено вакансий: ', len(vacancies_parsed))
    pprint(vacancies_parsed)
    file_path = os.path.join(os.getcwd(), 'vacancies.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(vacancies_parsed, f, ensure_ascii=False, indent=4)


@logger(path)
def get_vacance(city, link_1, response, salary, title, vacancies_parsed):
    global count, pattern
    vacance_html = response.text
    vacance_soup = BeautifulSoup(vacance_html, "lxml")
    company_tag = vacance_soup.find("span", class_="vacancy-company-name")
    company = company_tag.text.strip().replace('\xa0', ' ') if company_tag else "Компания не занрузилась"
    print('company', company, 'salary', salary)
    skill_list = vacance_soup.find_all("div", class_="bloko-tag-list")
    for skill in skill_list:
        skill_text = skill.text
        if "django" in skill_text.lower() or "flask" in skill_text.lower():
            count += 1
            print("Yes!!!", count)
            pattern = '\₽'
            salary = re.sub(pattern, 'руб.', salary)
            pattern = '\$'
            salary = re.sub(pattern, 'USD', salary)
            vacance_dict = {
                "title": title,
                "City": city,
                "company": company,
                "salary": salary,
                "link": link_1,
            }
            print(vacance_dict)
            vacancies_parsed.append(vacance_dict)


if __name__ == '__main__':
    response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=gen_headers())
    
    if response.status_code == 200:
        search_for_vacancies()
    else:
        print("проблема с подключением к сайту HH")

