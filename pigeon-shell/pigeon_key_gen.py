import click

from Crypto.PublicKey import RSA
from pathlib import Path


@click.command()
@click.option('--dec_digits', default=2048, help='Length of RSA private key')
@click.option('--save_dir', default='.', help='Directory to save both keys')
def gen_pair(dec_digits: int=2048, save_dir: str='.'):
    """Generate public and private key then save to files

        \b
        private key is saved to `private.pigeon.txt`
        public key is saved to `public.pigeon.txt`

    Parameters:

        \b
        dec_digits: int << Length of RSA private key
        save_dir: str << Directory to save both keys

    Returns:

        \b
        None
    """
    key = RSA.generate(bits=dec_digits)
    Path(save_dir).mkdir(exist_ok=True)
    private = key.export_key()
    private_path = Path(save_dir).joinpath('private.pigeon.txt')
    with open(private_path, 'wb') as f:
        f.write(private) 

    # Generate public key from a RSA key
    public = key.publickey().export_key()
    public_path = Path(save_dir).joinpath('public.pigeon.txt')
    with open(public_path, 'wb') as f:
        f.write(public)


if __name__ == '__main__':
    gen_pair()