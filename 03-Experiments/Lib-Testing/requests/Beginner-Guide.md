# The `requests` Library - Complete Beginner Guide

## Part 0: First Principles - Why This Library Exists

Every interaction with the web boils down to two things:

1. **Request** - your program asks a server for something ("send me this data", "save this data", "delete this thing")
2. **Response** - the server replies with a status and (usually) some content

A browser does this visually. `requests` lets Python do it programmatically - no browser needed. This is the foundation of talking to any web API: weather services, payment systems, social media platforms, your own backend, anything.

**Install it first:**

```bash
pip install requests
```

---

## Part 1: The Outline (Memorize This Map First)

| # | Concept | What it does |
|---|---------|---------------|
| 1 | HTTP verbs | GET, POST, PUT, PATCH, DELETE - the "intentions" |
| 2 | Query parameters | Data sent in the URL (`?key=value`) |
| 3 | Request body | Data sent inside the request (JSON, form data, files) |
| 4 | Headers | Metadata about the request (auth tokens, content type) |
| 5 | The Response object | Status code, body, headers of what came back |
| 6 | Authentication | Proving who you are to the server |
| 7 | Timeouts & exceptions | Handling things going wrong |
| 8 | Sessions | Reusing connections/settings across many requests |
| 9 | Advanced: streaming, redirects, SSL, proxies | Edge cases you'll meet eventually |

Everything below fills in this map, in order. Don't skip to Part 9 before Part 1 makes sense.

---

## Part 2: The Four Core Verbs

Think of HTTP verbs as **intent**, not just syntax:

| Verb | Real-world analogy |
|------|---------------------|
| GET | Reading a menu |
| POST | Placing a new order |
| PUT | Replacing your entire order |
| PATCH | Changing one item in your order |
| DELETE | Cancelling your order |

### GET - retrieve data

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)  # 200
print(response.text[:200])  # first 200 characters of the raw response
```

**Notes:**
- `requests.get()` returns a `Response` object - it does NOT print anything or raise errors automatically.
- Nothing is sent to the server except the URL itself (plus default headers).

### POST - create/send new data

```python
response = requests.post(
    "https://httpbin.org/post", json={"username": "yoghesh", "role": "developer"}
)
print(response.json())
```

**Notes:**
- `httpbin.org` is a free testing service - it echoes back whatever you send, which is perfect for learning (more on this in Part 8).
- `json=` auto-converts your dict to a JSON string AND sets the `Content-Type: application/json` header for you.

### PUT - replace existing data entirely

```python
response = requests.put(
    "https://httpbin.org/put", json={"username": "yoghesh", "role": "senior developer"}
)
```

**Notes:**
- PUT implies you're sending the *complete* replacement object, not just the changed field.

### PATCH - update part of existing data

```python
response = requests.patch(
    "https://httpbin.org/patch", json={"role": "senior developer"}
)
```

**Notes:**
- PATCH implies partial update - only send the fields that changed.
- Whether an API actually respects PUT vs PATCH semantics depends on how it's built - `requests` just sends the verb, it doesn't enforce meaning.

### DELETE - remove data

```python
response = requests.delete("https://httpbin.org/delete")
```

**Notes:**
- Many DELETE endpoints don't need a body at all - just the URL.

---

## Part 3: Sending Data - Three Ways

### 3.1 Query parameters (`params`)

Used for GET requests, filters, searches - anything that would appear after `?` in a URL.

```python
response = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "python", "sort": "stars", "order": "desc"},
)
print(response.url)
# https://api.github.com/search/repositories?q=python&sort=stars&order=desc
```

**Why use `params=` instead of building the string yourself:**
- Automatically handles URL-encoding (spaces become `%20`, special characters get escaped)
- Cleaner and less error-prone than string concatenation

### 3.2 Form data (`data`)

Used when an API expects traditional HTML-form-style data (`application/x-www-form-urlencoded`).

```python
response = requests.post(
    "https://httpbin.org/post", data={"username": "yoghesh", "password": "secret123"}
)
```

**Note:** This is different from `json=`. Check the API docs to see which one it expects - sending the wrong type is a common beginner bug.

### 3.3 JSON body (`json`)

Used for modern REST APIs - the most common case today.

```python
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "Yoghesh", "skills": ["python", "electron"]},
)
```

**Rule of thumb:** if the API docs show example requests with curly braces `{ }`, use `json=`. If they mention "form-encoded", use `data=`.

### 3.4 File uploads (`files`)

```python
with open("resume.pdf", "rb") as f:
    response = requests.post("https://httpbin.org/post", files={"file": f})
```

**Notes:**
- `"rb"` means "read binary" - files must be opened in binary mode for uploads.
- The `with` block auto-closes the file after the request finishes.

---

## Part 4: Reading the Response Object

Every request returns a `Response` object with these key attributes:

```python
response = requests.get("https://api.github.com/users/octocat")

response.status_code  # 200 - integer HTTP status code
response.ok  # True if status_code < 400 - quick success check
response.text  # raw response body as a string
response.content  # raw response body as bytes (for images, files, etc.)
response.json()  # parses body as JSON -> Python dict/list
response.headers  # dict-like object of response headers
response.url  # the final URL (after redirects, params applied)
response.elapsed  # how long the request took (timedelta)
```

**Example - inspecting everything:**

```python
response = requests.get("https://api.github.com/users/octocat")

print("Status:", response.status_code)
print("Content-Type:", response.headers["Content-Type"])
print("Response time:", response.elapsed.total_seconds(), "seconds")

data = response.json()
print("Name:", data["name"])
print("Followers:", data["followers"])
```

**Note:** `.json()` will raise a `json.JSONDecodeError` if the response isn't valid JSON (e.g., the server returned an HTML error page). Don't call it blindly - check `response.ok` first, or wrap it in a try/except.

---

## Part 5: Status Codes - The Vocabulary of HTTP

| Range | Meaning | Common examples |
|-------|---------|------------------|
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirect | 301 Moved Permanently, 304 Not Modified |
| 4xx | Client error (you made a mistake) | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx | Server error (their problem) | 500 Internal Server Error, 503 Service Unavailable |

```python
response = requests.get("https://api.github.com/users/this-user-does-not-exist-123456")

if response.status_code == 404:
    print("User not found")
elif response.ok:
    print(response.json())
else:
    print(f"Unexpected error: {response.status_code}")
```

**Note:** `response.ok` is shorthand for `response.status_code < 400`. It doesn't distinguish between 404 and 500 - use exact codes when the distinction matters.

---

## Part 6: Headers - Identifying Yourself to the Server

### Sending custom headers

```python
headers = {"User-Agent": "MyPythonApp/1.0", "Accept": "application/json"}
response = requests.get("https://api.github.com", headers=headers)
```

**Note:** Some APIs (and some websites) block requests that don't include a `User-Agent` header, because it looks like a bot with no identity. Setting one is good practice.

### Authorization headers (API keys / tokens)

```python
headers = {"Authorization": "Bearer YOUR_API_TOKEN_HERE"}
response = requests.get("https://api.example.com/data", headers=headers)
```

**Note:** This is the most common way modern APIs handle authentication - the token proves who you are without sending a password every time.

---

## Part 7: Authentication - Different Flavors

### 7.1 Basic Auth (username + password)

```python
from requests.auth import HTTPBasicAuth

response = requests.get(
    "https://api.example.com/protected", auth=HTTPBasicAuth("myusername", "mypassword")
)

# Shorthand - same effect:
response = requests.get(
    "https://api.example.com/protected", auth=("myusername", "mypassword")
)
```

**Note:** Basic Auth sends credentials encoded (not encrypted) in every request - only ever use this over HTTPS.

### 7.2 Bearer Token (most common for modern APIs)

```python
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
response = requests.get("https://api.example.com/data", headers=headers)
```

### 7.3 API Key in query params (less secure, but common)

```python
response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": "London", "appid": "YOUR_API_KEY"},
)
```

**Note:** API keys in URLs can end up in server logs and browser history - prefer headers when the API supports it.

---

## Part 8: Handling Errors Properly

Real networks fail. Real servers time out. Never assume a request will succeed.

```python
import requests

try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()  # raises HTTPError if status is 4xx or 5xx
    data = response.json()
    print(data)

except requests.exceptions.Timeout:
    print("Request timed out - server took too long to respond")

except requests.exceptions.ConnectionError:
    print("Failed to connect - check your internet or the URL")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")

except requests.exceptions.RequestException as e:
    # catch-all for anything requests-related that wasn't caught above
    print(f"An error occurred: {e}")
```

**Why each piece matters:**
- `timeout=5` - without this, a hung server can freeze your program forever. **Always set a timeout.**
- `raise_for_status()` - converts a "silent" 404/500 into an actual Python exception you can catch, instead of you having to manually check `status_code` everywhere.
- Catching `RequestException` last - it's the parent class of all `requests` errors, so it acts as a safety net for anything you didn't specifically anticipate.

---

## Part 9: Sessions - Efficiency for Multiple Requests

A `Session` object reuses the underlying TCP connection and remembers settings (headers, cookies) across multiple requests - faster and less repetitive.

```python
session = requests.Session()
session.headers.update({"Authorization": "Bearer YOUR_TOKEN"})

# Both requests reuse the same connection and auth header automatically
response1 = session.get("https://api.example.com/profile")
response2 = session.get("https://api.example.com/orders")

session.close()  # good practice when done
```

**When to use a session vs plain `requests.get()`:**

| Situation | Use |
|-----------|-----|
| One-off single request | `requests.get()` |
| Multiple requests to the same API/site | `Session()` |
| Need to persist login cookies across requests | `Session()` |

**Bonus - using a session as a context manager (auto-closes):**

```python
with requests.Session() as session:
    session.headers.update({"Authorization": "Bearer YOUR_TOKEN"})
    response = session.get("https://api.example.com/data")
```

---

## Part 10: Advanced Topics (Good to Know, Not Urgent)

### 10.1 Timeouts with separate connect/read values

```python
response = requests.get("https://api.example.com", timeout=(3, 10))
# 3 seconds to connect, 10 seconds to receive a response
```

### 10.2 Disabling SSL verification (rarely needed, use with caution)

```python
response = requests.get("https://self-signed-site.com", verify=False)
```

**Note:** Only do this for trusted internal/testing environments. Disabling SSL verification on public-facing requests is a security risk - it opens you up to man-in-the-middle attacks.

### 10.3 Following (or blocking) redirects

```python
response = requests.get("https://example.com", allow_redirects=False)
print(response.status_code)  # will show 301/302 instead of following it
```

### 10.4 Streaming large files (don't load everything into memory)

```python
response = requests.get("https://example.com/large-file.zip", stream=True)

with open("large-file.zip", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

**Note:** `stream=True` downloads the file in chunks instead of loading it all into RAM at once - essential for large files.

### 10.5 Proxies

```python
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}
response = requests.get("https://api.example.com", proxies=proxies)
```

---

## Part 11: Putting It All Together - A Real Function

```python
import requests


def get_github_user(username):
    """Fetch a GitHub user's public profile info, safely."""
    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "name": data.get("name"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
        }

    except requests.exceptions.HTTPError:
        print(f"User '{username}' not found or API error ({response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Network problem: {e}")

    return None


result = get_github_user("octocat")
print(result)
```

This one function touches almost every concept above: GET, timeout, status handling, JSON parsing, and layered exception handling.

---

## Part 12: Free Resources to Learn and Practice

### Official documentation (best starting point)
- **Requests official docs**: https://requests.readthedocs.io/en/latest/ - clear, example-driven, the primary source of truth
- **Requests Quickstart**: https://requests.readthedocs.io/en/latest/user/quickstart/ - a faster version of what you just read

### Free APIs to practice against (no signup required)
- **httpbin.org** (https://httpbin.org) - echoes back whatever you send; perfect for understanding exactly what your requests look like
- **JSONPlaceholder** (https://jsonplaceholder.typicode.com) - fake REST API with posts, comments, users - supports GET/POST/PUT/DELETE
- **GitHub REST API** (https://docs.github.com/en/rest) - real-world API, no auth needed for public data, great for building small tools
- **Open-Meteo** (https://open-meteo.com) - free weather API, no API key required at all

### Free APIs that require a (free) API key - good for practicing auth
- **OpenWeatherMap** (https://openweathermap.org/api) - free tier, teaches you query-param-based API keys
- **NewsAPI** (https://newsapi.org) - free tier, teaches header-based auth

### Interactive practice platforms
- **Postman** (https://www.postman.com) - not Python, but lets you visually explore what requests/responses look like before writing code - genuinely useful for beginners to build intuition
- **RequestBin / Beeceptor** (https://beeceptor.com) - create a temporary endpoint and inspect exactly what your Python code sends it

### Video/course resources (free)
- **Corey Schafer's Requests tutorial** (YouTube) - well-regarded, beginner-friendly walkthrough
- **Real Python - Requests guide**: https://realpython.com/python-requests/ - free article, goes deeper into edge cases than most tutorials

---

## Part 13: Practical Next Steps (Build Real Skill, Not Just Read)

1. **Warm-up**: Use `httpbin.org` to send a GET, POST, and PUT request. Print `response.json()` each time and study what got echoed back.
2. **First real project**: Write a script using the GitHub API that takes a username and prints their repo count and top 5 repos by stars.
3. **Practice auth**: Sign up for a free OpenWeatherMap key, and build a small CLI tool that takes a city name and prints the current temperature.
4. **Practice error handling**: Deliberately break things - pass a bad URL, an invalid username, disconnect your wifi - and confirm your try/except blocks catch each case gracefully instead of crashing.
5. **Practice sessions**: Build a script that logs into JSONPlaceholder-style fake data and makes 3-4 sequential requests using one `Session()`, comparing the speed against making them without a session.
