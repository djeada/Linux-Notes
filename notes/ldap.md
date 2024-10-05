# LDAP (Lightweight Directory Access Protocol)

LDAP is a protocol used to access and manage directory information over an IP network. It is open, vendor-neutral, and an industry standard. LDAP is commonly used for centralized authentication, where user credentials and permissions are managed in a single directory and applied across multiple systems and applications.

## Understanding LDAP Concepts

### Directory

A **directory** is similar to a database but optimized for reading, browsing, and searching information rather than for transaction-oriented operations. It stores descriptive, attribute-based information and supports advanced filtering capabilities.

- **Purpose**: Store user credentials, permissions, organizational data.
- **Structure**: Hierarchical, resembling a tree structure.

### Entries and Attributes

- **Entry**: A unique object within the directory (e.g., a user, group, or device).
- **Attributes**: Key-value pairs that describe the entry (e.g., name, email, password).

### Distinguished Names (DN)

A **Distinguished Name (DN)** uniquely identifies an entry in the LDAP directory. It is a string composed of key-value pairs separated by commas.

- **Example**: `uid=jdoe,ou=users,dc=example,dc=com`
- **Components**:
  - `uid=jdoe`: User ID
  - `ou=users`: Organizational Unit
  - `dc=example,dc=com`: Domain Components representing `example.com`

### Schema

The **schema** defines the directory's structure, including:

- **Object Classes**: Types of entries (e.g., person, organizationalUnit).
- **Attributes**: Allowed attributes for each object class.
- **Syntax Rules**: Data types and constraints for attributes.

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

- **LDAP Server**: Centralized directory service hosting user credentials.
- **Client Hosts**: Systems and applications (web servers, email servers, SSH servers, FTP servers) that authenticate users against the LDAP server.


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

**Components Explained**:

- **dc**: Domain Component
  - Represents parts of the domain name.
  - `dc=example,dc=com` corresponds to `example.com`.
- **ou**: Organizational Unit
  - Groups entries logically (e.g., `ou=users`, `ou=groups`).
- **uid**: User Identifier
  - Represents a user entry (e.g., `uid=alice`).
- **cn**: Common Name
  - Typically used for naming entries like groups (e.g., `cn=admins`).

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

- **Steps**:
  1. **User** sends login request to **Client Host**.
  2. **Client Host** sends authentication request to **LDAP Server**.
  3. **LDAP Server** processes the request and sends back the authentication result.
  4. **Client Host** grants or denies access to the **User** based on the result.

## Common LDAP Operations

LDAP defines a set of operations that clients can perform on the directory.

### Bind

- **Purpose**: Authenticate and specify the LDAP protocol version.
- **Usage**: Initiates a session between the client and the LDAP server.

**Example Command**:

```bash
ldapwhoami -x -D "uid=jdoe,ou=users,dc=example,dc=com" -W
```

- **Explanation**:
  - `-x`: Use simple authentication.
  - `-D`: Bind DN (the user's distinguished name).
  - `-W`: Prompt for the password.

**Expected Output**:

```
Enter LDAP Password:
dn:uid=jdoe,ou=users,dc=example,dc=com
```

### Search & Compare

- **Search**: Retrieve entries that match certain criteria.
- **Compare**: Check if a specified attribute has a certain value.

**Example Search Command**:

```bash
ldapsearch -x -b "dc=example,dc=com" "(uid=jdoe)"
```

- **Explanation**:
  - `-x`: Use simple authentication.
  - `-b`: Base DN to search.
  - `"(uid=jdoe)"`: Search filter.

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

### Add, Delete & Modify

- **Add**: Create new entries.
- **Delete**: Remove entries.
- **Modify**: Update existing entries.

**Example Add Command**:

```bash
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f new_user.ldif
```

**Example Delete Command**:

```bash
ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "uid=jdoe,ou=users,dc=example,dc=com"
```

### Unbind

- **Purpose**: Terminate the LDAP session.
- **Usage**: Automatically handled after operations or explicitly by the client.

---

## LDAP Data Model

The LDAP data model is entry-centric.

- **Entry**: A collection of attributes with a unique DN.
- **Attributes**: Have a type (attribute name) and one or more values.

**Example Entry**:

```
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
uid: jdoe
cn: John Doe
sn: Doe
mail: jdoe@example.com
userPassword: {SHA}kD9G1mvg3FjU5G2m5A==
```

- **dn**: Unique identifier.
- **objectClass**: Defines the type of object.
- **Attributes**: uid, cn, sn, mail, userPassword.

---

## LDAP Search Filters

Search filters control what entries are returned in a search operation.

**Syntax**:

- `(attribute=value)`: Equality match.
- `(&(filter1)(filter2))`: AND operation.
- `(|(filter1)(filter2))`: OR operation.
- `(!(filter))`: NOT operation.

**Examples**:

- **Find users with uid 'jdoe'**:

  ```
  (uid=jdoe)
  ```

- **Find entries that are persons and have an email**:

  ```
  (&(objectClass=person)(mail=*))
  ```

- **Find users not in the 'admins' group**:

  ```
  (!(memberOf=cn=admins,ou=groups,dc=example,dc=com))
  ```

---

## LDAP Tools and Utilities

### Command-Line Tools

1. **ldapsearch**: Search for entries.

   **Usage**:

   ```bash
   ldapsearch -x -b "dc=example,dc=com" "(objectClass=*)"
   ```

2. **ldapadd/ldapmodify**: Add or modify entries.

   **Usage**:

   ```bash
   ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f entry.ldif
   ```

3. **ldapdelete**: Delete entries.

   **Usage**:

   ```bash
   ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "uid=jdoe,ou=users,dc=example,dc=com"
   ```

4. **ldapwhoami**: Display the DN bound to the session.

   **Usage**:

   ```bash
   ldapwhoami -x -D "uid=jdoe,ou=users,dc=example,dc=com" -W
   ```

### GUI-Based Tools

1. **Apache Directory Studio**: An Eclipse-based LDAP browser and editor.

2. **phpLDAPadmin**: A web-based LDAP administration tool.

3. **JXplorer**: A Java-based LDAP client.

---

## Implementing LDAP for Centralized Authentication

Centralized authentication via LDAP allows multiple servers and applications to use a single directory for user authentication and authorization.

### Prerequisites

- **Operating System**: Ubuntu Server 20.04 LTS (or similar).
- **Root or Sudo Access**: Required for installation and configuration.
- **Network Configuration**: Ensure that servers can communicate over the network.

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

- **Omit OpenLDAP server configuration?**: **No**
- **DNS domain name**: `example.com`
- **Organization name**: `Example Company`
- **Administrator password**: `[Set a strong password]`
- **Database backend**: `MDB`
- **Remove the database when slapd is purged?**: **No**
- **Move old database?**: **Yes**

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

- **Expected Output**:

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

- **Enter Password**: `[Type password]`
- **Re-enter Password**: `[Retype password]`
- **Output**: `{SSHA}encrypted_password_here`

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

- **LDAP server URI**: `ldap://ldapserver.example.com`
- **Distinguished name of the search base**: `dc=example,dc=com`
- **LDAP version**: `3`
- **Make local root Database admin**: **Yes**
- **Does the LDAP database require login?**: **No**
- **LDAP account for root**: `cn=admin,dc=example,dc=com`
- **LDAP root account password**: `[Enter admin password]`

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

- **Expected Output**:

```
jdoe:x:10000:10000:John Doe:/home/jdoe:/bin/bash
```

**Test Login as LDAP User**:

- Use SSH or local terminal:

```bash
ssh jdoe@localhost
```

- **Expected Behavior**:
  - Prompt for password.
  - Upon successful authentication, home directory is created.

### Maintenance and Management

#### Adding More Users

- **Create LDIF File for New User** (`user2.ldif`):

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

- **Add User to LDAP**:

  ```bash
  sudo ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f user2.ldif
  ```

#### Modifying User Attributes

- **Create Modify LDIF File** (`modify_jdoe.ldif`):

  ```ldif
  dn: uid=jdoe,ou=users,dc=example,dc=com
  changetype: modify
  replace: mail
  mail: john.doe@example.com
  ```

- **Apply Changes**:

  ```bash
  sudo ldapmodify -x -D "cn=admin,dc=example,dc=com" -W -f modify_jdoe.ldif
  ```

#### Deleting Users

- **Delete User Entry**:

  ```bash
  sudo ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "uid=jdoe,ou=users,dc=example,dc=com"
  ```

## Challenges

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
