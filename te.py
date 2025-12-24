from telegram.ext import Application
from telegram.request import HTTPXRequest
import socks
import socket

TOKEN = "6542403472:AAHAK-htx8g7WGNQw3zvmKwboPnewB9mRtQ"

def setup_mtproxy():
    socks.set_default_proxy(
        socks.SOCKS5,
        "https.younum-c.co.uk",
        443,
        username="",
        password="dd638becf0fe989caa21b10797ad4d1c38"
    )

    socket.socket = socket.socksocket

    # connection test
    try:
        test_socket = socket.create_connection(("api.telegram.org", 443), timeout=5)
        test_socket.close()
        print("MTProto is activate")
    except Exception as e:
        print(f"connection failed : {e}")


setup_mtproxy()
application = Application.builder().token("AAHAK-htx8g7WGNQw3zvmKwboPnewB9mRtQ").build()
