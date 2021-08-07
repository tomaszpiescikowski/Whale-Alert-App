import requests
from bs4 import BeautifulSoup
import time
import smtplib, ssl


def whale_not_active():
    return "Subject: The Whale is sleeping...\n\nzzz....."


def whale_active():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get('https://bitinfocharts.com/pl/bitcoin/address/1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ', headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    transaction = soup.find('tr', class_='trb').find_all('td')
    date = transaction[0].find('span').text
    amount = transaction[2].find('span').text.split()[:2]
    prize = transaction[4].text.split()[2]
    sign = amount[0][0]

    if sign == '+':
        return f"Subject: Relax, the Whale is BUYING\n\nDate: {date}\nAmount: {' '.join(amount)}\nBTC price: {prize}"
    else:
        return f"Subject: The Whale is SELLING!!!\n\nDate: {date}\nAmount: {' '.join(amount)}\nBTC price: {prize}"


def check(current_date):
    file = open("C:\\Users\\tomek\\Desktop\\WhaleAlert\\market\\log.txt", "r")
    last_update = file.readline()
    file.close()
    if last_update != current_date + '\n':
        return True
    else:
        return False


def change_first_line(current_date):
    file = open("C:\\Users\\tomek\\Desktop\\WhaleAlert\\market\\log.txt", "r")
    first_line = True
    temp = []
    for line in file:
        if first_line is True:
            temp.append(current_date + '\n')
            first_line = False
        else:
            temp.append(line)
    file.close()
    file = open("C:\\Users\\tomek\\Desktop\\WhaleAlert\\market\\log.txt", "w")
    for i in temp:
        file.writelines(i)
    file.close()


def parsing():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get('https://bitinfocharts.com/pl/bitcoin/address/1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ', headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    transaction = soup.find('tr', class_='trb').find_all('td')
    date = transaction[0].find('span').text
    amount = transaction[2].find('span').text.split()[:2]
    prize = transaction[4].text.split()[2]
    sign = amount[0][0]
    return date, amount, prize, sign


def writing_to_file(date, amount, prize, sign):
    file = open("C:\\Users\\tomek\\Desktop\\WhaleAlert\\market\\log.txt", "a")
    if sign == '+':
        file.writelines("Relax, the Whale is BUYING\n")
    else:
        file.writelines("\nThe Whale is SELLING!!!\n")
    file.writelines(f'Date: {date}\n')
    file.writelines(f'Amount: {" ".join(amount)}\n')
    file.writelines(f'BTC price: {prize}\n\n')
    file.close()


def send_email(receiver_email_address, correct_password):
    date, amount, prize, sign = parsing()
    temp = check(date)

    print(receiver_email_address, correct_password)

    print(type(receiver_email_address), type(correct_password))

    if not temp:
        time.sleep(10)
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "automatedpythonmessage@gmail.com"
        receiver_email = str(receiver_email_address)
        password = str(correct_password)
        message = whale_not_active()
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    else:
        change_first_line(date)
        writing_to_file(date, amount, prize, sign)
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "automatedpythonmessage@gmail.com"
        receiver_email = str(receiver_email_address)
        password = str(correct_password)
        message = whale_active()

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
