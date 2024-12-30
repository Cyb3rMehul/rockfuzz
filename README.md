# rockfuzz

This script is designed for fuzz testing web applications by sending various payloads to specified URLs. It allows you to fuzz parameters in the URL and body.

## Example Usage

1. **Basic GET Request Fuzzing**

   To perform fuzzing with a wordlist using the default `GET` method, run the following command:

   ```bash
   python fuzz.py /path/to/wordlist.txt 10 http://example.com/FUZZ
   ```

   This will send requests to `http://example.com/FUZZ` and replace the `FUZZ` keyword with each entry from the wordlist. The script will send 10 requests per second.

2. **POST Request Fuzzing with Body Parameters**

   To fuzz a `POST` request with body parameters, use the following:

   ```bash
   python fuzz.py /path/to/wordlist.txt 5 http://example.com/api --method POST --body "username=FUZZ&password=test" --cookies "sessionid=12345" --headers "Content-Type: application/x-www-form-urlencoded"
   ```

   This will replace `FUZZ` in the body (`username=FUZZ&password=test`) with each entry from the wordlist and send `POST` requests to the API. The script will also include a cookie and header for each request.

3. **Custom Headers and Cookies**

   You can specify custom cookies and headers by separating key-value pairs with semicolons. Here's an example with custom headers and cookies:

   ```bash
   python fuzz.py /path/to/wordlist.txt 2 http://example.com/FUZZ --headers "User-Agent: Mozilla/5.0;X-Custom-Header: value" --cookies "sessionid=abc123;userid=456"
   ```

   This sends fuzzed payloads with custom headers and cookies while controlling the request rate.

## Arguments

- `wordlist`: Path to the wordlist file containing payloads.
- `rps`: Number of requests per second (Rate limiting).
- `url`: URL to fuzz. The string "FUZZ" in the URL will be replaced with each payload from the wordlist.
- `--method`: HTTP method, either `GET` or `POST`. Default is `GET`.
- `--cookies`: Optional cookies to send with the request, specified as `key=value` pairs separated by semicolons.
- `--headers`: Optional headers to include in the request, specified as `key:value` pairs separated by semicolons.
- `--body`: Optional body content for `POST` requests, which can contain the `FUZZ` keyword to be replaced with payloads.

## Output

The script will display the following details for each request:

- Status Code
- Response Length
- Response Time (in milliseconds)
- Payload

It will also write the results in CSV format to a file named `output.csv` with the similar columns.

## Requirements

- Python 3.x
- `requests` library

To install the required libraries:

```bash
pip install requests
```
