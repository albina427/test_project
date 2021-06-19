import requests
import codecs
from bs4 import BeautifulSoup as BS


headers = {}



def work(url):
    vacancies = []
    errors = []
    domain = 'https://www.work.ua'

    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_lst:
                title = div.find('h2').text
                href = title.a['href']
                description = div.p.text
                div_company = div.find('div', attrs={'class': 'add-top-xs'})
                company = div_company.span.text

                # company = 'No name'
                # logo = div.find('img')
                # if logo:
                #     company = logo['alt']
                #
                vacancies.append({'title': title.text, 'url': domain + href, 'description': description,
                                            'company': company})
        else:
            errors.append({'url': url, 'title': "Div does not exist"})


    else:
         errors.append({'url': url, 'title': "Page do not respond"})
    return vacancies, errors


def rabota(url):
    vacancies = []
    errors = []
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        table = soup.find('table', id='ct100_content_vacancyList_gridList')
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
                    vacancies.append({'title': title.text, 'url': domain + href,
                                      'description': description,
                                      'company': company})
                else:
                    errors.append({'url': url, 'title': "Card body div not found"})

        else:
            errors.append({'url': url, 'title': "Table does not exist"})


    else:
         errors.append({'url': url, 'title': "Div does not exist"})
    return vacancies, errors

if __name__ == '__main__':
    url = 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
    vacancies, errors = rabota(url)
with codecs.open('work.txt', 'w', 'utf-8') as file:
        file.write(str(vacancies))

# file = open('work.html', 'w')
# file.write(str(resp.content))
# file.close()