import click
import socket
import os
import subprocess
import json

from _utils import import_key, encode_encrypt, decrypt_decode
from datetime import datetime


BUFFER_SIZE = 4096


@click.command()
@click.option('--config_file', type=str, help='Filepath to where configs are saved')
def pigeon_server(config_file: str):
    """Setup pigeon server

    Parameters:

        \b
        config_dir: str << Filepath to where configs are saved

    Returns:

        \b
        None
    """
    config = json.load(open(config_file))
    server_port = config['server_port']
    server_private_key = config['server_private_key']
    client_public_key = config['client_public_key']

    server_private_key, client_public_key = import_key(server_private_key, client_public_key)

    soc = socket.socket()
    soc.bind(('0.0.0.0', server_port))
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    soc.listen(5)

    client_soc, client_add = soc.accept()
    print(f'{client_add[0]}:{client_add[1]} connected')

    while True:
        cwd = os.getcwd()
        client_soc.send(encode_encrypt(cwd, client_public_key))

        cmd = decrypt_decode(client_soc.recv(BUFFER_SIZE), server_private_key)
        if cmd.lower() == 'pigeonstop':
            print(f'{client_add[0]}:{client_add[1]} faded')
            break
        
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[On] {time_now} [in] {cwd} [executed] {cmd}')
        output = subprocess.getoutput(cmd)
        client_soc.send(encode_encrypt(output, client_public_key))

    client_soc.close()
    soc.close()

        


if __name__ == '__main__':
    pigeon_server()

