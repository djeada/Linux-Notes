## Reasons for encryption
Encryption is a technique used to protect data from unauthorized access or tampering. There are many reasons to use encryption, including:

* Protecting sensitive or confidential information from being accessed by unauthorized users.
* Ensuring the privacy and confidentiality of communications or data transfer.
* Protecting data from being modified or tampered with.
* Reducing the size of data for more efficient transfer over a network.

## GPG keys

To create public and private GPG keys on a Debian-based system, you can follow these steps:

1. Install the gnupg2 package:

```bash
apt install gnupg2
```

2. Generate a GPG key pair:

```bash
gpg2 --gen-key
```

3. Check the `.gnupg` directory in your home directory (`~/.gnupg`) for the generated keys:

```bash
pubring.gpg # public key
secring.gpg # private key
```

4. Verify the keys using the following commands:

```bash
gpg2 --list-keys
gpg2 --list-secret-keys
```

To encrypt and decrypt files using GPG, you can use the following steps:

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

This will create an encrypted file called `example.txt.gpg`, which is smaller than the original file.

4. Send the encrypted file to the recipient and ask them to decrypt it using their private key:

```bash
gpg2 -o example.txt -d example.txt.gpg
```

This will create a decrypted file called `example.txt`.

## Challenges

* Test the GPG command by following these steps:
  - Create a public key and a private key.
  - Encrypt a file using the public key.
  - Decrypt the file using the private key.
  - Verify that the decrypted file is the same as the original.

* Is there a way to encrypt a file without using a public key?
* Should a password be used to encrypt a file?
* Can you share the private key with someone?
