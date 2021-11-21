import binascii
import random
import secrets
import hashlib
import hmac
import base58
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


def normal_child_private_key_from_data_key(data: str, key: str) -> (str, str):
    string = str(hmac.new(data.encode(), key.encode(), hashlib.sha512).hexdigest())
    return string[:int(len(string) / 2)], string[int(len(string) / 2):]


def get_hd_from_private_key_chain(private_key: str, chain: str, as_dict: bool = False) -> HDKey or dict:
    if as_dict:
        return dict(HDKey(import_key=private_key, chain=chain.encode()).as_dict())
    return HDKey(import_key=private_key, chain=chain.encode())


def get_hd_from_public_key_chain(public_key: str, chain: str, as_dict: bool = False) -> HDKey or dict:
    pass  # TODO


def get_child_from_sub_derivation_path(parent, derivation: str):
    derivation = derivation.split('h')
    child = None
    if len(derivation) > 1:  # hardened
        child = parent.get_hardened_child(int(derivation[0]))
    else:  # normal
        child = parent.get_normal_child(int(derivation[0]))

    return child


def p2pkh_from_public_key(public_key: str, prefix: str = '00') -> str:
    hash_ = hashlib.new('ripemd160', hashlib.sha256(public_key.encode()).digest()).hexdigest()
    result = hashlib.sha256(hash_.encode()).hexdigest()
    check_some = "{0:08b}".format(int(result, 16))
    check_some = check_some[:8]
    result = prefix + hash_ + check_some
    return base58.b58encode(result).decode()
    # TODO-> update project with crypto_tools repo


if __name__ == '__main__':
    # e = random_entrophy()
    # m = mnemonic_from_entrophy(e)
    # s = seed_from_mnemonic(m)
    # master_private_key, chain_code = master_private_key_chain_from_seed(s)
    # hd = get_hd_from_private_key_chain(master_private_key, chain_code, False)
    # print('entrophy', e)
    # print('mnemonic', m)
    # print('seed', s)
    # print('master_private_key', master_private_key)
    # print('chain_code', chain_code)
    # print('HD', hd)
    # print('NORMAL 5', normal_child_private_key_from_data_key(master_private_key + '5', chain_code))
    # print('done')
    print(p2pkh_from_public_key('mvm74FACaagz94rjWbNmW2EmhJdmEGcxpa'))
