## Encryption

Encryption is the cornerstone of modern data security, ensuring that information remains confidential and unaltered during storage and transmission. By converting plaintext into ciphertext using cryptographic algorithms, encryption protects data from unauthorized access and tampering.

Main idea:

- Prevents unauthorized users from accessing sensitive information.
- Allows safe exchange of data over insecure networks.
- Ensures that data has not been altered during transit.
- Meets legal requirements like HIPAA or GDPR for protecting personal data.
  
**Visualization of Encryption Process:**

```
[ Plain Text ]     +--------------+     [ Cipher Text ]
    "Hello"   ---> | Encryption   | ---> "6hj7!#f&"
                   | Algorithm    |
                   +--------------+
```

**Visualization of Decryption Process:**

```
[ Cipher Text ]    +---------------+    [ Plain Text ]
   "6hj7!#f&" ---> | Decryption    | ---> "Hello"
                   | Algorithm     |
                   +---------------+
```

### GPG (GNU Privacy Guard)

GPG is an open-source implementation of the OpenPGP standard, providing cryptographic privacy and authentication through the use of public and private keys. It enables users to:

- Encrypt and decrypt data.
- Digitally sign and verify documents and messages.
- Manage cryptographic keys.

Main idea:

- A public key is primarily used to **encrypt** data, allowing only the corresponding private key holder to decrypt it.
- Public keys also play a critical role in verifying **signatures**, ensuring the authenticity of the sender’s message or document.
- Public keys are designed to be shared **openly**, enabling others to encrypt messages or verify signatures without compromising security.
- The private key, on the other hand, is used to **decrypt** data that was encrypted with the associated public key.
- Private keys are also responsible for creating digital **signatures**, which authenticate the identity of the sender.
- A private key must always be kept **secure**, as its exposure can lead to unauthorized decryption of data or fraudulent signature creation. 
- Both public and private keys are foundational components of **asymmetric** cryptography, which relies on the pairing of these keys for secure communication. 
- Sharing a public key is necessary for **establishing trust**, but under no circumstances should the private key be shared, as it is critical for maintaining security.

**Visualization of Public and Private Keys:**

```
[ Public Key ]  <--- Shared Openly --->  [ Private Key ]
    (Encrypt)                             (Decrypt)
     +-------> [ Encrypted Data ] <-------+
```

#### Generating GPG Keys

**Step 1: Install GPG**

```bash
sudo apt update
sudo apt install gnupg2
```

**Expected Output:**

```
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following NEW packages will be installed:
  gnupg2
...
Setting up gnupg2 (2.2.19-3ubuntu2.1) ...
```

**Step 2: Generate a New Key Pair**

```bash
gpg --gen-key
```

**Interactive Prompts and Expected Responses:**

```
gpg (GnuPG) 2.2.19; Copyright (C) 2019 Free Software Foundation, Inc.
...

Please select what kind of key you want:
   (1) RSA and RSA (default)
   ...

Your selection? 1

RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096

Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      ...

Key is valid for? (0) 0

Key does not expire at all
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: John Doe
Email address: john.doe@example.com
Comment: Work Key
You selected this USER-ID:
    "John Doe (Work Key) <john.doe@example.com>"

Change (N)ame, (E)mail, (C)omment, or (O)kay/(Q)uit? O

You need a Passphrase to protect your secret key.
...

We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, ...)

gpg: key 1A2B3C4D5E6F7G8H marked as ultimately trusted
gpg: revocation certificate stored as '/home/user/.gnupg/openpgp-revocs.d/1A2B3C4D5E6F7G8H.rev'
public and secret key created and signed.
```

- A new key pair is generated with a 4096-bit RSA algorithm.
- The key does not expire.
- User ID is set to "John Doe (Work Key) <john.doe@example.com>".
- A passphrase is set to protect the private key.

#### Listing GPG Keys

**List Public Keys:**

```bash
gpg --list-keys
```

**Expected Output:**

```
/home/user/.gnupg/pubring.kbx
-----------------------------
pub   rsa4096 2022-01-01 [SC]
      1A2B3C4D5E6F7G8H
uid           [ultimate] John Doe (Work Key) <john.doe@example.com>
```

**List Private Keys:**

```bash
gpg --list-secret-keys
```

**Expected Output:**

```
/home/user/.gnupg/pubring.kbx
-----------------------------
sec   rsa4096 2022-01-01 [SC]
      1A2B3C4D5E6F7G8H
uid           [ultimate] John Doe (Work Key) <john.doe@example.com>
```

**Interpretation:**

- `pub`: Public key information.
- `sec`: Secret (private) key information.
- The key ID is `1A2B3C4D5E6F7G8H`.

#### Importing a Public Key

**Command:**

```bash
gpg --import recipient_public_key.asc
```

**Expected Output:**

```
gpg: key 9H8G7F6E5D4C3B2A: public key "Jane Smith <jane.smith@example.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

**Interpretation:**

- The public key of Jane Smith is imported into your keyring.

#### Trusting an Imported Public Key

**Command:**

```bash
gpg --edit-key jane.smith@example.com
```

**Interactive Session:**

```
gpg> trust
pub  rsa4096/9H8G7F6E5D4C3B2A
      created: 2022-01-01  expires: never       usage: SC  
      trust: unknown       validity: unknown
[ unknown] (1). Jane Smith <jane.smith@example.com>

Please decide how far you trust this user to correctly verify others' keys
(1=I don't know or won't say, 2=I do NOT trust, 3=I trust marginally,
 4=I trust fully, 5=I trust ultimately)
Your decision? 5

Do you really want to set this key to ultimate trust? (y/N) y

gpg> save
```

**Expected Output:**

```
gpg: setting ownertrust to 5
```

**Interpretation:**

- Setting the trust level to "ultimate" indicates you fully trust that this key belongs to Jane Smith.

#### Encrypting a File

**Command:**

```bash
gpg -e -r jane.smith@example.com file.txt
```

**Expected Output:**

*(No output means the command was successful)*

**Interpretation:**

- The file `file.txt` is encrypted using Jane Smith's public key.
- The encrypted file is saved as `file.txt.gpg`.

**Visualization:**

```
[ Original File ]    +-------------+    [ Encrypted File ]
    file.txt   --->  | GPG Encrypt | ---> file.txt.gpg
                   (Recipient: jane.smith@example.com)
```

#### Symmetric Encryption

**Command:**

```bash
gpg --symmetric file.txt
```

**Expected Output:**

```
Enter passphrase: ********
Repeat passphrase: ********
```

**Interpretation:**

- The file `file.txt` is encrypted using a symmetric cipher.
- A passphrase is set for both encryption and decryption.
- The encrypted file is saved as `file.txt.gpg`.

## Decrypting a File

**Command:**

```bash
gpg -d -o file.txt file.txt.gpg
```

**Expected Output (If Passphrase Protected):**

```
gpg: encrypted with 4096-bit RSA key, ID 9H8G7F6E5D4C3B2A, created 2022-01-01
      "Jane Smith <jane.smith@example.com>"
gpg: encrypted with AES256 cipher
```

**Interpretation:**

- The encrypted file `file.txt.gpg` is decrypted.
- The output is saved as `file.txt`.

#### Creating Digital Signatures

**Command:**

```bash
gpg --sign file.txt
```

**Expected Output:**

*(No output means the command was successful)*

**Interpretation:**

- The file `file.txt` is signed with your private key.
- The signed file is saved as `file.txt.gpg`.

**Verification of Signature:**

```bash
gpg --verify file.txt.gpg
```

**Expected Output:**

```
gpg: Signature made Mon 03 Oct 2022 12:00:00 PM UTC
gpg:                using RSA key 1A2B3C4D5E6F7G8H
gpg: Good signature from "John Doe (Work Key) <john.doe@example.com>"
```

**Interpretation:**

- Confirms that the signature is valid and was made by John Doe.

#### Exporting Your Public Key

**Command:**

```bash
gpg --export -a john.doe@example.com > john_public_key.asc
```

**Expected Output:**

*(No output means the command was successful)*

**Interpretation:**

- Your public key is exported in ASCII armor format to `john_public_key.asc`.
- This file can be shared with others.

**Visualization of Key Export:**

```
[ Private Key ]     +-------------+     [ Public Key ]
    (Secure)   ---> | GPG Export  | ---> john_public_key.asc
```

#### Revoking a Key

**Command:**

```bash
gpg --gen-revoke john.doe@example.com
```

**Expected Output:**

```
sec  rsa4096/1A2B3C4D5E6F7G8H 2022-01-01 John Doe (Work Key) <john.doe@example.com>

Create a revocation certificate for this key? (y/N) y
...

Reason for revocation:
  0 = No reason specified
  1 = Key has been compromised
  2 = Key is superseded
  3 = Key is no longer used
  Q = Cancel
(Enter the number corresponding to your choice)> 1

Enter an optional description; end it with an empty line:
> Key compromised due to lost device.
> 
Reason for revocation: Key has been compromised
Key compromised due to lost device.
Is this okay? (y/N) y

Revocation certificate created.

...

```

- A revocation certificate is generated to invalidate your key if compromised.
- Store the certificate securely.

#### Creating an ASCII Armored Public Key

**Command:**

```bash
gpg --armor --export john.doe@example.com > public_key.asc
```

**Expected Output:**

*(No output means the command was successful)*

**Sample Content of `public_key.asc`:**

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBF+...
... (Key Data)
... 
-----END PGP PUBLIC KEY BLOCK-----
```

- The public key is exported in a text-friendly format suitable for email or posting online.

#### Revocation Certificates

**Command:**

```bash
gpg --gen-revoke --armor --output=revoke.asc john.doe@example.com
```

**Expected Output:**

- Similar to the revocation process earlier, but the certificate is saved as `revoke.asc`.

**Interpretation:**

- The revocation certificate is saved in ASCII armor format.

#### Subkeys

**Creating a Subkey:**

```bash
gpg --edit-key john.doe@example.com
```

**Interactive Session:**

```
gpg> addkey
Please select what kind of key you want:
   (4) RSA (sign only)
   (6) RSA (encrypt only)
   (8) RSA (set your own capabilities)
Your selection? 6

RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 2048

Please specify how long the key should be valid.
         0 = key does not expire
Key is valid for? (0) 1y

Is this correct? (y/N) y

Really create? (y/N) y

gpg> save
```

**Expected Output:**

```
gpg: key 1A2B3C4D5E6F7G8H marked as ultimately trusted
gpg: revocation certificate stored as '/home/user/.gnupg/openpgp-revocs.d/1A2B3C4D5E6F7G8H.rev'
```

**Interpretation:**

- A new subkey is added for encryption purposes.
- The subkey has a separate expiration date.

#### Advanced Encryption Options

**Symmetric Encryption:**

```bash
gpg --symmetric file.txt
```

**Specifying an Encryption Algorithm:**

```bash
gpg --cipher-algo AES256 -e file.txt
```

**Expected Output:**

- Files are encrypted using the specified cipher algorithm.

**Interpretation:**

- `AES256` provides strong encryption.
- Use specific algorithms as per security requirements.

### Working with Encrypted Emails

GPG can be integrated with email clients to send and receive encrypted emails.

#### Encrypting an Email

**Command:**

```bash
gpg --armor --encrypt --recipient 'jane.smith@example.com' --output message.asc message.txt
```

**Expected Output:**

*(No output means the command was successful)*

**Interpretation:**

- The file `message.txt` is encrypted for Jane Smith and saved as `message.asc` in ASCII armor format.

#### Decrypting an Email

**Command:**

```bash
gpg --decrypt message.asc > message.txt
```

**Expected Output:**

```
gpg: encrypted with 4096-bit RSA key, ID 9H8G7F6E5D4C3B2A, created 2022-01-01
      "Jane Smith <jane.smith@example.com>"
```

**Interpretation:**

- The encrypted message is decrypted and saved as `message.txt`.

### Key Servers

Key servers allow users to publish and retrieve public keys.

#### Sending Keys to a Key Server

**Command:**

```bash
gpg --send-keys --keyserver hkp://pgp.mit.edu 1A2B3C4D5E6F7G8H
```

**Expected Output:**

```
gpg: sending key 1A2B3C4D5E6F7G8H to hkp://pgp.mit.edu
```

**Interpretation:**

- Your public key is uploaded to the key server.

#### Searching for Keys on a Key Server

**Command:**

```bash
gpg --search-keys --keyserver hkp://pgp.mit.edu jane.smith@example.com
```

**Expected Output:**

```
gpg: data source: http://pgp.mit.edu:11371
(1)     Jane Smith <jane.smith@example.com>
          4096 bit RSA key 9H8G7F6E5D4C3B2A, created: 2022-01-01
Keys 1-1 of 1 for "jane.smith@example.com".  Enter number(s), N)ext, or Q)uit > 1
gpg: key 9H8G7F6E5D4C3B2A: public key "Jane Smith <jane.smith@example.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

**Interpretation:**

- Jane Smith's public key is imported from the key server.

#### Updating Key Information

**Command:**

```bash
gpg --refresh-keys --keyserver hkp://pgp.mit.edu
```

**Expected Output:**

```
gpg: refreshing 1 keys from hkp://pgp.mit.edu
gpg: key 9H8G7F6E5D4C3B2A: "Jane Smith <jane.smith@example.com>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1
```

**Interpretation:**

- Your keyring is updated with the latest key information from the server.

### Disk Encryption

Disk encryption secures data at rest on storage devices.

#### Integration with Disk Encryption Tools

GPG can enhance disk encryption by managing keys for tools like LUKS.

**Visualization of GPG with LUKS:**

```
[ GPG Key ]       [ Encrypted Keyfile ]       [ LUKS Volume ]
     |                    |                          |
     +--> Decrypt Keyfile +--> Unlocks LUKS Volume --+
```

#### Setting up GPG with LUKS

**Step 1: Generate GPG Key Pair (if not already done)**

```bash
gpg --gen-key
```

**Step 2: Create a Random Keyfile**

```bash
dd if=/dev/urandom of=/root/luks-keyfile bs=512 count=4
chmod 600 /root/luks-keyfile
```

**Expected Output:**

```
4+0 records in
4+0 records out
2048 bytes (2.0 kB, 2.0 KiB) copied, 0.000123 s, 16.7 MB/s
```

**Step 3: Encrypt the Keyfile with GPG**

```bash
gpg --encrypt --recipient "John Doe" /root/luks-keyfile
```

**Expected Output:**

```
gpg: /root/luks-keyfile: encryption failed: No public key
```

**If Error Occurs:**

- Ensure you have your own public key in your keyring.
- Alternatively, encrypt for yourself:

```bash
gpg --encrypt --recipient john.doe@example.com /root/luks-keyfile
```

**Step 4: Initialize LUKS Volume with Keyfile**

```bash
cryptsetup luksFormat /dev/sdX /root/luks-keyfile
```

**Expected Output:**

```
WARNING!
========
This will overwrite data on /dev/sdX irrevocably.

Are you sure? (Type uppercase yes): YES
```

**Interpretation:**

- The LUKS volume is formatted using the keyfile.

**Step 5: Decrypt Keyfile and Open LUKS Volume**

```bash
gpg --output /root/luks-keyfile --decrypt /root/luks-keyfile.gpg
cryptsetup luksOpen /dev/sdX my_encrypted_volume --key-file /root/luks-keyfile
```

**Expected Output:**

```
gpg: encrypted with 4096-bit RSA key, ID 1A2B3C4D5E6F7G8H, created 2022-01-01
      "John Doe (Work Key) <john.doe@example.com>"
```

**Interpretation:**

- The keyfile is decrypted and used to unlock the LUKS volume.

**Step 6: Mount the Decrypted Volume**

```bash
mount /dev/mapper/my_encrypted_volume /mnt/my_mount_point
```

**Step 7: Securely Delete the Decrypted Keyfile**

```bash
shred -u /root/luks-keyfile
```

**Interpretation:**

- The decrypted keyfile is securely deleted to prevent unauthorized access.

### Advantages

- Combining GPG with LUKS offers **enhanced** security by providing multiple layers of encryption, ensuring data is protected from unauthorized access.
- The integration of GPG simplifies **key** management, making it easier to revoke or rotate keys without the need to re-encrypt the entire disk.
- Using GPG and LUKS together adds **flexibility**, allowing for the implementation of more complex security policies tailored to different organizational needs.
- This combination supports **multi-user** environments, where different users can have separate encryption keys, maintaining individual security and access controls.
- One of the key benefits of this setup is the ability to **seamlessly** manage multiple encryption keys for various purposes, streamlining administration.
- GPG's ability to **revoke** keys without re-encrypting data adds a level of operational efficiency, reducing the risk and downtime in case of compromised keys.

### Challenges

I. Explore the basic functionalities of GPG by.

- Generating your own public and private GPG key pair.
- Encrypting a plaintext file with the public key you generated.
- Decrypting the resulting file with your private key.
- Confirming the contents of the decrypted file matches the original.

II. Experiment with symmetric encryption

- Try encrypting and decrypting a file using symmetric encryption in GPG.
- Consider the pros and cons of symmetric vs. asymmetric encryption.

III. Explore GPG's use in email communication

- Try to set up an encrypted email communication with another user.
- Experiment with sending, receiving, and verifying encrypted emails.

IV. Delve into key security practices

- Evaluate why sharing a private key is or isn't safe.
- Research the purpose and importance of strong passwords and passphrases for encryption. 
- Reflect on how you would keep your private key secure.

V. Explore the concept of key revocation

- Generate a revocation certificate for your key.
- Contemplate under what circumstances you might need to use this certificate.

VI. Understand the use of key servers

- Try uploading your public key to a key server.
- Download and import someone else's public key from a key server.

VII. Dive into disk encryption

- Research how GPG can be used for disk encryption.
- Understand the steps and tools required to set up disk encryption on a Linux system.

VIII. Understand subkeys and their purpose

- Generate a subkey for your primary key.
- Reflect on the benefits and potential use-cases for using subkeys instead of a primary key.
