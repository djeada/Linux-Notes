## Reasons for Encryption

Encryption is a method to protect data from unauthorized access or tampering. Reasons to use encryption include:

* Safeguarding sensitive or confidential information.
* Preserving privacy and confidentiality in communications or data transfers.
* Defending data from modification or tampering.
* Compressing data for efficient network transfers.

## GPG Keys

Create public and private GPG keys on a Debian-based system with these steps:

1. Install the `gnupg2` package:

```bash
apt install gnupg2
```

2. Generate a GPG key pair:

```bash
gpg2 --gen-key
```

3. In the` ~/.gnupg` directory, find the generated keys:

```bash
pubring.gpg # public key
secring.gpg # private key
```

4. Confirm the keys with:

```bash
gpg2 --list-keys
gpg2 --list-secret-keys
```

## Encrypt and decrypt files using GPG

1. Import the recipient's public key:

```bash
gpg2 --import examplekey.asc
```

2. Trust the public key:

```bash
gpg2 --edit-key user@domain.com
```

3. Encrypt the file using the recipient's public key:

```bash
gpg2 -e -r user@domain.com example.txt
```

This creates an encrypted file `example.txt.gpg`, smaller than the original.

4. Have the recipient decrypt the file with their private key:

```bash
gpg2 -o example.txt -d example.txt.gpg
```

This will create a decrypted file called `example.txt`.

## Challenges

1. Try GPG commands by:
  - Generating a public and private key.
  - Encrypting a file with the public key.
  - Decrypting the file with the private key.
  - Confirming the decrypted file matches the original.
2. Can you encrypt a file without a public key?
3. Should a password be used for encryption?
4. Is it safe to share a private key?
