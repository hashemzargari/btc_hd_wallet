from utils import *


class HDWallet:
    def __init__(self,
                 entrophy: str = None,
                 mnemonic: list[str] = None,
                 seed: str = None,
                 master_privet_key: str = None,
                 chain: str = None,
                 master_public_key: str = None
                 ):
        self.entrophy = entrophy
        self.mnemonic = mnemonic
        self.seed = seed
        self.master_privet_key = master_privet_key
        self.chain = chain
        self.master_public_key = master_public_key

    def __call__(self, *args, **kwargs):
        return self.get_wallet()

    def get_wallet(self):
        if self.master_privet_key is None or self.chain is None:
            if self.seed is None:
                if self.mnemonic is None:
                    if self.entrophy is None:
                        self.entrophy = random_entrophy()
                    self.mnemonic = mnemonic_from_entrophy(self.entrophy)
                self.seed = seed_from_mnemonic(self.mnemonic)

            self.master_privet_key, self.chain = master_private_key_chain_from_seed(self.seed)
            hd_ = get_hd_from_private_key_chain(self.master_privet_key, self.chain)
            self.master_public_key = hd_.public_hex
            self.chain = hd_.chain.decode()
        return get_hd_from_private_key_chain(self.master_privet_key, self.chain)


if __name__ == '__main__':
    hd = HDWallet()()
    hd2 = HDWallet(
        mnemonic=['mystery', 'quality', 'kangaroo', 'jar', 'inspire',
                  'stay', 'nose', 'oval', 'coconut', 'life', 'view', 'creek']
    )()
    print('done')
