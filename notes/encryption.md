<h1>Reasons for encryption</h1>

* One of the most important reasons for using encryption is to protect your data. Encryption is a way to hide the data from unauthorized users.
* Encrypted files are also usually smaller than the original files. This is because the data is encrypted and then compressed. Therefore they can be transferred over a network much more efficiently.

<h1>Make public and private GPG keys.</h1>

1. On debian based distributions:

```bash
apt install gnupg2
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

<h1>Challenges</h1>

1. Test the gpg2 command:
- Create a public key and a private key.
- Encrypt a file using the public key.
- Decrypt the file using the private key.
- Verify that the decrypted file is the same as the original.

2. Is there a way to encrypt a file without using a public key?
3. Should a password be used to encrypt a file?
4. Can you share the private key with someone?
