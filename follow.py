import random,time
import requests
from bs4 import BeautifulSoup
import csv
import re
import random
import datetime
import os

def del_list():
	f = open('/home/pasha/Рабочий стол/list.txt', 'w')
	f.close()

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

def write_csv(data):
    with open('property.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['url'], data['phone_number'],data['datetime']))

def get_html(url):
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36'}
	r = requests.get(url,headers=headers)
	if r.ok:
		return r.text
	raise Exception('Status_code:',r.status_code)


def get_page_data(html):
	global msg_answer
	msg_answer = None
	soup = BeautifulSoup(html, 'lxml')
	flat_items = soup.find_all('div', class_='item__line')
	
	if os.stat("/home/pasha/Рабочий стол/list.txt").st_size == 0:
		with open ("/home/pasha/Рабочий стол/list.txt", 'w') as w:
			for flat in flat_items:
				flat_id = flat.find('a', class_ = 'snippet-link').get('href').split('_')[-1]
				w.write(str(flat_id) + ' ')	
		
	with open ("/home/pasha/Рабочий стол/list.txt") as w:
		s1 = w.readline().strip() 
		l=s1.split(' ')
	
	name_list=[]
	
	for flat in flat_items:
		flat_id = flat.find('a', class_ = 'snippet-link').get('href').split('_')[-1]
		
		if flat_id not in l:
			l.insert(0,flat_id)
			if len(l)>60:
				l.pop()
			with open ("/home/pasha/Рабочий стол/list.txt", 'w') as w:
				for i in l:
					w.write(str(i) + ' ')
			try:
				name = flat.find('a', class_ = 'snippet-link').text.strip()
				name_list.append(name)
			except:
				name = ''
			try:
				url = flat.find('a', class_ = 'snippet-link').get('href')
			except:			
				url=''
			phone_number = phn()
			datetime_object = datetime.datetime.now()
			data={ 'name' : name,
			       'url' : url,
			       'phone_number' : phone_number,
			       'datetime' : str(datetime_object) }
			write_csv(data)
			msg_answer = data['name'] + '\n' + data['url'] + '\n' + data['phone_number'] + '\n' + data['datetime']
			
def main():
	count = 0
	url = 'https://www.avito.ru/rossiya/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1'
	
	#try:
	get_page_data(get_html(url))
	time.sleep(random.randint(18, 26))
	count+=1
	if msg_answer is not None:
		return msg_answer
	else:
		print(msg_answer)
	#except:
		#print('Конкретно не работает.Отправил:',count,' ','запросов')	

if __name__ == '__main__':
	main()	
