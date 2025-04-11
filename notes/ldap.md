# LDAP (Lightweight Directory Access Protocol)

LDAP is a protocol used to access and manage directory information over an IP network. It is open, vendor-neutral, and an industry standard. LDAP is commonly used for centralized authentication, where user credentials and permissions are managed in a single directory and applied across multiple systems and applications.

TODO:
- explain clearer client and server setup, also completely local setup
- tests
- more on auth

## Understanding LDAP Concepts

### Directory

- A directory functions similarly to a **database**, but it is designed primarily for reading, browsing, and searching information instead of performing frequent, transaction-oriented tasks.
- It is optimized for **attribute-based storage**, meaning it holds descriptive information about objects, allowing for advanced filtering and querying capabilities.
- The directory's **purpose** is to securely store information like user credentials, permissions, and organizational data that can be easily retrieved and managed.
- It employs a **hierarchical structure** akin to a tree, which facilitates an organized, layered approach to data storage and retrieval.

### Entries and Attributes

- An entry represents a **unique object** within the directory, such as a user, a group, or a device, each serving as an individual record in the hierarchy.
- Entries are characterized by **attributes**, which are key-value pairs that provide descriptive information about the entry, such as the name, email, or password of a user.
- Attributes allow for **detailed descriptions** of each entry, making it easier to perform specific searches and retrieve particular information as needed.

### Distinguished Names (DN)

- A Distinguished Name (DN) **uniquely identifies** an entry within the LDAP directory, providing a specific address for each object in the directory tree.
- The DN is structured as a **string of key-value pairs**, with each pair separated by commas, creating a clear and readable format.
- It consists of **components** like the user identifier (uid), organizational unit (ou), and domain components (dc), each specifying different levels of the directory hierarchy.
- For instance, the DN `uid=jdoe,ou=users,dc=example,dc=com` represents a **specific entry** under the "users" organizational unit in the "example.com" domain.

| Component                | Description                                    |
|--------------------------|------------------------------------------------|
| `uid=jdoe`               | User ID                                        |
| `ou=users`               | Organizational Unit                            |
| `dc=example,dc=com`      | Domain Components representing `example.com`   |

### Schema

- A schema establishes the **structure** of the directory, defining the rules and organization for all entries and their attributes.
- It includes **object classes**, which specify the types of entries permitted in the directory, such as "person" or "organizationalUnit."
- Each object class has a defined set of **attributes** that determine what information is allowed or required, ensuring consistency in how data is stored.
- The schema also enforces **syntax rules**, which dictate the data types and constraints for attributes, helping maintain data integrity and consistency across the directory.

### Network Topology Diagram

The network topology illustrates how the LDAP server interacts with multiple client hosts across the network.

```
                 +--------------------+
                 |    LDAP Server     |
                 | (ldap.example.com) |
                 +----------+---------+
                            |
             ---------------------------------
             |               |               |
     +-------+-----+   +-----+-------+   +---+-------+
     |             |   |             |   |           |
+------v------+ +----v-----+     +-----v----+     +----v-----+
| Client Host | | Client   |     | Client   |     | Client   |
|    (Web)    | | Host     |     | Host     |     | Host     |
|             | | (Email)  |     | (SSH)    |     | (FTP)    |
+-------------+ +----------+     +----------+     +----------+
```

- An LDAP server acts as a **centralized directory service**, where user credentials, permissions, and other organizational data are securely stored and managed.
- Client hosts include **systems and applications** such as web servers, email servers, SSH servers, and FTP servers, which rely on the LDAP server to authenticate users and grant appropriate access.
- By connecting to the LDAP server, these client hosts can **authenticate users** consistently, ensuring that access control is centralized and streamlined across various services and platforms.

## LDAP Directory Structure

LDAP directories are organized hierarchically in a structure known as the **Directory Information Tree (DIT)**.

**Visual Representation of a DIT**:

```
                    (Root)
                      |
           +----------+----------+
           |                     |
        dc=com                 dc=org
           |                     |
     +-----+-----+               |
     |           |               |
  dc=example   dc=company       ...
     |
 +---+---+
 |       |
ou=users ou=groups
 |         |
 |         +----------------+
 |                          |
+--+--+                   +---+---+
|     |                   |       |
uid=alice uid=bob       cn=admins cn=users
```

- The **dc** (Domain Component) represents parts of a domain name, allowing LDAP entries to reflect the domain structure; for example, `dc=example,dc=com` corresponds to the domain `example.com`.
- The **ou** (Organizational Unit) groups entries logically, so you might have entries like `ou=users` for user accounts or `ou=groups` for different group classifications.
- The **uid** (User Identifier) is used to represent individual user entries, such as `uid=alice` for a user named Alice.
- The **cn** (Common Name) typically names entries, like groups, with a descriptive label, such as `cn=admins` for an administrators group.

### User Authentication Sequence Diagram

```
User                Client Host             LDAP Server
|                       |                      |
|---Login Request------>|                      |
|                       |---Authenticate------>|
|                       |                      |
|                       |<--Authentication-----|
|<--Access Granted------|                      |
```

1. **User** sends login request to **Client Host**.
2. **Client Host** sends authentication request to **LDAP Server**.
3. **LDAP Server** processes the request and sends back the authentication result.
4. **Client Host** grants or denies access to the **User** based on the result.

### Common LDAP Operations

LDAP defines a set of operations that clients can perform on the directory.

#### Bind

- The purpose of the **bind** operation is to authenticate the client and specify the version of the LDAP protocol being used.
- This operation is used to initiate a session between the client and the LDAP server, allowing further communication and requests to proceed securely.

**Example Command**:

```bash
ldapwhoami -x -D "uid=jdoe,ou=users,dc=example,dc=com" -W
```

Options:

| Option | Description                                |
|--------|--------------------------------------------|
| `-x`   | Use simple authentication.                 |
| `-D`   | Bind DN (the user's distinguished name).   |
| `-W`   | Prompt for the password.                   |

**Expected Output**:

```
Enter LDAP Password:
dn:uid=jdoe,ou=users,dc=example,dc=com
```

#### Search & Compare

- The **search** operation is used to retrieve directory entries that match specific criteria, allowing clients to find and access particular information within the LDAP directory.
- The **compare** operation checks whether a specified attribute of an entry contains a certain value, helping to verify data or confirm user details.

**Example Search Command**:

```bash
ldapsearch -x -b "dc=example,dc=com" "(uid=jdoe)"
```

| Option           | Description                  |
|------------------|------------------------------|
| `-x`             | Use simple authentication.   |
| `-b`             | Base DN to search.           |
| `"(uid=jdoe)"`   | Search filter.               |

**Expected Output**:

```
# extended LDIF
#
# LDAPv3
# base <dc=example,dc=com> with scope subtree
# filter: (uid=jdoe)
# requesting: ALL
#

# jdoe, users, example.com
dn: uid=jdoe,ou=users,dc=example,dc=com
uid: jdoe
cn: John Doe
sn: Doe
mail: jdoe@example.com
...

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

#### Add, Delete & Modify

- The **add** operation is used to create new entries within the LDAP directory, enabling the addition of users, groups, or other objects.
- The **delete** operation removes entries from the directory, allowing for the cleanup or deactivation of outdated or unnecessary records.
- The **modify** operation updates existing entries, facilitating changes to attributes or values as needed to keep directory information current.

**Example Add Command**:

```bash
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f new_user.ldif
```

**Example Delete Command**:

```bash
ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "uid=jdoe,ou=users,dc=example,dc=com"
```

#### Unbind

- The purpose of the **unbind** operation is to terminate the LDAP session, signaling the end of communication between the client and the server.
- This operation is used either automatically after completing necessary actions or explicitly by the client to close the connection when it is no longer needed.

### LDAP Search Filters

Search filters control what entries are returned in a search operation.

**Syntax**:

- `(attribute=value)`: Equality match.
- `(&(filter1)(filter2))`: AND operation.
- `(|(filter1)(filter2))`: OR operation.
- `(!(filter))`: NOT operation.

**Examples**:

**Find users with uid 'jdoe'**:

```
(uid=jdoe)
```

**Find entries that are persons and have an email**:

```
(&(objectClass=person)(mail=*))
```

**Find users not in the 'admins' group**:

```
(!(memberOf=cn=admins,ou=groups,dc=example,dc=com))
```

### LDAP Tools and Utilities

#### Command-Line Tools

1. **ldapsearch**: Search for entries.


```bash
ldapsearch -x -b "dc=example,dc=com" "(objectClass=*)"
```

2. **ldapadd/ldapmodify**: Add or modify entries.

```bash
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f entry.ldif
```

3. **ldapdelete**: Delete entries.

```bash
ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "uid=jdoe,ou=users,dc=example,dc=com"
```

4. **ldapwhoami**: Display the DN bound to the session.

```bash
ldapwhoami -x -D "uid=jdoe,ou=users,dc=example,dc=com" -W
```

#### GUI-Based Tools

1. **Apache Directory Studio** is an Eclipse-based LDAP browser and editor, offering a user-friendly interface for browsing and managing LDAP directories.
2. **phpLDAPadmin** serves as a web-based LDAP administration tool, allowing administrators to manage directory entries through a convenient browser interface.
3. **JXplorer** is a Java-based LDAP client, providing cross-platform support for accessing and managing LDAP directories with various customization options.

### Implementing LDAP for Centralized Authentication

Centralized authentication via LDAP allows multiple servers and applications to use a single directory for user authentication and authorization.

Prerequisites:

- An **operating system** like Ubuntu Server 20.04 LTS (or a similar Linux distribution) is needed as the platform for hosting the LDAP server.
- **Root or sudo access** is essential for performing the installation and configuration steps, allowing you to manage system-level changes securely.
- Proper **network configuration** is required to ensure that the LDAP server and client systems can communicate effectively over the network, enabling reliable access and authentication.

### Step-by-Step Guide

#### 1. Install and Configure the LDAP Server

**Install OpenLDAP and Utilities**:

```bash
sudo apt-get update
sudo apt-get install slapd ldap-utils
```

**Configure slapd**:

During installation, you may not be prompted for configuration. Run the following to reconfigure:

```bash
sudo dpkg-reconfigure slapd
```

**Configuration Prompts**:

| Setting                                        | Value                     |
|------------------------------------------------|---------------------------|
| Omit OpenLDAP server configuration?            | No                        |
| DNS domain name                                | `example.com`             |
| Organization name                              | `Example Company`         |
| Administrator password                         | `[Set a strong password]` |
| Database backend                               | `MDB`                     |
| Remove the database when slapd is purged?      | No                        |
| Move old database?                             | Yes                       |

#### 2. Define the Directory Structure (Schema)

**Create Base LDIF File (`base.ldif`)**:

```ldif
dn: dc=example,dc=com
objectClass: top
objectClass: dcObject
objectClass: organization
o: Example Company
dc: example

dn: ou=users,dc=example,dc=com
objectClass: top
objectClass: organizationalUnit
ou: users

dn: ou=groups,dc=example,dc=com
objectClass: top
objectClass: organizationalUnit
ou: groups
```

**Load the Schema into LDAP**:

```bash
sudo ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f base.ldif
```

**Expected Output**:

```
adding new entry "dc=example,dc=com"

adding new entry "ou=users,dc=example,dc=com"

adding new entry "ou=groups,dc=example,dc=com"
```

#### 3. Add Users to the Directory

**Create User LDIF File (`user.ldif`)**:

```ldif
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
uid: jdoe
cn: John Doe
sn: Doe
givenName: John
mail: jdoe@example.com
userPassword: {SSHA}encrypted_password_here
```

**Note**: Use `slappasswd` to generate an encrypted password.

```bash
slappasswd
```

| Step                | Action                   |
|---------------------|--------------------------|
| Enter Password      | `[Type password]`        |
| Re-enter Password   | `[Retype password]`      |
| Output              | `{SSHA}encrypted_password_here` |

**Load the User into LDAP**:

```bash
sudo ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f user.ldif
```

- **Expected Output**:

```
adding new entry "uid=jdoe,ou=users,dc=example,dc=com"
```

#### 4. Install and Configure LDAP Client on Other Servers

**Install Required Packages**:

```bash
sudo apt-get install libnss-ldap libpam-ldap ldap-utils nscd
```

**Configuration Prompts**:

| Setting                                     | Value                           |
|---------------------------------------------|----------------------------------|
| LDAP server URI                             | `ldap://ldapserver.example.com` |
| Distinguished name of the search base       | `dc=example,dc=com`             |
| LDAP version                                | `3`                             |
| Make local root Database admin              | Yes                             |
| Does the LDAP database require login?       | No                              |
| LDAP account for root                       | `cn=admin,dc=example,dc=com`    |
| LDAP root account password                  | `[Enter admin password]`        |

**Configure NSS to Use LDAP**:

Edit `/etc/nsswitch.conf`:

```conf
passwd:         compat systemd ldap
group:          compat systemd ldap
shadow:         compat ldap
```

**Configure PAM for LDAP Authentication**:

Ensure that `/etc/pam.d/common-auth` includes:

```conf
auth    sufficient      pam_ldap.so
auth    required        pam_unix.so nullok_secure try_first_pass
```

**Restart NSS Service**:

```bash
sudo service nscd restart
```

#### 5. Enable Home Directory Creation

Install `libpam-mkhomedir`:

```bash
sudo apt-get install libpam-mkhomedir
```

Configure PAM to create home directories:

Edit `/etc/pam.d/common-session` and add:

```conf
session required        pam_mkhomedir.so skel=/etc/skel umask=077
```

### Verification and Testing

**Test LDAP Lookup**:

```bash
getent passwd jdoe
```

**Expected Output**:

```
jdoe:x:10000:10000:John Doe:/home/jdoe:/bin/bash
```

**Test Login as LDAP User**:

Use SSH or local terminal:

```bash
ssh jdoe@localhost
```

- **Expected Behavior**:
- Prompt for password.
- Upon successful authentication, home directory is created.

### Maintenance and Management

#### Adding More Users

**Create LDIF File for New User** (`user2.ldif`):

```ldif
dn: uid=asmith,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
uid: asmith
cn: Alice Smith
sn: Smith
givenName: Alice
mail: asmith@example.com
userPassword: {SSHA}encrypted_password_here
```

**Add User to LDAP**:

```bash
sudo ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f user2.ldif
```

#### Modifying User Attributes

**Create Modify LDIF File** (`modify_jdoe.ldif`):

```ldif
dn: uid=jdoe,ou=users,dc=example,dc=com
changetype: modify
replace: mail
mail: john.doe@example.com
```

**Apply Changes**:

```bash
sudo ldapmodify -x -D "cn=admin,dc=example,dc=com" -W -f modify_jdoe.ldif
```

#### Deleting Users

**Delete User Entry**:

```bash
sudo ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "uid=jdoe,ou=users,dc=example,dc=com"
```

### Challenges

1. Install and configure an LDAP server on a Linux system. Set up the basic directory structure and include at least three organizational units (OUs).
2. Add entries to the LDAP directory, including users and groups. Practice creating at least 10 user entries and 3 groups, assigning users to different groups.
3. Configure a Linux system to use LDAP for user authentication. Test this by logging into the system with user credentials stored in the LDAP directory.
4. Develop a strategy for backing up the LDAP directory. Perform a backup, then restore from this backup to ensure the integrity and completeness of your backup method.
5. Use the `ldapsearch` command to perform various queries on the LDAP directory. Try to search for specific users, groups, and other entities based on different attributes.
6. Secure your LDAP communications with TLS/SSL. Configure the server for encrypted connections and verify the security by connecting to it with an LDAP client.
7. Choose an application or service (such as email or web service) that supports LDAP integration. Configure it to authenticate users against your LDAP directory.
8. Design and implement a custom LDAP schema for a specific use case (like managing inventory or tracking software licenses). Add attributes and object classes that are not available in the default schema.
9. Set up LDAP replication. Configure a secondary LDAP server and ensure that it synchronizes correctly with your primary LDAP server.
10. Simulate common LDAP connectivity issues and practice troubleshooting. Document each issue simulated, your diagnostic process, and the steps taken to resolve the issues.
