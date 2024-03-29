
import asyncio
import codecs
import os, sys
import datetime

from django.contrib.auth import get_user_model
from django.db import DatabaseError


path_proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(path_proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

import django
django.setup()


from myapp.parsers import *
from myapp.models import Vacancy, City, Language, Error, URL

User = get_user_model()

parsers = ((work, 'work'),
           (dou, 'dou'),
           (rabota, 'rabota'),
           (djinni, 'djinni'))

vacancies, errors = [], []


def get_settings():
    qs = User.objects.filter(mailing=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = URL.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls
async def main(value):
    func, url, city, language = value
    vac, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    vacancies.extend(vac)

settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

loop.run_until_complete(tasks)
loop.close()

for vac in vacancies:
    v = Vacancy(**vac)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    qs = Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'Errors: {errors}').save()

# for func, url in parsers:
#    v, e = func(url)
#    vacancies += v
#    errors += e
#
#    with codecs.open('../work.txt', 'w', 'utf-8') as file:
#        file.write(str(vacancies))
