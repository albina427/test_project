import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'}
    ]
def work(url, city=None, language=None):
    vacancies = []
    errors = []
    domain = 'https://www.work.ua/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id="pjax-job-list")
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    description = div.p.text
                    div_company = div.find('div', attrs={'class': 'add-top-xs'})
                    company = div_company.span.text
                    # company = 'No name'
                    # logo = div.find('img')
                    # if logo:
                    #     company = logo['alt']
                    vacancies.append({'title': title.text, 'url': domain + href, 'description': description,
                                 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Page structure changed'})
        else:
            errors.append({'url': url, 'title': 'Page do not respond'})

    return vacancies, errors
def rabota(url, city=None, language=None):
    vacancies = []
    errors = []
    domain = 'https://rabota.ua/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'f-text-gray fd-craftsmen'})
            if not new_jobs:
                table = soup.find('table', id="ctl00_content_vacancyList_gridList")
                if table:
                    tr_lst = table.find_all('tr', attrs={'id': True})
                    for tr in tr_lst:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = tr.find('h2', attrs={'class': 'card-title'})
                            href = title.a['href']
                            description = div.find('div', attrs={'class': 'card-description'}).text
                            company = div.find('a', attrs={'class': 'company-profile-name'}).text
                            # company = 'No name'
                            # logo = div.find('img')
                            # if logo:
                            #     company = logo['alt']
                            vacancies.append({'title': title.text, 'url': domain + href, 'description': description,
                                     'company': company,
                                      'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': 'Table does not exist'})
            else:
                errors.append({'url': url, 'title': 'No vacancies for this request'})
        else:
            errors.append({'url': url, 'title': 'Page do not respond'})

    return vacancies, errors
def dou(url, city=None, language=None):
    vacancies = []
    errors = []
    # domain = 'https://www.work.ua/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id="vacancyListId")
            if main_div:
                li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_lst:
                    div_title = li.find('div', attrs={'class': 'title'})
                    title = div_title.find('a', attrs={'class': 'vt'})
                    href = div_title.a['href']
                    description = li.find('div', attrs={'class': 'sh-info'}).text
                    div_company = li.find('a', attrs={'class': 'company'})
                    company = div_company.text
                    # company = 'No name'
                    # logo = div.find('img')
                    # if logo:
                    #     company = logo['alt']
                    vacancies.append({'title': title.text, 'url': href, 'description': description,
                                 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Page structure changed'})
        else:
            errors.append({'url': url, 'title': 'Page do not respond'})

    return vacancies, errors
def djinni(url, city=None, language=None):
    vacancies = []
    errors = []
    domain = 'https://djinni.co/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_lst = main_ul.find_all('li', attrs={'class': 'list-jobsitem'})
                for li in li_lst:
                    title = li.find('div', attrs={'class': 'list-jobstitle'})
                    href = title.a['href']
                    description = li.find('div', attrs={'class': 'list-jobsdescription'}).text
                    div_company = li.find('div', attrs={'class': 'list-jobsdetails__info'})
                    company_recr = div_company.a
                    company = company_recr.find_next('a')
                    # company = 'No name'
                    # logo = div.find('img')
                    # if logo:
                    #     company = logo['alt']
                    vacancies.append({'title': title.text, 'url': domain + href, 'description': description,
                                 'company': f'{company_recr.text}. {company.text}',
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Page structure changed'})
        else:
            errors.append({'url': url, 'title': 'Page do not respond'})

    return vacancies, errors
if __name__ == 'main':
    url = 'https://djinni.co/jobs/location-kyiv/?keywords=Python'
    vacancies, errors = djinni(url)

    with codecs.open('../work.txt', 'w', 'utf-8') as file:
        file.write(str(vacancies))