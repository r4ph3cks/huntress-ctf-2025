# Huntress CTF 2025 - 📦 Trust Me

- **Team:** `r4ph3cks`
- **Date:** `07/10/2025`

## Challenge Information

- **Category:** `📦 Miscellaneous`

- **Description:**
> C'mon bro, trust me! Just trust me!! Trust me bro!!!

> The TrustMe.exe program on this Windows desktop "doesn't trust me?"

> It says it will give me the flag, but only if I "have the permissions of Trusted Installer"...?

> If you are using the VPN, you can RDP to this challenge with:

```
Username: Administrator
Password: h$4#82PSK0BUBaf7
```

> [!NOTE]
> This virtual machine does not have Internet access.

- **Author:** [`John Hammond`](https://www.youtube.com/@_JohnHammond)

- **Given:** `Windows VM with TrustMe.exe`

## Analysis and Solution

Given the challenge description, we have a Windows executable named `TrustMe.exe` that requires "Trusted Installer" permissions to retrieve the flag. The challenge hints at needing elevated privileges, specifically those of the Trusted Installer account, which is a highly privileged system account in Windows.

### Initial Analysis

I'm 100% sure that I didn't do this challenge the intended way.

I researched how to elevate my privileges to Trusted Installer.
Got to the links:
https://nuventureconnect.com/blog/2025/01/22/trusted-installer-in-windows-how-to-run-a-program-with-the-highest-privileges/
https://www.tiraniddo.dev/2019/09/the-art-of-becoming-trustedinstaller.html

And tried to gain the privileges using these methods.

The non-existence of internet access made it impossible to run the first method. The second one didn't work for me.

And so I tried to find another way.

Connecting to the VM through RDP using [`Remmina`](https://remmina.org/) on Linux, I mounted a local folder containing the tool [`RunAsTrustedInstaller`](https://github.com/fafalone/RunAsTrustedInstaller).

I then executed TrustMe.exe using this tool, which successfully elevated the privileges to Trusted Installer and got me the flag:

```
flag{c6065b1f12395d526595e62cf1f4d82a}
```

## Observations
The challenge required elevating privileges to the Trusted Installer account, which is not a common user account and has the highest level of privileges in Windows.
This challenge tested knowledge of Windows security and privilege escalation techniques.