from bs4 import BeautifulSoup
import requests
from requests.models import Response
from dataclasses import dataclass


@dataclass
class Сurrencies:
    url: str = "https://www.cbr.ru/currency_base/daily/"
    
    def get_html(self) -> Response:
        """
        Getting html code https://www.cbr.ru/currency_base/daily/
        """
        return requests.get(self.url)

    def get_content(self) -> list[float]:
        """
        Getting currency pairs rub/eur, eur/usd, eur/kzt
        """
        soup = BeautifulSoup(self.html.text, 'html.parser')
        items = soup.find_all('td', class_='')
        for i, item in enumerate(items):
            if item.text == "Евро":
                rub_eur = items[i+1].text.replace(',','.')
            elif item.text == "Доллар США":
                usd = items[i+1].text.replace(',','.')
            elif item.text == "Казахстанских тенге":
                kzt = items[i+1].text.replace(',','.')

        # calculation of currency pairs
        rub_eur, usd, kzt = map(float, (rub_eur, usd, kzt))
        eur_usd = round(rub_eur / usd, 4)
        eur_kzt = round(rub_eur / (kzt / 100), 4)
        return rub_eur, eur_usd, eur_kzt
    
    def parser_currencies(self):
        """
        Return currency pairs rub/eur, eur/usd, eur/kzt or print server error
        """
        self.html = self.get_html()
        status = self.html.status_code
        if status == 200:  # checking the server response
            return self.get_content()
        else:
            print("Error response!\nCode error: ", status)

# c = Сurrencies()
# pairs = c.parser_currencies()
# print(pairs)
