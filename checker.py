import random,time
import requests
from bs4 import BeautifulSoup
import csv
import re
import random
import datetime
def result():
	return "Процесс заверен"
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
	soup = BeautifulSoup(html, 'lxml')
	flat_item = soup.find_all('div', class_='item__line')
	print('Lenght',len(flat_item))
	count = 0
		
	for info in flat_item:
		try:
			name = info.find('a', class_ = 'snippet-link').text.strip()
		except:
			name = ''
		try:
			url = info.find('a', class_ = 'snippet-link').get('href')
			full_url = 'https://www.avito.ru'+ url
		except:
			full_url = ''
		phone_number = phn()
		datetime_object = datetime.datetime.now()
		# print(name + '\n',url)
		# print(phone_number)
		print('___________________________________')
		data = {'name' : name,
				'url' : full_url,
				'phone_number' : phone_number,
				'datetime' : datetime_object}
		count += 1		
		write_csv(data)
		time.sleep(2)
def main():

	url = 'https://www.avito.ru/kazan/kvartiry/sdam/na_dlitelnyy_srok?cd=1&rn=25934'
	soup = BeautifulSoup(get_html(url), 'lxml')
	pages_count = soup.find_all('span', class_='pagination-item-1WyVp')
	pages_count = int(pages_count[7].text.strip()) + 1
	#for i in range(pages_count):
	url = 'https://www.avito.ru/kazan/kvartiry/sdam/na_dlitelnyy_srok?cd=1&rn=25934&p=1' #+ str(i)
		
	get_page_data(get_html(url))
		#time.sleep(25)
		
if __name__ == '__main__':
    main()