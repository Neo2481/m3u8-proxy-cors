from urllib.parse import urlparse, parse_qs, quote, unquote
import requests
import json


class Requester:
    def __init__(self, url):
        parsed_url = urlparse(url)
        self.url = url
        self.schema = parsed_url.scheme
        self.domain = parsed_url.netloc
        self.query_params = self.query(parsed_url)
        self.host = self.get_host(parsed_url)
        self.path = parsed_url.path
        params = self.query_params.copy()

        # Remove unnecessary params
        for key in ["url", "type", "headers", "method", "json", "params"]:
            params.pop(key, None)

        self.remaining_params = params
        self.req_url = f"{self.host}{self.path}?{self.query_string(params)}"
        self.base_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Connection": "keep-alive",
            "Referer": None,
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Linux",
        }

    def get(self, data=None, headers=None, method="get", json_data=None, additional_params=None, cookies=None):
        headers = self.headers(headers)

        # Ensure additional_params is a valid dictionary
        try:
            additional_params = json.loads(additional_params)
        except (json.JSONDecodeError, TypeError):
            additional_params = {}

        additional_params = additional_params if isinstance(additional_params, dict) else {}

        cookies = cookies or {}
        json_data = json_data or {}

        if additional_params:
            self.req_url += "&" if "=" in self.req_url else ""
            self.req_url += self.query_string(additional_params)

        # Properly decode URL instead of manual replacements
        self.req_url = unquote(self.req_url)

        try:
            if method.lower() == "post":
                response = requests.post(
                    self.req_url, headers=headers, data=data, timeout=10, json=json_data, allow_redirects=False, cookies=cookies
                )
            else:
                response = requests.get(
                    self.req_url, headers=headers, data=data, timeout=10, json=json_data, allow_redirects=False, cookies=cookies
                )
        except requests.RequestException as e:
            return [None, {}, 500, {}]  # Return a server error code if the request fails

        return [response.content, response.headers, response.status_code, response.cookies]

    def headers(self, headers):
        header = self.base_headers.copy()
        header.update(headers or {})
        header.pop("Host", None)
        header.pop("Cookie", None)
        return header

    def safe(self, url):
        parsed_url = urlparse(url)
        queries = self.query(parsed_url)
        host = self.get_host(parsed_url)
        path = parsed_url.path
        return f"{host}{path}{'?' + self.query_string(queries) if queries else ''}"

    @staticmethod
    def safe_sub(url):
        return quote(url)

    @staticmethod
    def query(parsed_url):
        return {k: unquote(str(v[0]), 'utf-8') for k, v in parse_qs(parsed_url.query).items()}

    @staticmethod
    def query_string(queries):
        return "&".join(f"{query}={quote(queries[query])}" for query in queries)

    @staticmethod
    def get_host(parsed_url):
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    def __str__(self):
        return f"Domain: {self.domain}\nScheme: {self.schema}\nPath: {self.path}\nQuery Parameters: {self.query_params}"


if __name__ == "__main__":
    test_url = "https://example.com/test.mp4?token=3892&idea=2(]/s[e3r2&url=https%3A//example.com/test.mp4%3Ftoken%3D3892%26idea%3D2%28%5D/s%5Be3r2"
    requester = Requester(test_url)
    print(requester)
