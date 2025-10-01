#include <stdint.h>
#include <string.h>
#include <stdio.h>

void main() {
    uint8_t buffer[0x80];
    uint32_t *p = (uint32_t *)buffer;

    // Push the given 10 DWORD values onto the stack (simulate by storing in buffer)
    p[0] = 0x8484D893;
    p[1] = 0x97C6C390;
    p[2] = 0x929390C3;
    p[3] = 0xC7C3C490;
    p[4] = 0x939C939C;
    p[5] = 0xC6C69CC0;
    p[6] = 0x939CC697;
    p[7] = 0xC19DC794;
    p[8] = 0x9196C1DE;
    p[9] = 0xC2C4C9C3;

    // XOR each of the 10 DWORDs with 0xA5A5A5A5
    for (int i = 0; i < 10; i++) {
        p[i] ^= 0xA5A5A5A5;
    }

    // Print the modified values
    for (int i = 0; i < 10; i++) {
        // Transform to little-endian format for printing
        uint32_t val = p[i];
    }

    // Set byte at offset 0x26 in the stack frame to 0
    buffer[0x26] = 0;

    // Set byte at offset -0x81 from RBP to 0 (simulate with a separate variable)
    // Since we don't have RBP here, just declare a variable
    uint8_t rbp_minus_0x81 = 0;

    // Copy bytes from buffer (ESP) to another buffer at RBP-0x80 until zero byte is found
    uint8_t dest[0x80];
    uint8_t *src = buffer;
    uint8_t *dst = dest;
    while (*src != 0) {
        *dst++ = *src++;
    }
    *dst = 0;

    // Fill 0x40 bytes at buffer (RSP) with 1
    memset(buffer, 1, 0x40);
}