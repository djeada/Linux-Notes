## Encryption and GPG

Encryption is one of the main tools used to protect digital information. It keeps data private by changing readable information into an unreadable form. The readable version is called plaintext, and the unreadable version is called ciphertext.

For example, the message:

```text
Hello
```

might be transformed into something unreadable, such as:

```text
6hj7!#f&
```

The unreadable version is only useful to someone who has the correct key or password needed to turn it back into the original message.

### Why Encryption Matters

Encryption protects information when it is stored and when it is sent across a network.

It is used when logging into websites, sending private messages, storing passwords, protecting backups, securing disks, and sending sensitive files. Without encryption, anyone who intercepts or steals the data may be able to read it.

The main goals of encryption are:

```text
Confidentiality  -> Only authorized people can read the data.
Integrity        -> The data has not been changed unexpectedly.
Authentication   -> The sender or owner can be verified.
Compliance       -> Legal or policy requirements can be met.
```

Encryption is especially important when information travels over insecure networks, such as the internet or public Wi-Fi.

### Basic Encryption Process

The basic encryption process looks like this:

```text
[ Plaintext ]       +------------------+       [ Ciphertext ]
  "Hello"    -----> | Encryption       | -----> "6hj7!#f&"
                    | Algorithm + Key  |
                    +------------------+
```

The plaintext is the original readable data. The encryption algorithm is the mathematical process used to transform the data. The key controls how that transformation happens.

Without the correct key, the ciphertext should be extremely difficult to turn back into plaintext.

### Basic Decryption Process

Decryption reverses the process.

```text
[ Ciphertext ]      +------------------+       [ Plaintext ]
  "6hj7!#f&" -----> | Decryption       | -----> "Hello"
                    | Algorithm + Key  |
                    +------------------+
```

The encrypted data is given to the decryption algorithm along with the correct key. If the key is valid, the original plaintext is recovered.

### Symmetric and Asymmetric Encryption

There are two major types of encryption that are important to understand.

Symmetric encryption uses the same secret key for encryption and decryption.

```text
             Same Secret Key
                  |
                  v
[ Plaintext ] -> Encrypt -> [ Ciphertext ] -> Decrypt -> [ Plaintext ]
```

This is simple and fast, but both sides must already know the same secret key. If the key is shared insecurely, the encryption can be broken.

Asymmetric encryption uses a pair of related keys: a public key and a private key.

```text
[ Public Key ]  ---> encrypts data
[ Private Key ] ---> decrypts data
```

The public key can be shared with other people. The private key must be kept secret.

This makes asymmetric encryption useful for secure communication between people who have not already shared a secret password.

### GPG

GPG stands for GNU Privacy Guard. It is a free and open-source tool that implements the OpenPGP standard.

GPG can be used to encrypt files, decrypt files, create digital signatures, verify signatures, manage cryptographic keys, and exchange public keys with other people.

GPG is commonly used for protecting files, sending secure messages, verifying software releases, and managing trusted identities.

### Public and Private Keys

GPG uses key pairs.

A key pair contains:

```text
Public key   -> shared with others
Private key  -> kept secret
```

The public key can safely be shared. Other people use your public key to encrypt files or messages for you. Once something is encrypted with your public key, only your matching private key can decrypt it.

The private key must never be shared. It is used to decrypt data sent to you and to create digital signatures that prove something came from you.

The relationship looks like this:

```text
                 Shared openly
              <---------------->
[ Public Key ]                    [ Private Key ]
  encrypts data                    decrypts data
  verifies signatures              creates signatures
```

Another way to visualize it:

```text
Someone wants to send you a secret file

Their computer:
[ Plain File ] + [ Your Public Key ]
        |
        v
[ Encrypted File ]

Your computer:
[ Encrypted File ] + [ Your Private Key ]
        |
        v
[ Plain File ]
```

The important rule is:

```text
Share your public key.
Protect your private key.
```

### Public Key vs Private Key Responsibilities

- The public key is used for two main things.
- First, it encrypts data. If Jane wants to send John an encrypted file, Jane uses John’s public key.
- Second, it verifies signatures. If John signs a file with his private key, Jane can use John’s public key to verify that the signature is valid.
- The private key is also used for two main things.
- First, it decrypts data that was encrypted with the matching public key.
- Second, it creates digital signatures.
- This means the private key is highly sensitive. If someone steals your private key and knows its passphrase, they may be able to decrypt private data or impersonate you by creating signatures.

### Installing GPG

On Debian or Ubuntu-based systems, GPG can be installed with:

```bash
sudo apt update
sudo apt install gnupg2
```

On many Linux systems, GPG may already be installed.

To check whether it is available, run:

```bash
gpg --version
```

This prints the installed GPG version and supported algorithms.

### Generating a GPG Key Pair

To create a new GPG key pair, run:

```bash
gpg --gen-key
```

GPG will ask a series of questions.

A typical key generation process includes choosing the key type, key size, expiration date, name, email address, optional comment, and passphrase.

Example choices might be:

```text
Key type: RSA and RSA
Key size: 4096 bits
Expiration: 1 year or no expiration
Name: John Doe
Email: john.doe@example.com
Comment: Work Key
```

The user ID might look like this:

```text
John Doe (Work Key) <john.doe@example.com>
```

GPG will also ask for a passphrase. This passphrase protects the private key. Even if someone copies the private key file, they still need the passphrase to use it.

The process looks like this:

```text
gpg --gen-key
      |
      v
Choose key type and size
      |
      v
Set expiration date
      |
      v
Enter name and email
      |
      v
Set passphrase
      |
      v
Public key + private key are created
```

A strong passphrase is important. It should be long, unique, and difficult to guess.

### Key Expiration

- GPG keys can be created with or without an expiration date.
- A key that does not expire may be convenient, but it can be risky if it is forgotten, lost, or compromised.
- A key with an expiration date is often safer because it forces regular review. If the key is still valid and secure, the expiration date can usually be extended.
- For personal learning, a non-expiring key may be simple. For serious use, an expiration date is often better.

### Listing GPG Keys

GPG stores keys in a keyring.

To list public keys in your keyring, run:

```bash
gpg --list-keys
```

Example output:

```text
/home/user/.gnupg/pubring.kbx
-----------------------------
pub   rsa4096 2022-01-01 [SC]
      1A2B3C4D5E6F7G8H
uid           [ultimate] John Doe (Work Key) <john.doe@example.com>
```

To list private keys, run:

```bash
gpg --list-secret-keys
```

Example output:

```text
/home/user/.gnupg/pubring.kbx
-----------------------------
sec   rsa4096 2022-01-01 [SC]
      1A2B3C4D5E6F7G8H
uid           [ultimate] John Doe (Work Key) <john.doe@example.com>
```

The public key list shows keys you can use to encrypt data or verify signatures.

The secret key list shows private keys that belong to you and can be used for decryption or signing.

### Understanding Key Usage Flags

GPG output often includes letters such as:

```text
[S]  signing
[C]  certification
[E]  encryption
[A]  authentication
```

For example:

```text
pub rsa4096 2022-01-01 [SC]
```

means the primary public key can be used for signing and certification.

A subkey might show:

```text
sub rsa4096 2022-01-01 [E]
```

which means that subkey is used for encryption.

These flags help explain what each key is allowed to do.

### Importing a Public Key

To send encrypted data to someone, you need their public key.

If someone gives you a public key file, such as:

```text
recipient_public_key.asc
```

you can import it with:

```bash
gpg --import recipient_public_key.asc
```

Example output:

```text
gpg: key 9H8G7F6E5D4C3B2A: public key "Jane Smith <jane.smith@example.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

After importing the key, it becomes available in your keyring.

You can then use it to encrypt files for that person or verify signatures from that person.

### Checking a Key Fingerprint

Before trusting a public key, you should verify its fingerprint.

A fingerprint is a longer identifier for a key. It is more reliable than a short key ID.

To show a key fingerprint, run:

```bash
gpg --fingerprint jane.smith@example.com
```

You should compare the fingerprint with the owner through a trusted channel, such as in person, a verified website, a secure call, or another reliable method.

This matters because anyone can create a key with someone else’s name and email address. The fingerprint helps confirm that the key really belongs to the person you think it belongs to.

### Trusting an Imported Public Key

After importing someone’s public key, GPG may not automatically trust it.

To edit trust settings, run:

```bash
gpg --edit-key jane.smith@example.com
```

Inside the interactive GPG prompt, type:

```text
trust
```

GPG will ask how much you trust the key owner to verify other keys.

Example options include:

```text
1 = I do not know
2 = I do not trust
3 = I trust marginally
4 = I trust fully
5 = I trust ultimately
```

For example:

```text
Your decision? 5
```

Ultimate trust should usually be used only for your own keys. For other people’s keys, choose a level that matches how carefully you verified the key.

After making changes, type:

```text
save
```

or:

```text
quit
```

depending on what you are doing.

### Encrypting a File for Someone

To encrypt a file for a recipient, you need that recipient’s public key.

Use:

```bash
gpg -e -r jane.smith@example.com file.txt
```

Here:

```text
-e  means encrypt
-r  means recipient
```

This creates an encrypted file, usually named:

```text
file.txt.gpg
```

The process looks like this:

```text
[ Original File ]       +-------------+       [ Encrypted File ]
    file.txt     -----> | GPG Encrypt | -----> file.txt.gpg
                        +-------------+
                         Recipient: Jane
```

Only Jane’s private key can decrypt the file.

If the command succeeds, GPG may produce no output. In many Unix tools, no output often means success.

### Decrypting a File

To decrypt an encrypted file, use:

```bash
gpg -d -o file.txt file.txt.gpg
```

Here:

```text
-d          decrypt
-o file.txt write output to file.txt
```

The process looks like this:

```text
[ Encrypted File ]      +-------------+       [ Original File ]
   file.txt.gpg  -----> | GPG Decrypt | -----> file.txt
                        +-------------+
```

If the file was encrypted with your public key, GPG uses your private key to decrypt it.

If your private key is protected by a passphrase, GPG will ask for that passphrase.

### Symmetric Encryption with GPG

GPG can also use symmetric encryption.

Symmetric encryption uses one shared passphrase instead of a public/private key pair.

To encrypt a file symmetrically, run:

```bash
gpg --symmetric file.txt
```

GPG will ask for a passphrase:

```text
Enter passphrase:
Repeat passphrase:
```

The output file is usually:

```text
file.txt.gpg
```

The process looks like this:

```text
[ file.txt ] + [ passphrase ]
      |
      v
[ file.txt.gpg ]
```

To decrypt it, the recipient must know the same passphrase.

Symmetric encryption is useful when you do not want to manage public keys, but it has one major challenge: the passphrase must be shared safely.

### Asymmetric vs Symmetric Encryption

Asymmetric encryption is better when you want people to send encrypted data to each other without first sharing a password.

Symmetric encryption is simpler and often faster, but both sides must know the same secret.

A simple comparison:

|                  | **Asymmetric encryption**                              | **Symmetric encryption**                    |
| ---------------- | ------------------------------------------------------ | ------------------------------------------- |
| **How it works** | Uses public and private keys                           | Uses one shared password or key             |
| **Key sharing**  | Public key can be shared; private key must stay secret | Same secret encrypts and decrypts           |
| **Common uses**  | Secure communication between different people          | Personal file encryption or shared secrets  |
| **Notes**        | Useful without needing a pre-shared secret             | Requires a safe way to share the passphrase |

### Creating Digital Signatures

Encryption protects confidentiality. Digital signatures protect authenticity and integrity.

A digital signature proves two things:

```text
1. The file was signed by someone who has the private key.
2. The file has not changed since it was signed.
```

To sign a file, run:

```bash
gpg --sign file.txt
```

This creates a signed file, usually:

```text
file.txt.gpg
```

The signing process looks like this:

```text
[ File ] + [ Your Private Key ]
     |
     v
[ Signed File ]
```

Anyone with your public key can verify the signature.

### Verifying a Signature

To verify a signed file, run:

```bash
gpg --verify file.txt.gpg
```

Example output:

```text
gpg: Signature made Mon 03 Oct 2022 12:00:00 PM UTC
gpg:                using RSA key 1A2B3C4D5E6F7G8H
gpg: Good signature from "John Doe (Work Key) <john.doe@example.com>"
```

A good signature means the file matches the signature and the signature was created by the private key matching the public key in your keyring.

However, a good signature does not automatically mean you trust the person. It only means the signature is mathematically valid for that key.

You still need to decide whether the key itself is trustworthy.

### Detached Signatures

Sometimes you may want to keep the original file unchanged and create a separate signature file.

Use:

```bash
gpg --detach-sign file.txt
```

This creates a separate signature file, usually:

```text
file.txt.sig
```

To verify it, use:

```bash
gpg --verify file.txt.sig file.txt
```

Detached signatures are common for software downloads. A project may provide a file and a separate signature so users can verify that the file was not modified.

### Exporting Your Public Key

Other people need your public key if they want to send you encrypted files or verify your signatures.

To export your public key in ASCII-armored format, run:

```bash
gpg --export -a john.doe@example.com > john_public_key.asc
```

The `-a` option means ASCII armor. This creates a text-based version of the key that is easier to share in email, websites, or messages.

The process looks like this:

```text
[ Your Public Key in GPG Keyring ]
              |
              v
       GPG export command
              |
              v
[ john_public_key.asc ]
```

The file may contain text like:

```text
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBF+...
...
-----END PGP PUBLIC KEY BLOCK-----
```

This file can be shared publicly.

### Exporting Your Private Key

Normally, you should not export your private key unless you are making a secure backup or moving it to another trusted device.

To export a private key, the command is:

```bash
gpg --export-secret-keys -a john.doe@example.com > john_private_key.asc
```

This file must be protected carefully.

A private key backup should be stored securely, preferably offline and encrypted.

Never email your private key to yourself or upload it to an insecure cloud location.

### Revoking a Key

If your private key is lost, stolen, compromised, or no longer used, you need a way to tell others not to trust it anymore.

That is what a revocation certificate is for.

To create a revocation certificate, run:

```bash
gpg --gen-revoke john.doe@example.com
```

You can also save an ASCII-armored revocation certificate to a file:

```bash
gpg --gen-revoke --armor --output revoke.asc john.doe@example.com
```

The revocation process looks like this:

```text
Private key compromised or retired
          |
          v
Create or publish revocation certificate
          |
          v
Other users learn the key should no longer be trusted
```

It is a good idea to create a revocation certificate soon after creating a key and store it somewhere safe.

Do not publish the revocation certificate unless you actually want to revoke the key.

### Subkeys

A GPG key can have subkeys.

A primary key is often used for identity and certification. Subkeys can be used for specific tasks such as encryption, signing, or authentication.

This is useful because you can keep the primary key more secure and use subkeys for daily work.

The structure looks like this:

```text
[ Primary Key ]
      |
      +--> [ Signing Subkey ]
      |
      +--> [ Encryption Subkey ]
      |
      +--> [ Authentication Subkey ]
```

If a subkey is compromised, you may be able to revoke or replace only that subkey instead of replacing the entire identity.

To manage subkeys, run:

```bash
gpg --edit-key john.doe@example.com
```

Then inside the GPG prompt:

```text
addkey
```

GPG will ask what kind of subkey you want.

Example:

```text
(4) RSA sign only
(6) RSA encrypt only
(8) RSA set your own capabilities
```

After choosing the type, you can set the size and expiration date.

When finished, type:

```text
save
```

### Advanced Encryption Options

GPG chooses reasonable defaults, but you can also specify options manually.

For symmetric encryption, you can choose a cipher algorithm:

```bash
gpg --cipher-algo AES256 --symmetric file.txt
```

AES256 is a widely used symmetric encryption algorithm.

For public-key encryption, a basic command is:

```bash
gpg --encrypt --recipient jane.smith@example.com file.txt
```

You may also see the shorter form:

```bash
gpg -e -r jane.smith@example.com file.txt
```

In most normal situations, it is better to rely on GPG’s safe defaults unless you have a specific reason to change algorithms.

### Working with Encrypted Email

GPG can be used with email. Some email clients integrate GPG directly, while others require manual encryption and decryption.

The basic idea is:

```text
Write message
      |
      v
Encrypt message with recipient's public key
      |
      v
Send encrypted message
      |
      v
Recipient decrypts with private key
```

## Encrypting an Email Message Manually

Suppose the message is stored in:

```text
message.txt
```

To encrypt it for Jane and save it as an ASCII-armored file, run:

```bash
gpg --armor --encrypt --recipient 'jane.smith@example.com' --output message.asc message.txt
```

Here:

```text
--armor       creates text-based encrypted output
--encrypt     encrypts the file
--recipient   chooses who can decrypt it
--output      chooses the output filename
```

The result is:

```text
message.asc
```

This file can be sent through email or another text-based communication method.

### Decrypting an Encrypted Email Message

To decrypt the message, run:

```bash
gpg --decrypt message.asc > message.txt
```

This decrypts the encrypted content and writes the readable message to:

```text
message.txt
```

If the message was encrypted for your public key, your private key is required to decrypt it.

### Key Servers

Key servers are systems that allow people to publish and find public keys.

If you upload your public key to a key server, other people can search for it and import it.

The general workflow is:

```text
Create public key
      |
      v
Upload public key to key server
      |
      v
Other people search for your key
      |
      v
They import it and use it
```

### Sending a Key to a Key Server

To upload a public key to a key server, use:

```bash
gpg --send-keys --keyserver hkp://pgp.mit.edu 1A2B3C4D5E6F7G8H
```

Example output:

```text
gpg: sending key 1A2B3C4D5E6F7G8H to hkp://pgp.mit.edu
```

This makes your public key available to people who search that key server.

Before uploading a key publicly, remember that public key servers may preserve information for a long time. Do not upload keys with email addresses or identities you do not want publicly associated.

### Searching for Keys on a Key Server

To search for someone’s public key, use:

```bash
gpg --search-keys --keyserver hkp://pgp.mit.edu jane.smith@example.com
```

Example output:

```text
gpg: data source: http://pgp.mit.edu:11371
(1)     Jane Smith <jane.smith@example.com>
          4096 bit RSA key 9H8G7F6E5D4C3B2A, created: 2022-01-01
Keys 1-1 of 1 for "jane.smith@example.com". Enter number(s), N)ext, or Q)uit > 1
gpg: key 9H8G7F6E5D4C3B2A: public key "Jane Smith <jane.smith@example.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

After importing the key, you should still verify the fingerprint before trusting it.

A key server can help you find a key, but it does not automatically prove the key is genuine.

### Refreshing Keys

Keys may change over time. They can expire, be extended, gain new signatures, or be revoked.

To refresh keys from a key server, run:

```bash
gpg --refresh-keys --keyserver hkp://pgp.mit.edu
```

Example output:

```text
gpg: refreshing 1 keys from hkp://pgp.mit.edu
gpg: key 9H8G7F6E5D4C3B2A: "Jane Smith <jane.smith@example.com>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1
```

Refreshing keys helps make sure you are not using outdated or revoked key information.

### Disk Encryption

Disk encryption protects data stored on a hard drive, SSD, USB drive, or other storage device.

If someone steals the physical device, disk encryption helps prevent them from reading the files.

Disk encryption is different from encrypting a single file. Instead of protecting only one file, it can protect an entire partition, disk, or volume.

The basic idea is:

```text
[ Disk Data ] + [ Encryption Key ]
       |
       v
[ Encrypted Disk ]

Without the key, the disk contents are unreadable.
```

On Linux, a common disk encryption system is LUKS, which stands for Linux Unified Key Setup.

### GPG and LUKS Together

- GPG can be used with LUKS to protect a keyfile.
- A keyfile is a file used to unlock an encrypted disk volume.
- Instead of storing the keyfile in plain form, you can encrypt the keyfile with GPG.

The workflow looks like this:

```text
[ GPG Private Key ]
        |
        v
Decrypts
        |
        v
[ Encrypted Keyfile ] -----> [ Plain Keyfile ]
                                      |
                                      v
                              Unlocks LUKS Volume
                                      |
                                      v
                              [ Decrypted Disk Access ]
```

A simpler diagram:

```text
[ GPG Key ]       [ Encrypted Keyfile ]       [ LUKS Volume ]
     |                    |                          |
     +--> Decrypt Keyfile +--> Unlocks Volume ------+
```

This creates multiple layers of protection.

The disk needs the keyfile, and the keyfile is protected by GPG.

### Creating a Random LUKS Keyfile

To create a random keyfile, run:

```bash
dd if=/dev/urandom of=/root/luks-keyfile bs=512 count=4
chmod 600 /root/luks-keyfile
```

The `dd` command creates random data from `/dev/urandom`.

The `chmod 600` command makes the file readable and writable only by its owner.

Example output:

```text
4+0 records in
4+0 records out
2048 bytes copied
```

This keyfile should be protected carefully because it can unlock the encrypted volume.

### Encrypting the Keyfile with GPG

To encrypt the keyfile for yourself, run:

```bash
gpg --encrypt --recipient john.doe@example.com /root/luks-keyfile
```

This creates an encrypted version, usually:

```text
/root/luks-keyfile.gpg
```

If you see an error such as:

```text
gpg: /root/luks-keyfile: encryption failed: No public key
```

it means GPG could not find the public key for the recipient.

Check that the key exists:

```bash
gpg --list-keys
```

Then use the correct email address or key ID.

### Initializing a LUKS Volume with a Keyfile

To format a device as a LUKS encrypted volume using the keyfile, run:

```bash
cryptsetup luksFormat /dev/sdX /root/luks-keyfile
```

Be extremely careful with `/dev/sdX`.

This is only a placeholder. You must replace it with the correct device name.

Formatting the wrong device can destroy data.

GPG/LUKS setup should be tested in a safe lab environment before being used on important systems.

A warning may appear:

```text
WARNING!
========
This will overwrite data on /dev/sdX irrevocably.

Are you sure? (Type uppercase yes): YES
```

This warning means the data on that device will be overwritten.

### Decrypting the Keyfile and Opening the LUKS Volume

To decrypt the keyfile:

```bash
gpg --output /root/luks-keyfile --decrypt /root/luks-keyfile.gpg
```

Then use it to open the LUKS volume:

```bash
cryptsetup luksOpen /dev/sdX my_encrypted_volume --key-file /root/luks-keyfile
```

This creates a mapped decrypted device, usually under:

```text
/dev/mapper/my_encrypted_volume
```

The flow is:

```text
Decrypt keyfile
      |
      v
Use keyfile with cryptsetup
      |
      v
Open encrypted LUKS volume
      |
      v
Access mapped device
```

### Mounting the Decrypted Volume

After opening the LUKS volume, mount it:

```bash
mount /dev/mapper/my_encrypted_volume /mnt/my_mount_point
```

This makes the decrypted filesystem accessible at:

```text
/mnt/my_mount_point
```

The mount point must exist first. If it does not exist, create it with:

```bash
mkdir -p /mnt/my_mount_point
```

### Securely Deleting the Decrypted Keyfile

After unlocking the volume, the decrypted keyfile should not be left sitting on disk.

To securely delete it, run:

```bash
shred -u /root/luks-keyfile
```

The `shred` command overwrites the file before deleting it.

The `-u` option removes the file after overwriting.

This helps reduce the risk of someone recovering the keyfile later.

### Advantages of Combining GPG with LUKS

- Using GPG with LUKS can provide stronger key management.
- The LUKS volume protects the disk data. GPG protects the keyfile used to unlock the volume.
- This approach can be useful when managing encrypted storage, especially in situations where keyfiles need to be backed up, transferred, or protected separately.

Some advantages include:

```text
Extra protection for disk unlock keys
Better key management
Support for multiple users or recipients
Ability to revoke or rotate GPG keys
Separation between disk encryption and key protection
```

However, this setup is more complex than using a normal LUKS passphrase. More complexity can also create more chances for mistakes.

### Security Best Practices

- Keep your private key private. Never share it with anyone.
- Use a strong passphrase for your private key. A short or reused passphrase weakens the protection.
- Create a revocation certificate and store it somewhere safe.
- Back up your keys securely. If you lose your private key, you may lose access to encrypted data.
- Verify public key fingerprints before trusting keys.
- Do not assume a key is genuine just because it came from a key server.
- Use expiration dates for important keys.
- Be careful when running disk encryption commands. A wrong device name can erase data.
- Test complex encryption workflows in a virtual machine or lab environment before using them on real data.

### Common GPG Commands

Generate a new key:

```bash
gpg --gen-key
```

List public keys:

```bash
gpg --list-keys
```

List private keys:

```bash
gpg --list-secret-keys
```

Import a public key:

```bash
gpg --import recipient_public_key.asc
```

Export your public key:

```bash
gpg --export -a john.doe@example.com > john_public_key.asc
```

Encrypt a file for someone:

```bash
gpg -e -r jane.smith@example.com file.txt
```

Decrypt a file:

```bash
gpg -d -o file.txt file.txt.gpg
```

Encrypt a file symmetrically:

```bash
gpg --symmetric file.txt
```

Sign a file:

```bash
gpg --sign file.txt
```

Create a detached signature:

```bash
gpg --detach-sign file.txt
```

Verify a signature:

```bash
gpg --verify file.txt.gpg
```

Generate a revocation certificate:

```bash
gpg --gen-revoke john.doe@example.com
```

Edit a key:

```bash
gpg --edit-key john.doe@example.com
```

Search for keys on a key server:

```bash
gpg --search-keys --keyserver hkp://pgp.mit.edu jane.smith@example.com
```

Refresh keys:

```bash
gpg --refresh-keys --keyserver hkp://pgp.mit.edu
```

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
