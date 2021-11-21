import binascii
import random
import secrets
import hashlib
import hmac
from consts import bip39_wordlist
from bitcoinlib.keys import HDKey


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def random_hex_key(n_bytes: int = 64) -> str:
    return str(secrets.token_hex(n_bytes))


def master_private_key_chain_from_seed(seed: str, salt: str = 'btc_seed') -> (str, str):
    string = str(hmac.new(seed.encode(), salt.encode(), hashlib.sha512).hexdigest())
    return string[:int(len(string) / 2)], string[int(len(string) / 2):]


def random_entrophy(n_bits: int = 128) -> str:
    return ''.join([str(random.randint(0, 1)) for _ in range(n_bits)])


def mnemonic_from_entrophy(entrophy: str) -> list[str]:
    entrophy_ = entrophy.encode()
    result = hashlib.sha256(entrophy_).hexdigest()
    check_some = "{0:08b}".format(int(result, 16))
    check_some = check_some[:int(len(entrophy_) / 32)]
    result = entrophy + check_some
    chunks_ = [''.join(x) for x in list(chunks(list(result), 11))]
    mnemonic = [bip39_wordlist[y] for y in [int(x, 2) for x in chunks_]]
    return mnemonic


def seed_from_mnemonic(mnemonic: list[str], salt: str = '') -> str:
    mnemonic_str = ' '.join(mnemonic)
    return str(binascii.hexlify(hashlib.pbkdf2_hmac('sha512', mnemonic_str.encode(), salt.encode(), 2048)).decode())


def get_hd_from_private_key_chain(private_key: str, chain: str, as_dict: bool = False) -> HDKey or dict:
    if as_dict:
        return dict(HDKey(import_key=private_key, chain=chain.encode()).as_dict())
    return HDKey(import_key=private_key, chain=chain.encode())


if __name__ == '__main__':
    e = random_entrophy()
    m = mnemonic_from_entrophy(e)
    s = seed_from_mnemonic(m)
    master_private_key, chain_code = master_private_key_chain_from_seed(s)
    hd = get_hd_from_private_key_chain(master_private_key, chain_code, False)
    print('entrophy', e)
    print('mnemonic', m)
    print('seed', s)
    print('master_private_key', master_private_key)
    print('chain_code', chain_code)
    print('HD', hd)

    print('done')