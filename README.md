# btc_hd_wallet

implementation of hd wallet for bitcoin and other utils

testing repo

# TODO:
    update project with crypto_tools repo:
    https://github.com/mcdallas/cryptotools/

Examples
--------
HD Wallets :

```python

from hd_wallet import HDWallet
    
# new wallet
>>> hd = HDWallet()
>>> ' '.join(hd.mnemonic)
'mystery quality kangaroo jar inspire stay nose oval coconut life view creek'

# restore old wallet with mnemonic
>>> hd = HDWallet(mnemonic=['mystery', 'quality', 'kangaroo',
                           'jar', 'inspire', 'stay',
                           'nose', 'oval', 'coconut',
                           'life', 'view', 'creek'])
>>> hd.master_private_key
'ea3f12c2b491a5a9bd03120043e947ea83721873125f12562c5cc66fd76ebeec'
    
# get HDKey
>>> hd_key = hd.get_wallet()
    
# get n'th normal child
# return new instance from HDWallet
>>>> normal_child_5 = hd.get_normal_child(index=5)
    
# get n'th hardened child
# return new instance from HDWallet
>>>> hardened_child_5 = hd2.get_hardened_child(index=5)
    
# get derivation path (soon ...)
# return new instance from HDWallet
>>>> m = hd.get_wallet_for_derivation_path('m/44h/0h/0h/0')
```
