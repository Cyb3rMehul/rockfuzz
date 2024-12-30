import argparse
import requests
import time
import csv
import urllib.parse

def fuzz_request(url, method, cookies, headers, body, payload):
    headers = headers or {}
    cookies = cookies or {}
    payload = urllib.parse.quote(payload)
    url = url.replace("FUZZ", payload)
    
    if body and "FUZZ" in body:
        body = body.replace("FUZZ", payload)

    if method == "POST":
        response = requests.post(url, data=body, headers=headers, cookies=cookies)
    else:
        response = requests.get(url, headers=headers, cookies=cookies)
    
    response_time = round(response.elapsed.total_seconds() * 1000)
    
    return response.status_code, len(response.text), response_time, payload

def main():
    parser = argparse.ArgumentParser(description="Simple Fuzzing Script")
    parser.add_argument("wordlist", help="Path to wordlist")
    parser.add_argument("rps", type=int, help="Requests per second")
    parser.add_argument("url", help="URL with or without FUZZ keyword")
    parser.add_argument("--method", choices=["GET", "POST"], default="GET", help="Request method (default GET)")
    parser.add_argument("--cookies", help="Cookies as key=value pair")
    parser.add_argument("--headers", help="Additional headers as key=value pair")
    parser.add_argument("--body", help="Body parameters with or without FUZZ keyword")
    
    args = parser.parse_args()

    cookies = {}
    if args.cookies:
        for cookie in args.cookies.split(";"):
            key, value = cookie.split("=")
            cookies[key.strip()] = value.strip()

    headers = {}
    if args.headers:
        for header in args.headers.split(";"):
            key, value = header.split(":")
            headers[key.strip()] = value.strip()

    with open(args.wordlist, "r") as f:
        payloads = f.readlines()
    
    print(f"{'Status Code':<15}{'Length':<15}{'Response Time':<20}{'Payload'}")
    output = []
    for payload in payloads:
        payload = payload.strip()
        status_code, length, response_time, fuzzed_payload = fuzz_request(
            args.url, args.method, cookies, headers, args.body, payload
        )
        print(f"{status_code:<15}{length:<15}{response_time:<20}{payload}")
        output.append([status_code, length, response_time, payload])
        time.sleep(1 / args.rps)
    
    with open("output.txt", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Status Code", "Length", "Response Time", "Payload"])
        writer.writerows(output)

if __name__ == "__main__":
    main()
