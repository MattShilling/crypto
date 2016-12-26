# crypto

This repository contains cryptography work I have been doing.

I've been researching about encryption using private and public keys and will relay
what I have learned here:

Each person that wants to encrypt and decrypt messages has both a public key,
which is available to everyone, and a private key that only they know. 

Now here's how the encryption works: the private and public keys are mathematically related so that something encrypted using the public key can ONLY be decrypted using the private key. So, for example, if I wanted to send a secret message to Bob, I would encrypt it using HIS public key. That way he would be the only one that is able to decrypt it because only he knows his private key.
This works both ways. If Bob wants to send me something, he encrypts his message with MY public key and then I decrypt it using my super, top-secret private key. 



