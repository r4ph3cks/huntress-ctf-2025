# Huntress CTF 2025 - 👶 Maximum Sound

- **Team:** `r4ph3cks`
- **Date:** `03/10/2025`

## Challenge Information

- **Category:** `👶 Warmups`

- **Description:**
> Dang, this track really hits the target! It sure does get loud though, headphone users be warned!!

- **Author:** [`John Hammond`](https://www.youtube.com/@_JohnHammond)

- **Given:** [`maximum_sound.wav`](assets/maximum_sound.wav)

## Analysis and Solution

Given the challenge description, we need to examine the audio file for any hidden messages or flags.

### Initial Analysis

The audio file appears to be a standard WAV file. Listening to it reveals a loud sound, but there might be more beneath the surface.

Analyzing the file to see metadata info, strings or info on the hexdump doesn't show anything useful.

Searching for the audio description was hard but after some digging we found this thread https://dsp.stackexchange.com/questions/78367/how-to-decode-a-binary-signal-in-a-wav-file-into-binary-sent-here-from-stackov (I'm still not quite sure how I found it).

The thread had an answer talking about SSTV (Slow Scan Television) which is a method of transmitting still images via audio signals. This seems promising.

After some research, we found this tool https://github.com/colaclanth/sstv.

Using the tool on the WAV file we got the following image:

![output.png](assets/output.png)

Using reverse image search on the center qr code looking thing we got that this could be a thing called "MaxiCode" that is a two-dimensional barcode used by United Parcel Service.

Cropping the MaxiCode from the image and scanning it with an online MaxiCode reader (https://www.dynamsoft.com/barcode-reader/barcode-types/maxicode/) we got the following containing the flag:

```
Maxicode: flag{d60ea9faec46c2de1c72533ae3ad11d7}
```

## Observations

This challenge was a great exercise in thinking outside the box and exploring different methods of data encoding. The use of SSTV to hide an image within an audio file is a clever technique that showcases the versatility of data transmission methods. It also highlights the importance of being familiar with various encoding schemes, such as MaxiCode, which may not be as commonly encountered as QR codes or barcodes. Overall, this challenge reinforced the value of thorough analysis and creative problem-solving in CTF competitions.