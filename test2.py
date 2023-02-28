import http
import socket
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlsplit
import urllib3
import urllib.error
from bs4.builder import XMLParsedAsHTMLWarning
import warnings

good_host = []

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

with open("input_urls.txt") as f:
    urls = f.read().splitlines()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/72.0.3626.119 Safari/537.36"}


def get_status(url):
    r = requests.get(url)
    print(url, r.status_code)

    try:
        # Get Url
        get = requests.get(url, verify=False, timeout=10, headers=headers)
        # if the request succeeds
        if r.status_code == 200:
            print(f"{url}: is reachable,  {get.status_code}")
            good_host.append(url)
        else:
            print(f"{url}: Failed. {get.status_code}")

    # Exception
    except requests.exceptions.RequestException as e:
        # print URL with Errs
        print(f"{url}: Failed.")

    except requests.exceptions.SSLError as e:
        print(f"{url}: Failed.")

    except requests.exceptions.RequestException as e:
        print(f"{url}: Failed.")

    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        print(f"{url}: Failed.")

    except urllib.error.HTTPError as e:
        print(f"{url}: Failed.")

    except urllib.error.URLError as e:
        print(f"{url}: Failed.")

    except socket.error as e:
        print(f"{url}: Failed.")

    except http.client.IncompleteRead as e:
        print(f"{url}: Failed.")

    return r.status_code


if __name__ == "__main__":
    pool = ThreadPool(200)  # Make the Pool of workers
    results = pool.map(get_status, urls)  # Open the urls in their own threads
    pool.close()  # close the pool and wait for the work to finish
    pool.join()

    for i in good_host:
        print(i)
