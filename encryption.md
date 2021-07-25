Because an encrypted file is typically smaller than a non-encrypted file, it transfers more quickly.

<h1>Make public and private GPG keys.</h1>

1. On Ubuntu/Mint:

```bash
sudo apt install gnupg2
```

2. GPG key generation.

```bash
gpg2 --gen-key
```

3. Check you .gnupg directory. By default it is in your home dir ~/.gnupg. Expected content:

```bash
pubring.gpg #this is your public key
secring.gpg #this is your private key
```

4. To verify your keys use the following commands:

```bash
gpg2 --list-keys
gpg2 --list-secret-keys
```

<h1>File encryption and decryption</h1>
You've obtained a public key from someone and want to use it to encrypt a file so that it may be safely sent.
The public key is generally stored in a file with the extension .gpg or.asc.

1. Import the public key:

```bash
gpg2 --import examplekey.asc
```

2. Trust the public key:

```bash
gpg2 --edit-key user@domain.com
```

3. Encrypt the file with the public key of the user:

```bash
gpg2 -e -r user@domain.com example.txt
```

4. This will create the example.txt.gpg encrypted file, which is smaller than the initial.
Send the encrypted file to the receiver and ask them to decode it using the following command at their end:

```bash
gpg2 -o example.txt -d example.txt.gpg
```
