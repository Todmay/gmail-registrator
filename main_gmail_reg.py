### для работы браузера
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
### отдельный элемент для выпадающих списков
from selenium.webdriver.support.ui import Select
import os

import time
import random

### для запросов в сервис
import requests 
from requests.sessions import Session
from stem import Signal
from stem.control import Controller

# Библиотека для работы с Google Sheets API
import gspread
# Аутентификация
from oauth2client.service_account import ServiceAccountCredentials

#### импортируем конфиг, делаю поотдельности чтобы не забыть что я именно там сохранил
from config import API_KEY
from config import default_country_id
from config import spreadsheet_id
from config import spreadsheet_name
from config import CREDENTIALS_FILE

base_delay = 2

#### all xpath ####

# кнопка создания
create_new_path = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/button'
create_pop_person_path = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div/ul/li[1]'

# меню заполнения
first_name_path = '//*[@id="firstName"]'
second_name_path = '//*[@id="lastName"]'
login_path = '//*[@id="username"]'
password_path = '//*[@id="passwd"]/div[1]/div/div[1]/input'
confirm_password_path = '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input'
nextt_path = '//*[@id="accountDetailsNext"]/div/button'
already_exist_path = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/div[2]/div/span'

##### меню телефона

phone_number_path = '//*[@id="phoneNumberId"]'
phone_next_path = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button' 

#### меню кода
code_enter_path = '//*[@id="code"]'
code_next_path = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'

#### форма др

reserv_email_path = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input'
day_path = '//*[@id="day"]'
month_path = '//*[@id="month"]'
month_option_path = '//*[@id="month"]/option[2]'
year_path = '//*[@id="year"]'
pol_path = '//*[@id="gender"]'
pol_options_path = '//*[@id="gender"]/option[2]'
ff_nextt_path = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'

### после формы др

skip_path = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button'

### после скип

acsept_path = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'

#### all xpath ####

##### функциии подключения и работы с гугл доком

def google_sheet_coonect():

### для работы импортировать конфиг, два способа, использую второй
#credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
#httpAuth = credentials.authorize(httplib2.Http())
#service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    gc = gspread.authorize(credentials)
    # Открытие документа
    sheet = gc.open(spreadsheet_name)
    # Выбор листа
    worksheet = sheet.get_worksheet(0)

    # получаем список всех строк
    rows = worksheet.get_all_values()
    
    # считаем количество строк с непустыми значениями
    non_empty_rows = 0
    for row in rows:
        if any(row):
            non_empty_rows += 1


    return worksheet, non_empty_rows

def google_sheet_data_grub(worksheet, row_number = 1):
    # Считывание строки
    row = worksheet.row_values(row_number)
    # Запись в переменные разных колонок
    firstname = row[0]
    secondname = row[1]
    c_login = row[2]
    c_pass = row[3]
    pic_url = row[4]
    try:
        status = row[6]
    except:
        status = ''


    return firstname, secondname, c_login, c_pass, pic_url, status 

def google_sheet_data_log(worksheet, row_number, phone, status):
    # Записываем значение в строку
    worksheet.update_cell(row_number, 6, phone)
    worksheet.update_cell(row_number, 7, status)

    return None

####### функции работы с вебдрайвером
def browser_open():

# Инициализируем драйвер
# путь указывается только в случаях когда драйвер не установлен или не включен по умолчанию, указывается пусть в скобка веб драйвера
# пример пути если драйвер находится в каталоге скрипта
# path = '.\chromedriver_win32'
# сейчас на случай отсутствия драйвера он принудительно устанавливается при первом запуске

    driver = webdriver.Chrome(ChromeDriverManager().install())

# Открываем нужную вкладку
    driver.get("https://gmail.com/")
    time.sleep(base_delay)

    return driver


def browser_close(driver):
### закрываем браузер
    driver.quit()
    time.sleep(base_delay)

    return None

def start_create(driver):
# если не находит кнопку, то ждем еще немного и повторяем, рекурсия
    try:
    	# Кликаем на переход к отправке
        create_new = driver.find_element(by=By.XPATH, value=create_new_path)
        create_new.click()
        time.sleep(base_delay)
    except:    
    	print('Нет кнопки создать страницу')
    	time.sleep(base_delay*4)
    try:
    	# Кликаем на переход к отправке
        pop_person = driver.find_element(by=By.XPATH, value=create_pop_person_path)
        pop_person.click()
    except:    
        print('Нет выпадающего списка')
        time.sleep(base_delay*4)
        start_create(driver)

    return None

def text_login_pull(driver, first_name_text, second_name_text, login_text, password_text):
# если окно заполнения логина не успело повиться, ждем немного и повторяем, РЕКУРСИЯ
    no_status = False

    try:
# Находим и заполняем
        first_name = driver.find_element(by=By.XPATH, value=first_name_path)
        first_name.send_keys(first_name_text)
        second_name = driver.find_element(by=By.XPATH, value=second_name_path)
        second_name.send_keys(second_name_text)
        login = driver.find_element(by=By.XPATH, value=login_path)
        login.send_keys(login_text)
        password = driver.find_element(by=By.XPATH, value=password_path)
        password.send_keys(password_text)
        confirm_password = driver.find_element(by=By.XPATH, value=confirm_password_path)
        confirm_password.send_keys(password_text)
        nextt = driver.find_element(by=By.XPATH, value=nextt_path)
        nextt.click()
    except:    
    	print('Окошко для текста смс не прогрузилась')
    	time.sleep(base_delay*2)
    	text_pull(driver, sms_text)

    time.sleep(base_delay*2)
#### если логин уже есть создаст не даст, на проверку отдельный выход
    try:
        if (driver.find_element(by=By.XPATH, value=already_exist_path)): exist = True
    except:
        exist = False

    if exist:
        print('Такой логин уже занят')
        time.sleep(base_delay*2)
        no_status = True

        return no_status

    return no_status

def text_phone_pull(driver, number):
    phone_number = driver.find_element(by=By.XPATH, value=phone_number_path)
    phone_number.send_keys(number)
    time.sleep(base_delay*4)
    ## нужно перед нажатием кнопки подождать так происходит подстановка кода СМС и прогрузка кода страны
    phone_next = driver.find_element(by=By.XPATH, value=phone_next_path)
    phone_next.click()


    return None

def text_code_pull(driver, code):
    code_enter = driver.find_element(by=By.XPATH, value=code_enter_path)
    code_enter.send_keys(code)
    time.sleep(base_delay)
    ## нужно перед нажатием кнопки подождать
    code_next = driver.find_element(by=By.XPATH, value=code_next_path)
    code_next.click()

    return None

def avatar_pull(driver):

    return None


def last_form_pull(driver):
    random_day = random.randint(1, 25)
    day = driver.find_element(by=By.XPATH, value=day_path)
    day.send_keys(random_day)
    random_year = random.randint(1970, 2000)
    year = driver.find_element(by=By.XPATH, value=year_path)
    year.send_keys(random_year)
    select_month = Select(driver.find_element(by=By.XPATH, value=month_path))
    select_month.select_by_value('2')
    time.sleep(base_delay*2)
    select_pol = Select(driver.find_element(by=By.XPATH, value=pol_path))
    select_pol.select_by_value('1')
    time.sleep(base_delay*2)

    last_next = driver.find_element(by=By.XPATH, value=ff_nextt_path)
    last_next.click()



    return None

def last_step_clk(driver):
    time.sleep(base_delay*4)
    # ждем чтобы кнопка появилась

    skip = driver.find_element(by=By.XPATH, value=skip_path)
    skip.click()

    time.sleep(base_delay*4)
    # ждем чтобы кнопка появилась
    acsept = driver.find_element(by=By.XPATH, value=acsept_path)
    acsept.click()
    time.sleep(base_delay*4)

    return None

###### далее блок функций касающих смс
def sms_balance_not_tor():
    response = requests.get(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=getBalance")
    print(response.text)

    return None

def sms_balance_not_tor():
    response = requests.get(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=getBalance")
    print(response.text)

    return None


### используем для смены IP
def set_new_ip():
    with Controller.from_port(port = 9151) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    return None

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

def sms_balance_tor():
    #Запрос Баланса
    response = get_from_tor_net(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=getBalance")
    
    balance = False 
    if response.text == 'NO_BALANCE':
        print(response.text)
        print('денег нет')
    else:
        balance = True

    return balance

def sms_get_number():

    #Запрос номера
    response = get_from_tor_net(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=getNumber&service=go&country={default_country_id}")
    print(response)
    rtext = response.text
    print(rtext)
    number_response = rtext
    number = number_response.split(':')[-1]
    id_number = number_response.split(':')[-2]

    return number, id_number

def sms_cancel_number(id_number):

    #отмена активации
    response = get_from_tor_net(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=setStatus&status=8&id={id_number}")

    return response.text

def sms_again_number(id_number):

    #отмена активации
    response = get_from_tor_net(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=setStatus&status=3&id={id_number}")

    return response.text

def sms_status_and_code(id_number):

    #получение статуса по номеру
    response = get_from_tor_net(f"https://smshub.org/stubs/handler_api.php?api_key={API_KEY}&action=getStatus&id={id_number}")

    status_text = response.text
    code = ''
    if 'STATUS_OK' in status_text:
        code = status_text.split(':')[-1]

    return response.text, code

#### блок функций касающийся ведения логов ####
# Логирование и защита от повторного создания
def logs_check(login, l_pass):
    # Создаем файл если его нет файл для записи
    log = open('logs.txt', 'a+')
    log.close()
    # Читаем весь файл
    log = open('logs.txt', 'r')
    data = log.read()
    log.close()
    is_not_create = False
    if login not in data:
#        log = open('logs.txt', 'a')
#        log.write(f'{login} : {l_pass} \n')
#        log.close()
        is_not_create = False
    else:
        is_not_create = True
        print('С таким логином уже создавали ' + login)
    # Закрываем файл
    
    return is_not_create

def logs_write(text):
    # Создаем файл если его нет файл для записи
    log = open('logs.txt', 'a+')
    log.close()
    # Читаем весь файл
    log = open('logs.txt', 'a')
    log.write(text)
    log.close()
    # Закрываем файл

    return None

#### сохраняем старый номер телефона
def last_number_write(number, id_number):
    # Создаем файл если его нет файл для записи
    f = open('last_number.txt', 'a+')
    f.close()
    # Читаем весь файл и перезаписываем если в нем что-то есть
    with open('last_number.txt', 'w') as f:
        f.write(number + '\n')
        f.write(id_number + '\n')

    # Закрываем файл

    return None

def last_number_get():
    try:
        with open('last_number.txt', 'r') as f:
            number = f.readline().strip()
            id_number = f.readline().strip()
    except:
        number = ''
        id_number = ''


    return number, id_number

def last_number_check():
    check = True

    if os.path.exists('last_number.txt'):
        with open('last_number.txt') as f:
            if f.read():
                 print('В файле с телефонами есть содержимое')
                 check = True
            else:
                 print('Файл пустой')
                 check = False
    else:
         print('Файла с телефонами не существует')
         check = False
#### по умолчанию мы не будем создавать новый номер, а пытаемся использовать существующий
    return check

#### функция запроса нового номера

def new_number_activate():
    if sms_balance_tor():
        number, id_number = sms_get_number()
        last_number_write(number, id_number)
    else:
        number = 'Денеги кончились'
        id_number = 'Денеги кончились'
    return number, id_number




worksheet, row_count  = google_sheet_coonect()

for row_num in range(1, row_count+1):
    firstname, secondname, c_login, c_pass, pic_url, status = google_sheet_data_grub(worksheet, row_num)
    
    # скипуем если в гугл доке уже такой есть
    ##### EXIT #######    ##### EXIT #######
    if status == 'СОЗДАН': continue


    # открываем форму и драйвер    
    driver = browser_open()
    start_create(driver)
    time.sleep(base_delay*2)
    

    if text_login_pull(driver, firstname, secondname, c_login, c_pass): 
        google_sheet_data_log(worksheet, row_num, '', 'С таким логином и паролем не создать')
        time.sleep(base_delay*2)
        browser_close(driver)
        continue
            ##### EXIT #######    ##### EXIT #######    ##### EXIT #######

    #скипуем если в гугл доке уже такой есть
    if logs_check(c_login, c_pass): 
        google_sheet_data_log(worksheet, row_num, '', 'Такой логин уже есть в логах')
        continue
    ##### EXIT #######    ##### EXIT #######

    #time.sleep(base_delay*2)


    #### проверяем есть номер от прошлого запуска
    last_number, last_id_number = last_number_get()
    ### если нет, то запрашиваем новый
    if last_number == '': 
        number, id_number = new_number_activate()
    else:
        ### если есть, то проверяем не протух ли он
        status_last_number, code = sms_status_and_code(last_id_number)
        ### если номер получил код, то пробуем его заставить получить еще один код
        if 'STATUS_OK' in status_last_number: 
            status_again = sms_again_number(last_id_number)
        ### если номер готов получить новый код, то работаем с ним
            if 'ACCESS_READY' in status_again or 'ACCESS_RETRY_GET' in status_again: 
                 ### то работаем с этим номером
                number = last_number
                id_number = last_id_number
            else:
                number, id_number = new_number_activate()
        else:
            number, id_number = new_number_activate()
            ### если номер не готов получить новый код, то получаем новый номер
    if number == 'Денеги кончились':
        print('Денеги кончились')
        break

    #time.sleep(base_delay*2)

    text_phone_pull(driver, '+' + number)
    ### после ввода номера страница с кодом появляется не сразу, нужно больше ожидания
    time.sleep(base_delay*6)


    status, code = sms_status_and_code(id_number)
    print(status)
    print(code)
    if status == 'STATUS_WAIT_CODE':
    #если на момент запроса идет ожидание кода, ждем и повторяем
        time.sleep(10)
        status, code = sms_status_and_code(id_number)
        print(status)
        print(code)


    text_code_pull(driver, code)

    time.sleep(base_delay*2)

    last_form_pull(driver)

    time.sleep(base_delay*2)

    last_step_clk(driver)

# длинное время создания так как после создания идет вход в аккаунт, которого по всей видимости надо дождаться
    time.sleep(200)


    logs_write(f'Логин создан - {c_login} : {c_pass} \n')

    time.sleep(base_delay*2)



    browser_close(driver)

    continue

try: 
    browser_close(driver)
except:
    print('Ой? Уже закрылся...')    

print('Работа скрипта закончена....')
print('Для повтора перезапустите скрипт....')
print('Хорошего дня....')







