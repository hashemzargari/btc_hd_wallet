from utils import *
from bitcoinlib.keys import HDKey


class HDWallet:
    def __init__(self,
                 entrophy: str = None,
                 mnemonic: list[str] = None,
                 seed: str = None,
                 master_private_key: str = None,
                 chain: str = None,
                 master_public_key: str = None
                 ):
        self.entrophy = entrophy
        self.mnemonic = mnemonic
        self.seed = seed
        self.master_private_key = master_private_key
        self.chain = chain
        self.master_public_key = master_public_key

        # init basic data
        self.hd = None
        self.hd = self.get_wallet()

    def get_wallet(self) -> HDKey:
        if self.hd:
            return self.hd

        if self.master_private_key is None or self.chain is None:
            if self.seed is None:
                if self.mnemonic is None:
                    if self.entrophy is None:
                        self.entrophy = random_entrophy()
                    self.mnemonic = mnemonic_from_entrophy(self.entrophy)
                self.seed = seed_from_mnemonic(self.mnemonic)

            self.master_private_key, self.chain = master_private_key_chain_from_seed(self.seed)
        hd_ = get_hd_from_private_key_chain(self.master_private_key, self.chain)
        self.master_public_key = hd_.public_hex
        self.chain = hd_.chain.decode()
        return get_hd_from_private_key_chain(self.master_private_key, self.chain)

    def get_normal_child(self, index: int):
        if index < 0 or index >= 2147483647:
            raise ValueError('please Use an index between 0 and 2147483647')
        data = self.master_public_key + str(index)
        key = self.chain
        child_master_private_key, child_chain = normal_child_private_key_from_data_key(data, key)
        return HDWallet(master_private_key=child_master_private_key, chain=child_chain)

    def get_hardened_child(self, index: int):
        index += 2147483647
        if index < 2147483647 or index >= 4294967295:
            raise ValueError('please Use an index between 2147483647 and 4294967295')
        data = self.master_private_key + str(index)
        key = self.chain
        child_master_private_key, child_chain = normal_child_private_key_from_data_key(data, key)
        return HDWallet(master_private_key=child_master_private_key, chain=child_chain)

    def get_wallet_for_derivation_path(self, derivation_path: str):
        m, purpose, coin_type, account, change, index = derivation_path.split('/')

        child_ = get_child_from_sub_derivation_path(self, purpose)
        child_ = get_child_from_sub_derivation_path(child_, coin_type)
        child_ = get_child_from_sub_derivation_path(child_, account)
        child_ = get_child_from_sub_derivation_path(child_, change)
        child_ = get_child_from_sub_derivation_path(child_, index)

        address = None

        # TODO

        if '44' in purpose:  # BIP 44, P2PKH
            pass
        elif '49' in purpose:  # BIP 49
            pass
        elif '84' in purpose:  # BIP 84
            pass
        else:
            raise ValueError('please use standard purpose. ex: BIP44, BIP49, BIP84')


if __name__ == '__main__':
    hd = HDWallet()
    hd2 = HDWallet(
        mnemonic=['mystery', 'quality', 'kangaroo', 'jar', 'inspire',
                  'stay', 'nose', 'oval', 'coconut', 'life', 'view', 'creek']
    )
    print(hd2.master_public_key, hd2.chain)

    normal_child_5 = hd2.get_normal_child(index=5)
    print(normal_child_5.master_private_key)
    print(normal_child_5.master_private_key == 'ea3f12c2b491a5a9bd03120043e947ea83721873125f12562c5cc66fd76ebeec')

    hardened_child_5 = hd2.get_hardened_child(index=5)
    print(hardened_child_5.master_private_key)
    print(hardened_child_5.master_private_key == 'e92393884d1a98cd4ecd6a59647dcb7f14ed6327350a084aca8c1bfec4690d91')

    print('done')
