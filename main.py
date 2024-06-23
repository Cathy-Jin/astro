from typing import List, Tuple
from life_theme_calculator import calculate_life_themes, Energy
from pyscript import document, display, fetch, HTML
from pyscript.ffi import create_proxy


async def get_life_themes_with_basic_info(event):
    # clear the output
    display('', target='output', append=False)

    year: str = document.querySelector('#year').value
    month: str = document.querySelector('#month').value
    day: str = document.querySelector('#day').value
    hour: str = document.querySelector('#hour').value
    minute: str = document.querySelector('#minute').value
    city: str = document.querySelector("#city").value
    state: str = document.querySelector("#state").value
    country: str = document.querySelector("#country").value
    lat_d, lat_m, lon_d, lon_m = await _get_coordinates(city, state, country)
    if not lat_d:
        display(_render_error('无法找到地点坐标，请重试'), target='output', append=False)
        return
    
    astro_seek_url: str = f'''
        https://horoscopes.astro-seek.com/calculate-birth-chart-horoscope-online/?input_natal=1&send_calculation=1
        &narozeni_den={day}&narozeni_mesic={month}&narozeni_rok={year}&narozeni_hodina={hour}&narozeni_minuta={minute}&narozeni_sekunda=00
        &narozeni_podstat_kratky_hidden=&narozeni_sirka_stupne={lat_d}&narozeni_sirka_minuty={lat_m}&narozeni_sirka_smer=0
        &narozeni_delka_stupne={lon_d}&narozeni_delka_minuty={lon_m}&narozeni_delka_smer=0
        &narozeni_timezone_form=auto&narozeni_timezone_dst_form=auto&house_system=placidus&hid_fortune=1&hid_fortune_check=on&hid_vertex=1&hid_vertex_check=on
        &hid_chiron=1&hid_chiron_check=on&hid_lilith=1&hid_lilith_check=on&hid_uzel=1&hid_uzel_check=on
        &tolerance=1&aya=&tolerance_paral=1.2&zmena_nastaveni=1&aktivni_tab=&hide_aspects=0&dominanta_metoda=1&dominanta_rulership=1#tabs_redraw
    '''
    birth_chart_info: str = await _fetch_astro_seek_page(astro_seek_url)
    if birth_chart_info.startswith('错误'):
        display(_render_error(birth_chart_info), target='output', append=False)
        return
    
    energies: List[Energy] = calculate_life_themes(resp=birth_chart_info, url=astro_seek_url)
    display(_render_energies(energies, astro_seek_url), target='output', append=False)
    
    
async def get_life_themes_with_url(event):
    # clear the output
    display('', target='output', append=False)

    url: str = document.querySelector("#astro_seek_url").value
    birth_chart_info: str = await _fetch_astro_seek_page(url)
    if birth_chart_info.startswith('错误'):
        display(_render_error(birth_chart_info), target='output', append=False)
        return
    
    energies: List[Energy] = calculate_life_themes(resp=birth_chart_info, url=url)
    display(_render_energies(energies, url), target='output', append=False)


async def _get_coordinates(city: str, state: str, country: str) -> Tuple[int, int, int, int]:
    nominatim_url: str = f'https://nominatim.openstreetmap.org/search?city={city}&state={state}&country={country}&format=json&limit=1';
    response = await fetch(nominatim_url)
    if response.status == 200:
        data = await response.json()
        if len(data) > 0:
            lat: float = float(data[0].get('lat'))
            lat_d: int = int(lat)
            lat_m: int = int((lat - lat_d) * 60)
            lon: float = float(data[0].get('lon'))
            lon_d: int = int(lon)
            lon_m: int = int((lon - lon_d) * 60)
            return lat_d, lat_m, lon_d, lon_m
        else:
            return None, None, None, None
    else:
        return None, None, None, None


async def _fetch_astro_seek_page(url: str = None) -> str:
    # payload = {
    #     'link': url
    # }
    # # Define the fetch options
    # options = {
    #     'method': 'POST',
    #     'headers': {
    #         'Content-Type': 'application/json'
    #     },
    #     'body': json.dumps(payload)
    # } 
    response = await fetch(url)  # https://astroseek-api.onrender.com/astroseek-bith-chart-calculator/v2  # https://astroseek-api.onrender.com/astroseek-calculator
    if response.status == 200:
        data = await response.text()
        return data
    else:
        return f'错误：无法从astro-seek.com获取信息 - {response.status}'


def _render_energies(energies: List[Energy], url: str) -> HTML:
    output: str = '<h2>计算结果</h2>'
    if not energies:
        output += '<hr><p>似乎没有找到</p>'
    else:
        for e in energies:
            output += f'''
            <hr>
            <h3>主题：{e.name_cn}</h3>
            <p><b>关键词（仅供参考）</b>：{_render_keywords(e)}</p>
            <p><b>星盘中出现次数</b>： {len(e.patterns_cn)}</p>
            <p><b>星盘中表现形式</b>：<ul><li>{'</li><li>'.join(e.patterns_cn)}</ul></p>
            '''
    output += f'''
    <hr>
    <p>更多关于你的星盘信息: <a href="{url}" target="_blank">Astro-Seek</a></p>
    <p>联系我：cathyking716@gmail.com</p>
    '''
    return HTML(output)


def _render_keywords(energy: Energy) -> str:
    if len(energy.principles) == 1:
        return energy.principles[0].kw_cn
    else:
        s: str = '<ul>'
        for p in energy.principles:
            s += f'<li>{p.value}的能量包含：{p.kw_cn}</li>'
        return s + '</ul>'
    
def _render_error(err: str) -> HTML:
    return HTML(f'<h2>计算结果</h2><hr><p>{err}</p>')


# Attach the event handler to the button using create_proxy
def main():
    button1 = document.querySelector('#fetch_button_1')
    button2 = document.querySelector("#fetch_button_2")
    proxy1 = create_proxy(get_life_themes_with_basic_info)
    proxy2 = create_proxy(get_life_themes_with_url)
    button1.addEventListener("click", proxy1)
    button2.addEventListener("click", proxy2)

main()