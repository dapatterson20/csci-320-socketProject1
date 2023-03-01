import socket
import hashlib  # needed to calculate the SHA256 hash of the file
import sys  # needed to get cmd line parameters
import os.path as path  # needed to get size of file in bytes
import time

#127.0.0.1
#12000
IP = '127.0.0.1'  # change to the IP address of the server
PORT = 13000  # change to a desired port number
BUFFER_SIZE = 10024  # change to a desired buffer size


def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str):
    # get the file size in bytes
    # TODO: section 2 step 2 in README.md file
    file_size=get_file_size(filename)
    # convert the file size to an 8-byte byte string using big endian
    # TODO: section 2 step 3 in README.md file
    size = file_size.to_bytes(8, byteorder='big')
    # create a SHA256 object to generate hash of file
    # TODO: section 2 step 4 in README.md file
    print(f"Encode: {filename}")
    file_hash=hashlib.sha256(filename.encode())
    print(file_hash.digest())
    # create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # send the file size in the first 8-bytes followed by the bytes
        # for the file name to server at (IP, PORT)
        # TODO: section 2 step 6 in README.md file
        client_socket.sendto(size + filename.encode(), (IP, PORT))
        # TODO: section 2 step 7 in README.md file
        print('lsk;djfa')
        response, server_address = client_socket.recvfrom(BUFFER_SIZE)
        print(response)
        #while len(response)<1:
        if response!=b'go ahead':
            raise Exception('Bad server response - was not go ahead!')
            #file_hash.update()
        #else:

            '''
            try:
                #client_socket.sendto(message.encode(), server)
                
            except socket.timeout or response!=b'go ahead':
            '''




        # open the file to be transferred
        with open(filename, 'rb') as file:
            print('a')
            # read the file in chunks and send each chunk to the server
            # TODO: section 2 step 8 a-d in README.md file
            while len(file.read(BUFFER_SIZE))>0:
                print('b')
                chunk=file.read(BUFFER_SIZE)
                file_hash.update(chunk)
                client_socket.sendto(chunk, (IP, PORT))
                print('r1')
                print(time.time())
                response2, server_address = client_socket.recvfrom(BUFFER_SIZE)
                print('r2')
                print(response2)
                if response2!=b'received':
                    raise Exception('Bad server response - was not received')
                '''
                if len(file.read(BUFFER_SIZE))<1:
                    print('k')
                    break
                '''
                '''
                while len(response2) < 1:
                    try:
                        
                    except socket.timeout:
                        
                bNum+=4
                '''


        # send the hash value so server can verify that the file was
        # received correctly.
        # TODO: section 2 step 9 in README.md file
        print('done')
        print(file_hash.digest())
        hashResponse, server_address=client_socket.recvfrom(BUFFER_SIZE)
        if hashResponse==b'send hash':
            client_socket.sendto(file_hash.digest(), server_address)
        print('continue')
        # TODO: section 2 steps 10 in README.md file
        #client_socket.sendto(size + chunk.encode(), (IP, PORT))
        print('s;lfjal;')
        response3, server_address = client_socket.recvfrom(BUFFER_SIZE)
        print(response3)
        # TODO: section 2 step 11 in README.md file
        if response3 == b'failed':
            raise Exception('Transfer failed!')
        else:
            print('Transfer completed!')


        
    except Exception as e:
        print(f'An error occurred while sending the file: {e}')
    finally:
        client_socket.close()


if __name__ == "__main__":
    # get filename from cmd line
    '''
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename>')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    '''
    #send_file(file_name)
    send_file('ReadmeTxt/README.txt')

