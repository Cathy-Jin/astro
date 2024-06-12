from collections import defaultdict
from dataclasses import dataclass
import re
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
import requests

from constants import ASTRO_SEEK_PLANET_DICT, Planet, Sign


@dataclass(frozen=True)
class BirthChartInfo:
    planet_to_sign: Dict[Planet, Sign]
    planet_to_house: Dict[Planet, int]
    aspects: List[str]


class AstroSeek:
    resp: str = None
    url: str = None
    headers: dict = {}

    def __init__(self, resp: str, url: str, headers: dict):
        self.resp = resp
        self.url = url
        self.headers = headers

    def get_birth_chat_info(self) -> Optional[BirthChartInfo]:
        try:
            if not self.resp:
                # should not reach here
                soup = BeautifulSoup(requests.get(self.url, headers=self.headers).text, 'html.parser')
            else:
                soup = BeautifulSoup(self.resp, 'html.parser')

            # get sign and house of each planet
            planet_to_sign: Dict[Planet, Sign] = defaultdict()
            planet_to_house: Dict[Planet, int] = defaultdict()
            for planet in ASTRO_SEEK_PLANET_DICT.keys():
                sign, house = self._get_planet_sign_and_house(soup, planet)
                planet_to_sign[planet] = Sign(sign)
                planet_to_house[planet] = int(house)
    
            # get aspects of the chart
            aspects: List[str] = self._get_aspects(soup)

            return BirthChartInfo(
                planet_to_sign=planet_to_sign, 
                planet_to_house=planet_to_house, 
                aspects=aspects
            )
        except:
            # TODO: handle error gracefully
            return None

    def _get_planet_sign_and_house(self, soup: BeautifulSoup, planet: Planet) -> Tuple[str, str]:
        tag = soup.find_all('a', attrs={'name': ASTRO_SEEK_PLANET_DICT[planet]})[0]
        div = tag.findNext('div')
        all_info = div.find_all('strong')
        basic_info: list = [t for t in all_info if f'{planet.value}  in' in t.text]
        sign: str = basic_info[0].contents[-1]
        house: str = re.search(r'\d+', basic_info[1].text).group()
        return sign, house


    def _get_aspects(self, soup: BeautifulSoup) -> List[str]:
        aspects: List[str] = list()
    
        tags = soup.find_all('a', attrs={'name': re.compile('aspekt_\d+')})
        for tag in tags:
            div = tag.findNext('div').find('div', class_='cl nulka')
            asp: str = re.search(r'\n\s(.*?)\s\(', div.contents[1].text).group(1)
            aspects.append(asp)

        return aspects
