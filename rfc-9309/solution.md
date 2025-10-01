# Challenge Prompt

Sorry. You know every CTF has to have it. 🤷

## Solution

Though from the name of the challenge I expected something to do with the `robots.txt` file, the VM served a page similar (but not identical) to [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html).

I first tried to fetch robots.txt with curl, but it required a token. After digging a bit I found the token in the browser's localStorage and used it:

```bash
curl -s -b "token=7075890---------878asd0776891" "https://7-----.proxy.coursestack.com/robots.txt"
```

The response contained many empty lines; the flag was hidden in the middle:

```text
flag{--ec1142c199a--}
```
