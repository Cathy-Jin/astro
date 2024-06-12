from enum import Enum
from typing import List


# planet
class Planet(Enum):
    SUN = 'Sun', [5], '太阳'
    MOON = 'Moon', [4], '月亮'
    MERCURY = 'Mercury', [3, 6], '水星'
    VENUS = 'Venus', [2, 7], '金星'
    MARS = 'Mars', [1], '火星'
    JUPITER = 'Jupiter', [9], '木星'
    SATURN = 'Saturn', [10], '土星'
    URANUS = 'Uranus', [11], '天王星'
    NEPTUNE = 'Neptune', [12], '海王星'
    PLUTO = 'Pluto', [8], '冥王星'

    def __new__(cls, *args, **kargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, principles: List[int], val_cn: str):
        self._principles_ = principles
        self._val_cn_ = val_cn

    def __str__(self):
        return self.value

    @property
    def principles(self):
        return self._principles_
    
    @property
    def val_cn(self):
        return self._val_cn_


# sign
class Sign(Enum):
    ARIES = 'Aries', 1, '白羊座'
    TAURUS = 'Taurus', 2, '金牛座'
    GEMINI = 'Gemini', 3, '双子座'
    CANCER = 'Cancer', 4, '巨蟹座'
    LEO = 'Leo', 5, '狮子座'
    VIRGO = 'Virgo', 6, '处女座'
    LIBRA = 'Libra', 7, '天秤座'
    SCORPIO = 'Scorpio', 8, '天蝎座'
    SAGITTARIUS = 'Sagittarius', 9, '射手座'
    CAPRICORN = 'Capricorn', 10, '魔羯座'
    AQUARIUS = 'Aquarius', 11, '水瓶座'
    PISCES = 'Pisces', 12, '双鱼座'

    def __new__(cls, *args, **kargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj
    
    def __init__(self, _: str, principle: int, val_cn: str):
        self._principle_ = principle
        self._val_cn_ = val_cn

    @property
    def principle(self):
        return self._principle_
    
    @property
    def val_cn(self):
        return self._val_cn_
    

# aspect
class Aspect(Enum):
    CONJUNCTION = 'Conjunction', '合相', 0
    OPPOSITION = 'Opposition', '对分相', 180
    TRINE = 'Trine', '三分相', 120
    SQUARE = 'Square', '四分相', 90
    SEXITILE = 'Sexitile', '六分相', 60 
    QUINCUNX = 'Quincunx', '梅花相', 150
    SEMISEXTILE = 'Semi-Sextile', '十二分相', 30
    OCTILE = 'Octile', '八分相', 45
    TRIOCTILE = 'Tri-Octile', '补八分相', 135
    QUINTILE = 'Quintile', '五分相', 72
    BIQUINTILE = 'Bi-Quintile', '倍五分相', 144

    def __new__(cls, *args, **kargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj
    
    def __init__(self, _: str, val_cn: str, degree: int):
        self._val_cn_ = val_cn
        self._degree_ = degree
    
    @property
    def val_cn(self):
        return self._val_cn_

    @property
    def degree(self):
        return self._degree_


# principle
# inspired by： "The Inner Sky" by Steven Forrest
class Principle(Enum):
    ONE = '1', '生命力、自我意志、存在、身份认同、勇气、果断、战斗、压力'
    TWO = '2', '宁静、沉默、简单、掌控力、安全感、物质、感官、个人价值、自知之明'
    THREE = '3', '感知、好奇、智力、信息收集、信息分享、活力、开放的心态'
    FOUR = '4', '主观、感受、直觉、情绪、内心世界、防御、伪装、家、爱、灵魂'
    FIVE = '5', '表达、活在当下、个性、大方、信任、领导力、自我'
    SIX = '6', '完美主义、道德、原则、责任、服务、谦逊、诚实、自我评估'
    SEVEN = '7', '平衡、和谐、审美、选择、关系、承诺、业力'
    EIGHT = '8', '生存主义、本能、压抑机制、深刻、自省、危机处理、怀疑、隐秘'
    NINE = '9', '全局、世界观、意义、文化、信念、体验、开放、冒险精神、扩张、乐观'
    TEN = '10', '社会认同、自尊、整合、独处、耐心、自律、务实'
    ELEVEN = '11', '自由、真理、独立、个性、反叛、革新、执着'
    TWELVE = '12', '意识、想象、形而上、高我、慈悲、边界消融、逃避'

    def __new__(cls, *args, **kargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj
    
    def __init__(self, _: str, kw_cn: str):
        self._kw_cn_ = kw_cn
    
    @property
    def kw_cn(self):
        return self._kw_cn_


# birth chart source
ASTRO_SEEK: str = 'astro-seek'

# planet dictionary
ASTRO_SEEK_PLANET_DICT: dict = {
    Planet.SUN: 'slunce',
    Planet.MOON: 'luna',
    Planet.MERCURY: 'merkur',
    Planet.VENUS: 'venuse',
    Planet.MARS: 'mars',
    Planet.JUPITER: 'jupiter',
    Planet.SATURN: 'saturn',
    Planet.URANUS: 'uran',
    Planet.NEPTUNE: 'neptun',
    Planet.PLUTO: 'pluto'
}