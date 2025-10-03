import base64

INPUT_FILE = "base64decodedAndExtracted"

if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as file:
        data = file.read().rstrip()

    i = 0

    stringList = data.split('\n')
    for string in stringList:
        if '"' in string:
            try:
                # Extract the base64 string between quotes
                base64_string = string.split('"')[1]
                decoded_content = base64.b64decode(base64_string).decode('utf-8')
                
                with open(f'script{i}.ps1', 'w') as output_file:
                    output_file.write(decoded_content)
                
                print(f"Successfully decoded script{i}.ps1")
                i += 1
                
            except Exception as e:
                print(f"Error decoding line {i}: {e}")
                print(f"Problematic line: {string[:100]}...")
        
    
