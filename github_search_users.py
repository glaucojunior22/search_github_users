# -*- coding: utf-8 -*-
import requests
import codecs

print 'Welcome to the Github search users script!'
print 'In order to use this script you will need a access token from Github'
print 'To get a token acess: https://github.com/developer/register'
print 'Note: You will need a paid account to get a token'
print 'If you do not input a access token the Github API limits your requets.'
token = raw_input('Enter your access token: ').strip()
city = raw_input('Enter the city to find Developers: ').strip()
language = raw_input('Enter the programming language: ').strip()
url = 'https://api.github.com/search/users?'
token = 'access_token=%s' % token
query = 'q=language:%s+location:%s' % (language, city)
api_url = '{0}{1}&{2}'.format(url, token, query)
response = requests.get(api_url)
json = response.json()
count = json['total_count']
pages = count / 30
if count % 30 > 0:
    pages += 1
items = json['items']
urls = [x['url'] for x in items]
for i in xrange(2, pages + 1):
    api_url += '&page={}'.format(i)
    response = requests.get(api_url)
    json = response.json()
    items = json['items']
    if items:
        urls += [x['url'] for x in items]
    else:
        break
users = ''
for url in urls:
    res = requests.get('{0}?{1}'.format(url, token))
    info = res.json()
    if info['email']:
        email = info['email'].replace(' at ', '@').replace(' dot ', '.')
        users += 'Nome: ' + info['name'].ljust(40)
        users += 'Email: ' + email
        users += '\r\n'

text_file = '%s_%s.txt' % (city, language)
with codecs.open(text_file, 'w', 'utf-8') as txt:
    txt.write(users)
