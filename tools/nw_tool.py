"""
https://playwright.dev/python/docs/api/class-response#response-json

https://sqqihao.github.io/trillworks.html

Charly Molero - 2022

Ejercicios:
"https://www.sofascore.com/football/livescore"
"https://www.aysa.com.ar/Que-Hacemos/estaciones-meteorologicas/datos#"
"""
import sys
import json
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import Error as PwhtTypeError

URL_TO_ANALYZE = str(sys.argv[1])
# URL_TO_ANALYZE = "https://www.aysa.com.ar/Que-Hacemos/estaciones-meteorologicas/datos#" # sacar rapidamente
# URL_TO_ANALYZE = "https://www.ambito.com/contenidos/dolar.html" # pasar a df
#URL_TO_ANALYZE = "https://www.cinepolis.com.ar/cines/cinepolis-recoleta"  # jugar con parametros de query
# URL_TO_ANALYZE = "https://www.sofascore.com/football/livescore" # armar df
# URL_TO_ANALYZE = "https://www.sofascore.com/football/all" # considerar reload
# URL_TO_ANALYZE = "https://www.bloomberg.com/quote/BDIY:IND" # buscar mas rapidamente


def return_json_response(response, errors_counters: dict, json_responses: list, json_request_urls: list) -> None:
    try:
        formated_response = {"url": response.url, "json_response": response.json()}
        json_responses.append(formated_response)
        json_request_urls.append(response.url)

    except json.JSONDecodeError:
        errors_counters["not_a_json"] += 1

    except UnicodeDecodeError:
        errors_counters["unicode_error"] += 1

    except PwhtTypeError:
        errors_counters["pwht_type_error"] += 1


def run(pwht) -> tuple:
    errors_counters = {"not_a_json": 0, "unicode_error": 0, "pwht_type_error": 0, }
    json_responses = []
    json_request_urls = []

    chromium = pwht.chromium
    browser = chromium.launch(headless=False, slow_mo=8_000, timeout=240_000)
    page = browser.new_page()
    page.on("response",
            lambda response: return_json_response(response=response, errors_counters=errors_counters,
                                                  json_responses=json_responses, json_request_urls=json_request_urls))
    page.goto(URL_TO_ANALYZE, timeout=240_000)
    browser.close()
    return json_responses, json_request_urls, errors_counters


with sync_playwright() as pwht:
    json_responses, json_request_urls, errors_counters = run(pwht)

    with open('results.json', 'w') as f:
        json.dump(json_responses, f)

    with open('urls.txt', 'w') as f:
        f.write('\n'.join(json_request_urls))

print(f"Possible Hidden API's = {len(json_responses)}")
print("\nOther responses:")
for error, count in errors_counters.items():
    print(f"\t{error} = {count}")
print("\n")