import random,time
import requests
from bs4 import BeautifulSoup
import csv
import re
import random
import datetime

def phn():
    phone=list('00000')
    first = [917,987,952,999,950,953,960,905,968,966]
    phone[0] = str(8)
    phone[1] = str(random.choice(first))
    phone[2] = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    phone[3] = str(random.randint(0,9)) + str(random.randint(0,9))
    phone[4] = str(random.randint(0,9)) + str(random.randint(0,9))
    result = phone[0] + ' ' + phone[1] + ' ' + phone[2] + '-' + phone[3] + '-' + phone[4]
    return result

def get_html(url):
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36'}
	r = requests.get(url,headers=headers)
	if r.ok:
		return r.text
	raise Exception('Status_code:',r.status_code)

def write_csv(data):
    with open('property.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['url'], data['phone_number'],data['datetime']))

#url = '/home/pasha/Рабочий стол/parserproperty_bot/Аренда квартир.html'
def get_page_data(html):
	global msg_answer 
	soup = BeautifulSoup(html, 'lxml')
	flats_id = set()
	""" реализовать файл,хранящий множество id"""

	flat_item = soup.find('div', class_='item__line')
	flat_id = flat_item.find('a', class_ = 'snippet-link').get('href').split('_')[-1]
	
	if flat_id not in flats_id:
		try:
			name = flat_item.find('a', class_ = 'snippet-link').text.strip()
		except:
			name = ''
		try:
			url = flat_item.find('a', class_ = 'snippet-link').get('href')
			full_url = 'https://www.avito.ru'+ url
		except:
			full_url = ''
		phone_number = phn()
		datetime_object = datetime.datetime.now()	

		data = {'name' : name,
				'url' : full_url,
				'phone_number' : phone_number,
				'datetime' : str(datetime_object)}
			
		write_csv(data)
		msg_answer = data['name'] + '\n' + data['url'] + '\n' + data['phone_number'] + '\n' + data['datetime']
		flats_id.add(flat_id)	
def main():
	while True:
		url = 'https://www.avito.ru/rossiya/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' 
		get_page_data(get_html(url))
		return msg_answer
		time.sleep(180)
			
		
if __name__ == '__main__':
    main()