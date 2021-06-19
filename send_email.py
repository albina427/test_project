import os, sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives


path_proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(path_proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

django.setup()

from myapp.models import Vacancy, Error, URL
from test_project.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Дневная рассылка вакансий на {today}'
text_content = 'Дневная рассылка вакансий'
from_email = EMAIL_HOST_USER
alt = '<2>На сегодня вакансий не найдено:)<2>'

User = get_user_model()
qs = User.objects.filter(mailing=True).values('city', 'language', 'email')


users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])

if users_dct:
    params = {'city_id': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['city_id__in'].append(pair[1])
        qs = Vacancy.object.filter(**params, timestamp=today).value()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id'], []))
        vacancies[(i['city_id'])], i['language_id'].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{row["url"]}" target="_blank">{row["title"]}</a></h5>'
            html += f'<h5>{row["company"]}</h5>'
            html += f'<p>{row["description"]}<p><br><hr>'
        _html = html if html else alt
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html, "text/html")
            msg.send()


qs = Error.object.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''

if qs.exist():
    error = qs.first()
    data = error.data.get('errors', [])

    for i in data:
        _html += f'<p>Error: <a href="{i["url"]}">{i["title"]}</a><p>'
        subject += f'Ошибка сбора вакансий{today}. '
        text_content += 'Ошибка'

    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Запрос на добавления вакансии(ий)</h2>'
    for i in data:
        _html += f'<p>Город: {i["city"]}, ЯП: {i["language"]}. Почта для ответа: {i["email"]} </p>'
        subject += f'Запрос на добавления вакансии(ий) {today}. '
        text_content += 'Запрос'
qs = URL.object.all().values('city', 'language')
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_errors = ''
for keys in users_dct.keys():
            if keys not in urls_dct:
                urls_errors += f'<p>Для города: {keys[0]}и ЯП: {keys[1]} отсутствуют ссылки.</p>'

if urls_errors:
    subject += f'Отсутствующие ссылки. '
    text_content += 'Отсутствующие ссылки'
    _html += '<hr>'
    _html += '<h2>Отсутствующие ссылки</h2>'

    _html += urls_errors
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()

