import requests 
from requests.sessions import Session
from stem import Signal
from stem.control import Controller

#### импортируем конфиг
from config import API_KEY
from config import default_country_id

def get_from_tor_net(select):
    # Инициализация сессии
    session = Session()
    # Задаем прокси сервер
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }
    # Задаем необходимые параметры запроса
    params = {
        'api_key': API_KEY
    }
    # Делаем запрос и получаем ответ
    response = session.get(select)
    # Изменяем IP
    #set_new_ip()

    return response

def sms_status_and_code(id_number):

    #получение статуса по номеру
    response = get_from_tor_net(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=getStatus&id={id_number}")

    status_text = response.text
    code = ''
    if 'STATUS_OK' in status_text:
        code = status_text.split(':')[-1]

    return response.text, code


def sms_cancel_number(id_number):

    #отмена активации
    response = get_from_tor_net(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=setStatus&status=8&id={id_number}")

    return response.text

def last_number_get():
    with open('last_number.txt', 'r') as f:
        number = f.readline().strip()
        id_number = f.readline().strip()

    return number, id_number

number, id_number = last_number_get()

response = sms_cancel_number(id_number)

print(response)


#status, code = sms_status_and_code(id_number)
#print(status)
#print(code)


