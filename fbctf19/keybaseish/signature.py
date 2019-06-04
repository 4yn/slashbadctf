from Crypto.PublicKey import RSA
from Crypto import Random

def print_twitter(sig):
    sig_str = str(sig)
    n = (len(sig_str) / 255) + 1
    chunks, chunk_size = len(sig_str), int(len(sig_str)/n) + 1
    tweets = [ sig_str[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    print("Please post these signature strings as public twitter posts from your accout:")
    for ndx in range(len(tweets)):
        print ('  "PRF{}/{}:{}"'.format(ndx+1, len(tweets), tweets[ndx]))

def main():
    rng = Random.new().read
    print('Enter challenge pin from site: ')
    pin = input()
    print('Signing "{}" with a new RSA key....'.format(pin))
    RSAkey = RSA.generate(1024, rng)
    signature = RSAkey.sign(int(pin), rng)
    key_params = RSAkey.__getstate__()
    print_twitter(signature[0])
    print('\\n\\nPlease input your public key on the web form:')
    print('  "{}:{}"'.format(key_params['e'], key_params['n']))
    print('\\n\\n')

if __name__ == '__main__':
    main()