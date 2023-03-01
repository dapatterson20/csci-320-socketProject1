import socket
import os
import hashlib  # needed to verify file hash
import time
import select


IP = '127.0.0.1'  # change to the IP address of the server
PORT = 13000  # change to a desired port number
BUFFER_SIZE = 10024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8],byteorder='big')


def upload_file(server_socket: socket, file_name: str, file_size: int):
    print('called')
    # create a SHA256 object to verify file hash
    # TODO: section 1 step 5 in README.md file
    print(f"Encode: {file_name}")
    hsh=hashlib.sha256(file_name.encode())
    print(hsh.digest())
    # create a new file to store the received data
    with open(file_name+'.temp', 'wb') as file:
        print('while')
        # TODO: section 1 step 7a - 7e in README.md file
        try:
            while True:
                server_socket.setblocking(0)
                ready = select.select([server_socket], [], [], 1)
                if ready[0]:
                    chunk, client_address = server_socket.recvfrom(BUFFER_SIZE)
                else:
                    server_socket.setblocking(1)
                    break
                print('a')
                chunkst=get_file_info(chunk)[0]
                print(chunkst)
                file.write(chunk)
                hsh.update(chunk)
                print('b')
                server_socket.sendto(b'received', client_address)
                print('received')
                # time.sleep(1)
                # server_socket.sendto(b'received', (IP, PORT))
                print('c')
                if len(chunk) < 1:
                    print('k')
                    break

        except KeyboardInterrupt as ki:
            print("Shutting down...")
    # get hash from client to verify
    # TODO: section 1 step 8 in README.md file
    print('hash check')
    server_socket.setblocking(1)
    server_socket.sendto(b'send hash', client_address)
    response2, client_address = server_socket.recvfrom(BUFFER_SIZE)
    print(f'Response 2: {response2}')
    print(hsh.digest())
    # TODO: section 1 step 9 in README.md file
    if response2==hsh.digest():
        print('success')
        server_socket.sendto(b'success', client_address)
        print('done')
    else:
        print('hkl;ji')
        #os.remove(file_name+'.temp')
        server_socket.sendto(b'failed', client_address)


def start_server():
    # create a UDP socket and bind it to the specified IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print(f'Server ready and listening on {IP}:{PORT}')

    try:
        while True:
            # TODO: section 1 step 2 in README.md file
            # expecting an 8-byte byte string for file size followed by file name
            name, client_address = server_socket.recvfrom(BUFFER_SIZE)

            # TODO: section 1 step 3 in README.md file
            #file_size = get_file_info(name[:8])
            file_size = get_file_info(name)[1]
            file_name = get_file_info(name)[0]
            print(name)
            print(file_size)
            print(file_name)
            #file_size = int.from_bytes(file_size, byteorder='big')
            # TODO: section 1 step 4 in README.md file
            print(time.time())
            print('aaaa')
            server_socket.sendto(b'go ahead', client_address)
            #time.sleep(0.1)
            #server_socket.sendto(b'go ahead', client_address)
            print('bbb')
            upload_file(server_socket, file_name, file_size)
            break
    except KeyboardInterrupt as ki:
        pass
    except Exception as e:
        print(f'An error occurred while receiving the file:str {e}')
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()
