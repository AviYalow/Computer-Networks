import socket

#IP = '0.0.0.0'
#PORT = 80
SOCKET_TIMEOUT = 0.1
ROOT = "C:\\Networks\\webroot"
PROTOCOL_VERSION = "HTTP/1.1"
DEFAULT_URL = "\\index.html"
REDIRECTION_DICTIONARY = {"/stam.html": DEFAULT_URL}
STATUS_CODE = {200: " 200 OK", 302: " 302 Moved temporarily", 404: " 404 Not Found"}


def get_file_data(filename):
    """ Get data from file """
    filename = ROOT + filename
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data


def get_name_and_type(url):
    """
     extract the name file and the type file from the request
    :param url: url from the request
    :return: name and type of the file
    """
    index_start_name = url.rfind('/', 0, len(url) - 1) + 1
    index_start_type = url.rfind('.', 0, len(url) - 1) + 1
    filename = url[index_start_name:]
    filetype = url[index_start_type:]
    return filename, filetype


def gets_parameters(url):
    """
    extract parameters from url
    :param url: a given url
    :return: dictionary with the parameters and they value
    """
    if '/calculate-area?' in url:

        # find the start index of the parameters
        index = url.find('/calculate-area?') + len('/calculate-area?')

        parameters_lst = url[index:].split('&')

        # creating a dictionary for the parameters
        parameters_dict = {}
        for param in parameters_lst:
            param = param.split('=')
            parameters_dict[param[0]] = param[1]

        return parameters_dict


def handle_get_with_parameters(resource):
    """
    handle get request with parameters
    :param resource: a given resource
    :return: the required data
    """
    parameters = gets_parameters(resource)
    if '/calculate-area?' in resource:
        # if parameters['height'].isnumeric() and parameters['width'].isnumeric():
        try:
            res = float(parameters['height']) * float(parameters['width']) / 2
            if res % 2 == 0.0:
                res = int(res)
            return res
        except:
            return "NaN"


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""

    if resource == '/':
        url = DEFAULT_URL
    else:
        url = resource

    # building the response header. the template: http version, status code ,optional filed, data.
    http_header = PROTOCOL_VERSION

    # check if URL had been redirected, not available or other error code.
    if url in REDIRECTION_DICTIONARY:
        url = REDIRECTION_DICTIONARY[url]
        http_header += STATUS_CODE[302] + "\r\n"

    try:
        http_header += STATUS_CODE[200] + "\r\n"
        # handle with a get with parameters requests
        content_type = ""
        if '?' in url:
            data = str(handle_get_with_parameters(url)).encode()

        # handle with a regular get requests
        else:
            filename, filetype = get_name_and_type(url)
            if filetype == 'html':
                content_type = "Content-Type: text/html; charset=utf-8\r\n"
            elif filetype == 'js':
                content_type = "Content-Type: text/javascript\r\n"
            elif filetype == 'css':
                content_type = "Content-Type: text/css\r\n"
            elif filetype == 'jpg':
                content_type = "Content-Type: image/jpeg\r\n"
            elif filetype == 'ico':
                content_type = "Content-Type: image/x-icon\r\n"

            # read the data from the file
            data = get_file_data(url)
        content_len = "Content-Length: " + str(len(data)) + "\r\n"
        http_response = (http_header + content_len + content_type + "\r\n").encode() + data
    
    except:

        # handle with a 404 status cases
        http_response = (PROTOCOL_VERSION + STATUS_CODE[404] + "\r\n").encode()

    finally:

        client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # Extracting the first line of the request and separating it

    method, url, version = request.split("\r\n")[0].split()
    if method == "GET" and version == PROTOCOL_VERSION:
        return True, url
    else:
        return False, url


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        try:
            client_request = client_socket.recv(1024).decode()
        except socket.error as socEr:
            print("ERROR: {}".format(socEr))
            continue
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
