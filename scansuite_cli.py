import requests
import os
import re

def fetch_session_and_csrf(url):
    login_path = "/log_in"
    login_url = url + login_path

    # Step 1: Make the first request
    response1 = requests.get(login_url, verify=False)

    # Extract the "session" cookie from the response headers
    session_cookie1 = response1.cookies.get("session")
    if not session_cookie1:
        raise ValueError("Session cookie not found in the first response.")

    # Step 2: Make the second request with the session cookie
    cookies = {"session": session_cookie1}
    response2 = requests.get(login_url, cookies=cookies, verify=False)

    # Extract the new "session" cookie from the response headers
    session_cookie2 = response2.cookies.get("session")
    if not session_cookie2:
        raise ValueError("Session cookie not found in the second response.")

    # Extract the CSRF token from the response body
    csrf_token_match = re.search(
        r'<input[^>]*id="csrf_token"[^>]*value="([^"]+)"', response2.text
    )
    if not csrf_token_match:
        raise ValueError("CSRF token not found in the response body.")

    csrf_token = csrf_token_match.group(1)

    return session_cookie2, csrf_token

def login(url, username, password):

    session_cookie, csrf_token = fetch_session_and_csrf(url)

    login_path = "/log_in"
    login_url = url + login_path

    # Prepare POST data
    data = {
        "csrf_token": csrf_token,
        "username": username,
        "password": password,
        "login": ""
    }

    # Prepare cookies
    cookies = {"session": session_cookie}

    # Make the POST request
    response = requests.post(login_url, data=data, cookies=cookies, verify=False, allow_redirects=False)
    if response.status_code == 302:
        session_cookie3 = response.cookies.get("session")
        if session_cookie3:
            return session_cookie3
        else:
            print("Session cookie not found in the 302 response")
            print(response.headers)
    else:
        print(f"Unexpected response status code: {response.status_code}")
        print(response.headers)

    return response

def create_product(url, session_cookie, product_name):
    product_path = "/product"
    product_url = url + product_path

    # Prepare POST data
    data = {"prodname": product_name}

    # Prepare cookies
    cookies = {"session": session_cookie}

    # Make the POST request
    response = requests.post(product_url, data=data, cookies=cookies, verify=False)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Product request failed with status code {response.status_code}.")
        print(response.headers)
        print(response.text)
        return False

def static_scan_url(url, session_cookie, giturl, lang, engid, scanners_list):
    static_path = "/static"
    static_url = url + static_path

    # Prepare multipart form-data
    params = {
        "file": "undefined",
        "lang": lang,
        "engid": engid,
        "giturl": giturl,
        "frequency": "Once",
        "branch_name": "main",
        "scan_id": "New"
    }
    data = {**params, **scanners_list}

    # Prepare cookies
    cookies = {"session": session_cookie}

    # Make the POST request
    response = requests.post(static_url, data=data, cookies=cookies, verify=False)

    if response.status_code == 200:
        print(f"Submitted {giturl}: {response.status_code} - {response.text}")
        return response.text
    else:
        print(f"Static request failed with status code {response.status_code}.")
        print("Headers:")
        print(response.headers)
        print("Body:")
        print(response.text)

def extract_file_name(file_path):
    # Linux path
    if "/" in file_path:
        file_name = file_path.split("/")[-1]
    # Windows path
    elif "\\" in file_path:
        file_name = file_path.split("\\")[-1]
    # File is in the current folder
    else:
        file_name = file_path
    return file_name

def static_scan_file(url, session_cookie, lang, engid, file_path, scanners_list):
    file_name = extract_file_name(file_path)

    static_path = "/static"
    static_url = url + static_path

    cookies = {"session": session_cookie}

    # Form data fields
    params = {
        "lang": lang,
        "engid": engid,
        "giturl": "",
        "frequency": "Once",
        "branch_name": "main",
        "scan_id": "New",
    }
    data = {**params, **scanners_list}

    try:
        # Read the .zip file as binary data
        with open(file_path, "rb") as file:
            files = {"file": (file_name, file, "application/x-zip-compressed")}

            # Send the POST request with form data
            response = requests.post(static_url, files=files, data=data, cookies=cookies, verify=False)

            if response.status_code == 200:
                print(f"Uploaded {file_name}: {response.status_code} - {response.text}")
                return response.text
            else:
                print(f"Static request failed with status code {response.status_code}.")
                print(response.headers)
                return False

    except Exception as e:
        print(f"Failed to upload {file_name}: {e}")

def dynamic_scan(url, session_cookie, targets, engid, auth_cookie, auth_header, web_scanners):
    path = "/dynamic"
    url = url + path

    # Prepare POST data
    params = {
        "scan_id": "New",
        "targets": targets,
        "engid": engid,
        "cookie": auth_cookie,
        "frequency": "Once",
        "scan_date": "",
        "scan_time": "",
        "run_or_save": "Run now",
        "header": auth_header
    }

    data = {**params, **web_scanners}

    # Prepare cookies
    cookies = {"session": session_cookie}

    # Make the POST request
    response = requests.post(url, json=data, cookies=cookies, verify=False)

    if response.status_code == 200:
        print("Dynamic scan started.")
        return response.text
    else:
        print(f"Dynamic scan request failed with status code {response.status_code}.")
        print(response.headers)
        #print(response.text)
        return False

def infra_scan(url, session_cookie, targets, engid, ping, ports, scan_type, scanners):
    path = "/infrastructure"
    url = url + path

    # Prepare POST data
    params = {
        "scan_id": "New",
        "targets": targets,
        "engid": engid,
        "frequency": "Once",
        "scan_date": "",
        "scan_time": "",
        "run_or_save": "Run now",
        "ping": ping,
        "ports": ports,
        "scan_type": scan_type
    }

    if scanners:
        data = {**params, **scanners}
    else:
        data = params

    # Prepare cookies
    cookies = {"session": session_cookie}

    # Make the POST request
    response = requests.post(url, json=data, cookies=cookies, verify=False)

    if response.status_code == 200:
        print("Infrastructure scan started.")
        return response.text
    else:
        print(f"Infrastructure scan request failed with status code {response.status_code}.")
        print(response.headers)
        #print(response.text)
        return False
    
def get_scan_status(url, session_cookie, scanid):
    login_path = "/history"
    login_url = url + login_path
    params = {"actualId": scanid}

    cookies = {"session": session_cookie}

    response = requests.get(login_url, cookies=cookies, params=params, verify=False)

    if response.status_code == 200:
        return response.text
    
    else:
        print(f"Getting scan status failed with status code {response.status_code}.")
        print(response.headers)
        #print(response.text)
        return False