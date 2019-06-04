# keybaseish (453) - FBCTF 19

> We built a secure messaging platform based on twitter identities, verified with our proprietary signature protocol! Right now our founder is the only one using it. Would you like to join?
>
> Note: You do not need a twitter account to solve this challenge
>
> http://challenges.fbctf.com:8080

We are given a web portal with a (broken) register page, login page and a forgot password page.

The forgot password page contains a link to the ["admin's" twitter page](https://twitter.com/baseishcoinfou1) with some interesting tweets:

```
@baseishcoinfou1 at 9:25 AM 3 Apr 2019: 
PRF1/2:43522081190908620239526125376626925272670879862906206214798620592212761409287968319160030205818706732092664958217053982767385296720310547463903001181881966

@baseishcoinfou1 at 9:25 AM 3 Apr 2019:
PRF2/2:554081621263332073144333148831108871059921677679366681345909190184917461295644569942753755984548017839561073991169528773602380297241266112083733072690367
```

The forgot password page also contains a link to a [signature generator](signature.py) which guides a user through the reset password proceedure.

The password reset proceedure involves the following:

1. Obtain a 6 digit (one-time) "Pin" from the reset password page
2. Generate a RSA key locally
3. Sign the "Pin" with the key and post the signature on your twitter handle
4. Provide the RSA public key to the reset password page

Given the contstraits of the challenge, we are given a predefined signature (as obtain from the tweets), a server-controlled "Pin" to sign and we thus need to produce a RSA public key (exponent and modulus) that will decrypt the signature to our desired "Pin".

As the signing script provided shows us that no padding is applied and that "textbook" RSA signing is used in this system, we only need to find some `n` and `e` such that `pin = pow(signature, e, n)`.

With some modulo arithmetic:

```python
pin = pow(signature, e, n)
    = pow(signature, e) - k * n # Where k is a positive integer
    = pow(signature, e) - n # Let k = 1

n = pow(signature, e) - pin
```

We can naively generate a `n` from some `e` where `n = pow(signature, e) - pin`. The system will accept this keypair despite the comparable size of `n` relative to `pow(signature, e)`. By testing, any `e` larger than 3 will be accepted by the system.

We can thus generate keypairs as such:

```python
signature = 43522081190908620239526125376626925272670879862906206214798620592212761409287968319160030205818706732092664958217053982767385296720310547463903001181881966554081621263332073144333148831108871059921677679366681345909190184917461295644569942753755984548017839561073991169528773602380297241266112083733072690367
pin = int(input("Pin: "))
e = 4

n = pow(signature, e) - pin
print("Key: \"{}:{}\"".format(e, n))
```

Submit a generated key from this script with user `baseishcoinfou1` and we obtain a temporary password that can be used to login to the system. The flag is presented on login.
