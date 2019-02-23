try:
    import httplib
except:
    import http.client as httplib

def check_network():
    conn = httplib.HTTPConnection("google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False