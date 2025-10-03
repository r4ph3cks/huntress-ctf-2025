import base64

INPUT_FILE = "base64chunks.txt"
OUTPUT_FILE = "base64decodedAndExtracted.txt"

def extract(data):
    return data.replace('"', '').replace('&', '').replace('_', '').replace('\n', '')


if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as file:
        data = file.read().rstrip()

    with open(OUTPUT_FILE, 'w') as output_file:
        output_file.write(base64.b64decode(extract(data)).decode())


    
    