# Huntress CTF 2025 - 🔍 Webshellz

- **Team:** `r4ph3cks`
- **Date:** `22/10/2025`

## Challenge Information

- **Category:** `🔍 Forensics`

- **Description:**
> The sysadmin reported that some unexpected files were being uploaded to the file system of their IIS servers.

> As a security analyst, you have been tasked with reviewing the Sysmon, HTTP, and network traffic logs to help us identify the flags!

> ![NOTE]

> The password to the ZIP archive is webshellz

- **Author:** `Ben Folland`

- **Given:** [`webshellz.zip`](assets/webshellz.zip)

## Analysis and Solution

After extracting the provided ZIP file using the password `webshellz`, we find several log files that need to be analyzed. The main goal is to identify any webshells that have been uploaded to the IIS servers and extract the flags hidden within them.