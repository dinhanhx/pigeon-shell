import click
import socket
import json

from _utils import import_key, encode_encrypt, decrypt_decode


BUFFER_SIZE = 4096


@click.command()
@click.option('--config_file', type=str, help='Filepath to where configs are saved')
def pigeon_client(config_file: str):
    """Setup connection to pigeon server

    Parameters:

        \b
        config_file: str << Filepath to where configs are saved

    Returns:

        \b
        None
    """
    config = json.load(open(config_file))
    server_ip = config['server_ip']
    server_port = config['server_port']
    client_private_key = config['client_private_key']
    server_public_key = config['server_public_key']

    client_private_key, server_public_key = import_key(client_private_key, server_public_key)

    soc = socket.socket()
    soc.connect((server_ip, server_port))

    while True:
        cwd = decrypt_decode(soc.recv(BUFFER_SIZE), client_private_key)
        cmd = input(f'{cwd}#>')
        if cmd.lower() == 'pigeonstop':
            soc.send(encode_encrypt(cmd, server_public_key))
            break

        soc.send(encode_encrypt(cmd, server_public_key))
        output = decrypt_decode(soc.recv(BUFFER_SIZE), client_private_key)
        print(output)

    soc.close()


if __name__ == '__main__':
    pigeon_client()

