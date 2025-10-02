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