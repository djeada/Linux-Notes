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

**Example Output:**

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

To manage GPG keys, you can list both public and private keys stored in your keyring. Public keys represent the keys of others that you've imported, while private keys are your own, used for decrypting messages and signing data. Listing public keys helps you verify which keys are available for encrypting files or verifying signatures. Similarly, listing secret (private) keys allows you to ensure your personal encryption keys are correctly stored and accessible.

**List Public Keys:**

```bash
gpg --list-keys
```

**Example Output:**

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

**Example Output:**

```
/home/user/.gnupg/pubring.kbx
-----------------------------
sec   rsa4096 2022-01-01 [SC]
      1A2B3C4D5E6F7G8H
uid           [ultimate] John Doe (Work Key) <john.doe@example.com>
```

#### Importing a Public Key

When communicating securely with someone, you need their public key to encrypt files for them or verify their signatures. The `gpg --import` command allows you to import a public key from a file, adding it to your keyring so that you can use it for encryption or verification purposes.

```bash
gpg --import recipient_public_key.asc
```

**Example Output:**

```
gpg: key 9H8G7F6E5D4C3B2A: public key "Jane Smith <jane.smith@example.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

#### Trusting an Imported Public Key

After importing a public key, you may want to specify how much you trust the key owner to verify others' identities. This process ensures that when you receive files or signatures from the key owner, you can trust their authenticity. The `gpg --edit-key` command allows you to interactively set the trust level for a specific key, providing options from "do not trust" to "ultimate trust," depending on your confidence in the key owner.

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
```

#### Encrypting a File

To protect sensitive information, you can encrypt files using GPG. When encrypting for a specific recipient, their public key is required. The command `gpg -e -r` encrypts the specified file so that only the recipient (who possesses the corresponding private key) can decrypt it. No output indicates success, and the encrypted file is saved with a `.gpg` extension.

```bash
gpg -e -r jane.smith@example.com file.txt
```

**Example Output:**

*(No output means the command was successful)*

**Visualization:**

```
[ Original File ]    +-------------+    [ Encrypted File ]
    file.txt   --->  | GPG Encrypt | ---> file.txt.gpg
                     +-------------+
                   (Recipient: jane.smith@example.com)
```

#### Symmetric Encryption

For cases where both parties share a secret password instead of using public-key cryptography, you can encrypt files using symmetric encryption. The command `gpg --symmetric` encrypts a file using a passphrase that you set. Both encryption and decryption of the file will require the same passphrase.

```bash
gpg --symmetric file.txt
```

**Example Output:**

```
Enter passphrase: ********
Repeat passphrase: ********
```

#### Decrypting a File

Once a file has been encrypted (either with a public key or using symmetric encryption), you can decrypt it using the `gpg -d` command. If the file was encrypted with a public key, you’ll need the corresponding private key. If the file was symmetrically encrypted, you’ll need the correct passphrase.

```bash
gpg -d -o file.txt file.txt.gpg
```

**Example Output (If Passphrase Protected):**

```
gpg: encrypted with 4096-bit RSA key, ID 9H8G7F6E5D4C3B2A, created 2022-01-01
      "Jane Smith <jane.smith@example.com>"
gpg: encrypted with AES256 cipher
```

#### Creating Digital Signatures

Digital signatures ensure that the recipient of a file can verify its authenticity and that it hasn’t been altered. By using the `gpg --sign` command, you can sign a file with your private key, creating a signature that others can verify using your public key.

```bash
gpg --sign file.txt
```

**Example Output:**

*(No output means the command was successful)*

#### Verifying a Signature

After receiving a signed file, you can verify the authenticity of the signature using the `gpg --verify` command. This process checks the signature against the sender's public key, confirming whether the file has been tampered with and verifying the identity of the signer.

```bash
gpg --verify file.txt.gpg
```

**Example Output:**

```
gpg: Signature made Mon 03 Oct 2022 12:00:00 PM UTC
gpg:                using RSA key 1A2B3C4D5E6F7G8H
gpg: Good signature from "John Doe (Work Key) <john.doe@example.com>"
```

#### Exporting Your Public Key

When someone wants to send you an encrypted file or verify your digital signature, they’ll need your public key. The `gpg --export` command allows you to export your public key to a file, which can then be shared with others. The `-a` option ensures the key is exported in a text-readable format (ASCII armor).

```bash
gpg --export -a john.doe@example.com > john_public_key.asc
```

**Example Output:**

*(No output means the command was successful)*

**Visualization of Key Export:**

```bash
[ Private Key ]     +-------------+     [ Public Key ]
    (Secure)   ---> | GPG Export  | ---> john_public_key.asc
                    +-------------+
```

#### Revoking a Key

If your private key is ever compromised, lost, or you no longer use it, it’s essential to generate a revocation certificate. This certificate informs others that the key should no longer be trusted. The `gpg --gen-revoke` command guides you through the process of creating a revocation certificate, which you should store securely and distribute only if needed.

```bash
gpg --gen-revoke john.doe@example.com
```

**Example Output:**

```
sec  rsa4096/1A2B3C4D5E6F7G8H 2022-01-01 John Doe (Work Key) <john.doe@example.com>

Create a revocation certificate for this key? (y/N) y
...
```

#### Creating an ASCII Armored Public Key

When you need to share your public key in a human-readable format (such as for emails or posting on a website), you can use ASCII armor. The `gpg --armor --export` command converts your public key into an ASCII-encoded format, making it easier to share in text-based mediums. This command outputs the public key into a file (`public_key.asc`) which contains the key data in a format that begins and ends with `-----BEGIN PGP PUBLIC KEY BLOCK-----` and `-----END PGP PUBLIC KEY BLOCK-----`, respectively.

```bash
gpg --armor --export john.doe@example.com > public_key.asc
```

**Example Output:**

*(No output means the command was successful)*

**Sample Content of `public_key.asc`:**

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBF+...
... (Key Data)
... 
-----END PGP PUBLIC KEY BLOCK-----
```

#### Revocation Certificates

If your private key is compromised or lost, it’s crucial to have a revocation certificate ready. The `gpg --gen-revoke` command creates this certificate, allowing you to inform others that the key should no longer be trusted. By adding the `--armor` option, the certificate is saved in an ASCII-encoded format, making it easy to share via email or other text-based methods. This is useful in scenarios where you need to distribute the revocation certificate if your key is no longer secure.

```bash
gpg --gen-revoke --armor --output=revoke.asc john.doe@example.com
```

**Example Output:**

*(No output means the command was successful)*

The revocation certificate is saved in `revoke.asc` and is ready to be shared or used if needed.

#### Subkeys

Subkeys are additional keys associated with your main key that can be used for specific tasks like encryption or signing, providing flexibility in key management. The `gpg --edit-key` command opens an interactive session where you can manage keys, including creating subkeys. In this process, you can choose the purpose of the subkey (e.g., for encryption only), set its size, and define its expiration date. This makes it easier to manage different aspects of key usage while ensuring that your main key remains secure.

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

**Example Output:**

```
gpg: key 1A2B3C4D5E6F7G8H marked as ultimately trusted
gpg: revocation certificate stored as '/home/user/.gnupg/openpgp-revocs.d/1A2B3C4D5E6F7G8H.rev'
```

A new subkey has been added with specific capabilities (e.g., encryption only) and a custom expiration date.

#### Advanced Encryption Options

GPG allows you to specify the encryption algorithm you want to use for encrypting files. By default, it uses a strong encryption algorithm, but you can customize it based on your security requirements. The `gpg --symmetric` command encrypts a file using a passphrase, while the `gpg --cipher-algo` option allows you to specify a particular cipher, like AES256, which is known for its strong security.

**Symmetric Encryption:**

```bash
gpg --symmetric file.txt
```

**Specifying an Encryption Algorithm:**

```bash
gpg --cipher-algo AES256 -e file.txt
```

**Example Output:**

*(No output means the command was successful)*

The file `file.txt` is encrypted using AES256, a secure encryption algorithm. You can adjust the algorithm based on your needs.

#### Working with Encrypted Emails

GPG can be integrated with email clients or used directly to send and receive encrypted messages. Encrypting an email involves converting the email content into an encrypted format that can only be read by the intended recipient. By using the `--armor` option, you ensure the encrypted email content is saved in ASCII format, suitable for sending via email. The recipient can then decrypt the email using their private key.

#### Encrypting an Email

When encrypting an email message, you can use GPG to ensure that only the intended recipient can read it. The command `gpg --armor --encrypt` takes the message file and encrypts it for the recipient, saving the output in an ASCII-armored file (`message.asc`). This file can then be safely sent over email or other communication methods.

```bash
gpg --armor --encrypt --recipient 'jane.smith@example.com' --output message.asc message.txt
```

**Example Output:**

*(No output means the command was successful)*

The email content in `message.txt` is encrypted for Jane Smith and saved as `message.asc`, making it safe to send electronically.

#### Decrypting an Email

To read an encrypted email, the recipient must decrypt it using their private key. The `gpg --decrypt` command allows you to decrypt the encrypted file (e.g., `message.asc`), saving the content back into a readable text file.

```bash
gpg --decrypt message.asc > message.txt
```

**Example Output:**

```
gpg: encrypted with 4096-bit RSA key, ID 9H8G7F6E5D4C3B2A, created 2022-01-01
      "Jane Smith <jane.smith@example.com>"
```

The encrypted message from `message.asc` is decrypted and saved as `message.txt`, allowing the recipient to read the original content.

### Key Servers

Key servers provide a platform for users to publish and retrieve public keys, enabling secure communication and file sharing across different systems and users. By sending your public key to a key server, you make it easily accessible to others, while searching for and importing keys allows you to securely exchange encrypted data with new contacts. Key servers are a critical part of the public-key infrastructure (PKI), helping users find and trust public keys for encryption and digital signatures.

#### Sending Keys to a Key Server

When you want to make your public key available for others to find and use, you can upload it to a public key server. The command `gpg --send-keys` sends your key to the specified key server, allowing others to retrieve it and use it to encrypt data for you or verify your digital signatures. This is useful for establishing secure communications or making your public key widely available.

```bash
gpg --send-keys --keyserver hkp://pgp.mit.edu 1A2B3C4D5E6F7G8H
```

**Example Output:**

```
gpg: sending key 1A2B3C4D5E6F7G8H to hkp://pgp.mit.edu
```

Your public key, identified by the key ID `1A2B3C4D5E6F7G8H`, has been successfully uploaded to the key server at `pgp.mit.edu`. Now, anyone can search for and download your public key from that server.

#### Searching for Keys on a Key Server

To communicate securely with someone, you need their public key. The `gpg --search-keys` command allows you to look up public keys by email address or name on a specific key server. Once found, you can import the key into your keyring for encryption or verification. This process ensures that you have the correct public key before sending encrypted messages.

```bash
gpg --search-keys --keyserver hkp://pgp.mit.edu jane.smith@example.com
```

**Example Output:**

```
gpg: data source: http://pgp.mit.edu:11371
(1)     Jane Smith <jane.smith@example.com>
          4096 bit RSA key 9H8G7F6E5D4C3B2A, created: 2022-01-01
Keys 1-1 of 1 for "jane.smith@example.com".  Enter number(s), N)ext, or Q)uit > 1
gpg: key 9H8G7F6E5D4C3B2A: public key "Jane Smith <jane.smith@example.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

This output shows that a public key for "Jane Smith" has been found on the key server and successfully imported into your keyring. You can now use this key to encrypt files for her or verify her signatures.

#### Updating Key Information

Over time, the public keys stored on your keyring may be updated with new expiration dates, revocation information, or additional signatures. The `gpg --refresh-keys` command checks the key server for updated information and refreshes the keys in your local keyring. This ensures that you are always working with the latest key information, reducing the risk of using outdated or compromised keys.

```bash
gpg --refresh-keys --keyserver hkp://pgp.mit.edu
```

**Example Output:**

```
gpg: refreshing 1 keys from hkp://pgp.mit.edu
gpg: key 9H8G7F6E5D4C3B2A: "Jane Smith <jane.smith@example.com>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1
```

This output indicates that the keyring was successfully refreshed, but Jane Smith's key did not require any updates. If any keys had been updated, GPG would show the changes, ensuring that you are using the most current versions of your contacts' keys.

### Disk Encryption

Disk encryption protects sensitive data stored on hard drives, SSDs, or other storage devices by converting it into unreadable ciphertext. Even if the physical drive is stolen, encrypted data cannot be accessed without the correct decryption key. GPG can be used to manage encryption keys for disk encryption tools such as LUKS (Linux Unified Key Setup), ensuring that keys are securely stored and protected.

#### Integration with Disk Encryption Tools

GPG can work alongside tools like LUKS to enhance security in managing encrypted volumes. By using GPG to encrypt the keyfile required to unlock a LUKS volume, you add an additional layer of security. The workflow typically involves decrypting the keyfile using GPG, which in turn is used to unlock the encrypted disk volume.

**Visualization of GPG with LUKS:**

```
[ GPG Key ]       [ Encrypted Keyfile ]       [ LUKS Volume ]
     |                    |                          |
     +--> Decrypt Keyfile +--> Unlocks LUKS Volume --+
```

- The GPG key involves using your **private** key to decrypt the keyfile, which is necessary for unlocking the LUKS volume.
- An **encrypted** keyfile is used to unlock the LUKS volume, and it is securely encrypted with your GPG key to prevent unauthorized access.
- A LUKS volume is a disk that is **encrypted** using LUKS, with access only granted when the decrypted keyfile, provided by the GPG key, is available.
- The **private** GPG key plays a critical role in maintaining security, as it is required to decrypt the keyfile before unlocking the LUKS volume.
- Once the keyfile is **decrypted**, it acts as the input to unlock the LUKS volume, providing secure access to the disk’s contents.
- LUKS encryption ensures that the disk remains **inaccessible** without the decrypted keyfile, enhancing the overall security of the storage medium.

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

**Example Output:**

```
4+0 records in
4+0 records out
2048 bytes (2.0 kB, 2.0 KiB) copied, 0.000123 s, 16.7 MB/s
```

**Step 3: Encrypt the Keyfile with GPG**

```bash
gpg --encrypt --recipient "John Doe" /root/luks-keyfile
```

**Example Output:**

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

**Example Output:**

```
WARNING!
========
This will overwrite data on /dev/sdX irrevocably.

Are you sure? (Type uppercase yes): YES
```

The LUKS volume is formatted using the keyfile.

**Step 5: Decrypt Keyfile and Open LUKS Volume**

```bash
gpg --output /root/luks-keyfile --decrypt /root/luks-keyfile.gpg
cryptsetup luksOpen /dev/sdX my_encrypted_volume --key-file /root/luks-keyfile
```

**Example Output:**

```
gpg: encrypted with 4096-bit RSA key, ID 1A2B3C4D5E6F7G8H, created 2022-01-01
      "John Doe (Work Key) <john.doe@example.com>"
```

The keyfile is decrypted and used to unlock the LUKS volume.

**Step 6: Mount the Decrypted Volume**

```bash
mount /dev/mapper/my_encrypted_volume /mnt/my_mount_point
```

**Step 7: Securely Delete the Decrypted Keyfile**

```bash
shred -u /root/luks-keyfile
```

The decrypted keyfile is securely deleted to prevent unauthorized access.

#### Advantages

- Combining GPG with LUKS offers **enhanced** security by providing multiple layers of encryption, ensuring data is protected from unauthorized access.
- The integration of GPG simplifies **key** management, making it easier to revoke or rotate keys without the need to re-encrypt the entire disk.
- Using GPG and LUKS together adds **flexibility**, allowing for the implementation of more complex security policies tailored to different organizational needs.
- This combination supports **multi-user** environments, where different users can have separate encryption keys, maintaining individual security and access controls.
- One of the key benefits of this setup is the ability to **seamlessly** manage multiple encryption keys for various purposes, streamlining administration.
- GPG's ability to **revoke** keys without re-encrypting data adds a level of operational efficiency, reducing the risk and downtime in case of compromised keys.

### Challenges

1. Generate your own public and private GPG key pair and use the public key to encrypt a plaintext file. Then, decrypt the file using your private key and verify that the contents match the original. Discuss the fundamentals of asymmetric encryption and why the public-private key pairing is secure.
2. Encrypt and decrypt a file using symmetric encryption with GPG, experimenting with different passphrases. Compare and contrast the security, speed, and use cases of symmetric versus asymmetric encryption, discussing when each method is appropriate.
3. Set up an encrypted email communication with another student using GPG. Send and receive encrypted messages, and practice verifying the signatures on received emails. Explain the role of encryption in email security and how it protects against eavesdropping.
4. Reflect on key security practices by evaluating why sharing a private key compromises security. Research the purpose of strong passwords and passphrases for encryption and write a brief strategy for keeping your private key secure on different devices.
5. Generate a revocation certificate for your GPG key and explain when and why you might need to use it. Discuss the process and implications of key revocation, as well as the potential impact on your digital communication.
6. Upload your public key to a key server and download someone else’s public key from the server. Practice verifying the downloaded key's authenticity and reflect on the role of key servers in facilitating secure communication with others.
7. Explore disk encryption by researching how it works in GPG and other tools available on Linux for full-disk encryption. Set up a basic encrypted volume on a Linux system, then mount and unmount it while discussing the security advantages and limitations of disk encryption.
8. Generate a subkey from your primary GPG key and experiment with encrypting a file using the subkey. Reflect on the purpose of subkeys, including why they are beneficial and how they can enhance security by limiting exposure of the primary key.
9. Use GPG to create and sign a message digitally, then verify the signature as another user might. Discuss how digital signatures provide message integrity and non-repudiation, and explain the process of verifying signatures with the sender’s public key.
10. Research advanced encryption algorithms like AES and RSA, explaining how they differ in terms of key length, security, and typical applications. Use GPG or other encryption tools to experiment with different algorithms, noting any differences in performance or encryption speed.
