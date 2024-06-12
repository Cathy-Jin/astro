from birth_chart_craweler import AstroSeek, BirthChartInfo
from constants import Aspect, Planet, Sign, Principle
from typing import Dict, List
from collections import defaultdict 
from dataclasses import dataclass


@dataclass(frozen=True)
class Energy:
    name_cn: str
    principles: List[Principle]
    patterns_cn: List[str]


def calculate_life_themes(resp: str, url: str=None, headers: dict=None) -> List[Energy]:
    # Get planet, house, and aspect info from the source url
    birth_chart_info = AstroSeek(resp, url, headers).get_birth_chat_info()
    if not birth_chart_info:
        return None
    
    # Translate patterns into interchanges
    interchange_to_patterns: Dict[str, List[str]] = _get_interchanges(birth_chart_info)
    return _get_energies(interchange_to_patterns)


def _get_interchanges(birth_chart_info: BirthChartInfo) -> Dict[str, List[str]]:
    i_to_p: Dict[str, List[str]] = defaultdict(lambda: list())

    # process planets & signs
    # rule(s):
    # planet principle ~ sign principle
    for planet, sign in birth_chart_info.planet_to_sign.items():
        for p_principle in planet.principles:
            i_to_p[_get_interchange(sign.principle, p_principle)].append(_get_planet_in_sign_cn(planet, sign))

    # process planets & houses
    # rule(s):
    # planet principle ~ house principle
    for planet, house in birth_chart_info.planet_to_house.items():
        for p_principle in planet.principles:
            i_to_p[_get_interchange(house, p_principle)].append(_get_planet_in_house_cn(planet, house))
    
    # process aspects
    # rule(s): 
    # planet A principle ~ planet B principle
    # planet A house principle ~ planet B house principle
    # planet A sign principle ~ planet B sign principle
    for asp in birth_chart_info.aspects:
        try:
            # get planet A and B
            p_a, aspect, p_b = tuple(asp.split())
            planet_a: Planet = Planet(p_a)
            planet_b: Planet = Planet(p_b)
            aspt: Aspect = Aspect(aspect)
            sign_a: Sign = birth_chart_info.planet_to_sign[planet_a]
            sign_b: Sign = birth_chart_info.planet_to_sign[planet_b]
            house_a: int = birth_chart_info.planet_to_house[planet_a]
            house_b: int = birth_chart_info.planet_to_house[planet_b]

            for a_principle in planet_a.principles:
                for b_principle in planet_b.principles:
                    i_to_p[_get_interchange(a_principle, b_principle)].append(_get_aspect_cn(planet_a, aspt, planet_b))

            i_to_p[_get_interchange(house_a, house_b)].append(_get_aspect_cn(planet_a, aspt, planet_b) + '（' + _get_planet_in_house_cn(planet_a, house_a) + '，' + _get_planet_in_house_cn(planet_b, house_b) + '）')

            i_to_p[_get_interchange(sign_a.principle, sign_b.principle)].append(_get_aspect_cn(planet_a, aspt, planet_b) + '（' + _get_planet_in_sign_cn(planet_a, sign_a) + '，' + _get_planet_in_sign_cn(planet_b, sign_b) + '）')
        except ValueError:
            # Aspect about non-planet objects. Skip for now.
            continue
    
    return i_to_p


def _get_interchange(p1: int, p2: int) -> str:
    if p1 == p2:
        return str(p1)
    else:
        return f'{min(p1, p2)}-{max(p1, p2)}'


def _get_planet_in_sign_cn(p: Planet, s: Sign) -> str:
    return f'{p.val_cn}在{s.val_cn}'


def _get_planet_in_house_cn(p: Planet, h: str) -> str:
    return f'{p.val_cn}落在第{h}宫'


def _get_aspect_cn(a: Planet, aspt: Aspect, b: Planet) -> str:
    return f'{a.val_cn}与{b.val_cn}呈{aspt.val_cn}（{aspt.degree}度）'


def _get_energies(i_to_p: Dict[str, List[str]]) -> List[Energy]:
    energies: List[Energy] = list()
    major_i_to_p: Dict[str, List[str]] = {k: v for (k, v) in i_to_p.items() if len(v) >= 3}
    sorted_keys: List[str] = sorted(major_i_to_p, key=lambda k: len(major_i_to_p[k]), reverse=True)
    for i in sorted_keys:
        if '-' in i:
            [p1, p2] = i.split('-')
            energy = Energy(
                name_cn = f'整合{p1}与{p2}的能量',
                principles = [Principle(p1), Principle(p2)],
                patterns_cn=major_i_to_p[i]
            )
        else:
            energy = Energy(
                name_cn = f'发挥{i}的能量',
                principles = [Principle(i)],
                patterns_cn=major_i_to_p[i]
            )
        energies.append(energy)
    return energies
