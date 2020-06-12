import yagmail
import csv
import requests
from dotenv import load_dotenv
import os

subject = "Coronavirus Stats for your country."

load_dotenv()
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
PASSWORD = os.getenv('PASSWORD')


def get_global_data():
    global_data = requests.get('https://corona.lmao.ninja/v2/all').json()
    global_cases = global_data['cases']
    global_deaths = global_data['deaths']
    global_recovered = global_data['recovered']

    return global_cases, global_deaths, global_recovered


def get_country_data(COUNTRY):
    COUNTRY = COUNTRY.lower()
    country_data = requests.get(
        f'https://corona.lmao.ninja/v2/countries/{COUNTRY}').json()
    country_name = country_data['country']
    country_cases = country_data['cases']
    country_today_cases = country_data['todayCases']
    country_deaths = country_data['deaths']
    country_today_deaths = country_data['todayDeaths']
    country_recovered = country_data['recovered']
    country_active_cases = country_data['active']
    country_critical_cases = country_data['critical']
    country_cases_per_million = country_data['casesPerOneMillion']
    country_deaths_per_million = country_data['deathsPerOneMillion']

    return country_name, country_cases, country_today_cases, country_deaths, country_today_deaths, country_recovered, country_active_cases, country_critical_cases, country_cases_per_million, country_deaths_per_million


def organize(COUNTRY):
    global_cases, global_deaths, global_recovered = get_global_data()
    country_name, country_cases, country_today_cases, country_deaths, country_today_deaths, country_recovered, country_active_cases, country_critical_cases, country_cases_per_million, country_deaths_per_million = get_country_data(
        COUNTRY)

    body = f"""\
    <html>
        <body>
            <h3>Hello {name}</h3>
            <p>Here\'s your daily Coronavirus Stats for your country {country_name}.</p>
            <hr>
            <h4>Global Stats: </h4>
        
            <ul>
                <li>Global Cases: {global_cases}</li>
                <li>Global Deaths: {global_deaths}</li>
                <li>Global Recovered: {global_recovered}</li>
            </ul>

            <h4>Country Stats: </h4>

            <ul>
                <li>Country Name: {country_name}</li>
                <li>Country Cases: {country_cases}</li>
                <li>Country Today Cases: {country_today_cases}</li>
                <li>Country Deaths: {country_deaths}</li>
                <li>Country Today Deaths: {country_today_deaths}</li>
                <li>Country Recovered: {country_recovered}</li>
                <li>Country Active Cases: {country_active_cases}</li>
                <li>Country Critical Cases: {country_critical_cases}</li>
                <li>Country Cases Per Million: {country_cases_per_million}</li>
                <li>Country Deaths per Million: {country_deaths_per_million}</li>
            </ul>
            <hr>
            <p>By SyedAhkam</p>
        </body>
    </html>"""

    return body


if __name__ == "__main__":
    with open("./contacts_file.csv") as file:
        reader = csv.reader(file)
        next(reader)
        for name, email, country in reader:
            print(f"Sending email to {name}")

            body = organize(country)

            yag = yagmail.SMTP(EMAIL_SENDER, PASSWORD)
            yag.send(
                to=email,
                subject=subject,
                contents=body,
                attachments=None,
            )
            print(f'Email sent to {email}')
        else:
            print('All emails sent!')
