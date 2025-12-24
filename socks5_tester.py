import socket
import socks
import time
import concurrent.futures
from urllib.request import Request, urlopen
from urllib.error import URLError

def test_socks5_proxy(proxy_host, proxy_port, test_url="https://api.telegram.org", timeout=5):

    #saving socket setting
    original_socket = socket.socket

    #socks5 proxy setting
    socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
    socket.socket = socks.socksocket

    result = {
        "proxy": f"{proxy_host}:{proxy_port}",
        "status": "unknown",
        "delay_ms": None,
        "external_ip": None,
        "error": None
    }

    try:
        start_time = time.time()

        req = Request(test_url)
        req.add_header("User-Agent", "Mozilla/5.0 (Test Proxy)")

        # request a connection with proxy
        response = urlopen(req, timeout=timeout)
        end_time = time.time()

        delay_ms = round((end_time - start_time) * 1000, 2)

        #reading response
        content = response.read().decode("utf-8")

        if "origin" in content:
            import json
            data = json.loads(content)
            external_ip = data.get("origin", "unknown")
        else:
            external_ip = "not extract"

        result.update({
            "status": "active",
            "delay_ms": delay_ms,
            "external_ip": external_ip
        })

    except socks.ProxyConnectionError as e:
        result.update({
            "status": "Error",
            "error": f"failure of proxy connection: {str(e)}"
        })
    except socket.timeout:
        result.update({
            "status": "Error",
            "error": f"the connection is timeout {timeout}"
        })
    except URLError as e:
        result.update({
            "status": "Error",
            "error": f"network error: {str(e.reason)}"
        })
    except Exception as e:
        result.update({
            "status": "Error",
            "error": f"unknown error: {str(e)}"
        })
    finally:
        # reset the socket setting to default
        socket.socket = original_socket
        socks.set_default_proxy()

    return result

def proxy_list(proxy_list, max_workers=10):
    ''' proxy testing with a list using the parallel testing'''
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {
            executor.submit(test_socks5_proxy, host, port): (host, port)
            for host, port in proxy_list
        }
        for future in concurrent.futures.as_completed(future_to_proxy):
            host, port = future_to_proxy[future]
            try:
                result = future.result(timeout=5)
                results.append(result)
            except Exception as e:
                results.append({
                    "proxy": f"{host}:{port}",
                    "status": "error",
                    "delay_ms": None,
                    "external_ip": None,
                    "error": f"error in testing {str(e)}"
                })
    return results

def convert_text_list(txt_file):
    lst = []
    with open(txt_file, "r") as f:
        lines_read = f.readlines()
        for item in lines_read:
            x = item.rstrip('\n')
            y = x.rsplit(sep=":", maxsplit=1)
            y[0] = str(y[0])
            y[1] = int(y[1])
            lst.append(y)
    return lst

def main():
    proxies_to_test = convert_text_list("proxy_second.txt")
    print(f"testing a {len(proxies_to_test)} proxies")
    print("=" * 60)

    results = proxy_list(proxies_to_test)

    # showing the result
    successful = 0
    for result in results:
        if result["status"] == "active":
            print(f"proxy {result["proxy"]} successful")
            print(f"delay: {result['delay_ms']}ms | external_ip: {result['external_ip']}")
            successful += 1
        else:
            print(f"proxy {result['proxy']} failed")
            print(f" error: {result['error']}")
        print("-" * 40)
    print(f"\n summey: {successful} from {len(proxies_to_test)} proxies  is active")

    if successful > 0:
        working_proxies = [r for r in results if r["status"] == "active"]
        sorted_proxies = sorted(working_proxies, key=lambda r: r["delay_ms"])

        print("the best proxies due to the delay ms")
        for i, proxy in enumerate(sorted_proxies[:3], 1):
            print(f"{i}. {proxy['proxy']} - {proxy['delay_ms']}ms")




if __name__ == "__main__":
    # lst = convert_text_list("proxy_data.txt")
    main()



# =======================================================================================
# This is the second code for test
# =======================================================================================

#
# import requests
#
# def test_socks5_proxy(proxy):
#     proxy = ""
#
#
#     try:
#         response = requests.get("https://api.telegram.org", proxies=proxies, timeout=5)
#         print("✅ Proxy is working")
#         print("Status code:", response.status_code)
#     except Exception as e:
#         print("❌ Proxy failed")
#         print("Error:", e)
#
#
# if __name__ == "__main__":
#     # نمونه تست
#     with open("proxy_second.txt", "r") as f:
#         liness = f.readlines()
#         for item in liness:
#             test_socks5_proxy(item.strip())

