from dotenv import load_dotenv

import csv
import requests
import time
import yagmail
import os

load_dotenv()
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
PASSWORD = os.getenv('PASSWORD')

SLEEP_TIME = 0

SUBJECT = 'Coronavirus Stats for your country.'

GLOBAL_API_URL = 'https://corona.lmao.ninja/v2/all'
COUNTRY_API_URL = 'https://corona.lmao.ninja/v2/countries/{country}'

yag = yagmail.SMTP(EMAIL_SENDER, PASSWORD)


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def get_global_data():
    r = requests.get(GLOBAL_API_URL).json()
    return r


def get_country_data(country):
    r = requests.get(COUNTRY_API_URL.format(country=country)).json()
    return r


def send_email(email, subject, body):
    time.sleep(SLEEP_TIME)
    yag.send(to=email, subject=subject, contents=body, attachments=None)


def parse_data(name, template, global_data, country_data):
    format_data = {
        'name': name,
        'global_cases': global_data['cases'],
        'global_deaths': global_data['deaths'],
        'global_recovered': global_data['recovered'],
        'country_name': country_data['country'],
        'country_cases': country_data['cases'],
        'country_today_cases': country_data['todayCases'],
        'country_deaths': country_data['deaths'],
        'country_today_deaths': country_data['todayDeaths'],
        'country_recovered': country_data['recovered'],
        'country_active_cases': country_data['active'],
        'country_critical_cases': country_data['critical'],
        'country_cases_per_million': country_data['casesPerOneMillion'],
        'country_deaths_per_million': country_data['deathsPerOneMillion']
    }
    return template.format(**format_data)


def main():
    template = read_file('./template.html')

    with open('./contacts_file.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for name, email, country in reader:
            global_data = get_global_data()
            country_data = get_country_data(country)

            body = parse_data(name, template, global_data, country_data)

            print(
                f'Sending email to {name} at {email} for country \'{country}\'')

            send_email(email, SUBJECT, body)

            print(f'Sent email to {name}')
        else:
            print(f'Sent emails to all {reader.line_num -1 } contacts.')


if __name__ == "__main__":
    main()
