## LDAP: Lightweight Directory Access Protocol

LDAP stands for Lightweight Directory Access Protocol.

It is a network protocol used to access and manage directory information. A directory is a structured store of information about users, groups, devices, applications, permissions, and organizational resources.

LDAP is commonly used for centralized authentication.

Instead of creating separate user accounts on every server, an organization can store users in one LDAP directory. Then many systems can ask the LDAP server to verify users.

Without LDAP:

- Server A has its own users
- Server B has its own users
- Server C has its own users
- User management is repeated on every system.

With LDAP:

- Users are stored centrally in LDAP
- Servers ask LDAP to authenticate users
- User management is centralized.

LDAP is used by systems such as:

- Linux login authentication
- SSH authentication
- email systems
- web applications
- VPN services
- file servers
- enterprise directories
- identity management platforms

LDAP itself is a protocol. OpenLDAP is a common open-source LDAP server implementation.

### Why LDAP Is Useful

LDAP is useful when many systems need the same identity information.

For example, an organization may have:

- web servers
- email servers
- SSH servers
- file servers
- internal applications
- VPN gateways

All of these systems may need to know:

- Who is this user?
- What is their username?
- What groups do they belong to?
- Are they allowed to log in?
- What is their email address?
- What is their home directory?

LDAP allows this information to live in one central directory.

```text id="d59bwr"
                 +--------------------+
                 |    LDAP Server     |
                 | ldap.example.com   |
                 +----------+---------+
                            |
             ---------------------------------
             |               |               |
     +-------+-----+   +-----+-------+   +---+-------+
     | Web Server  |   | Email Server|   | SSH Server|
     +-------------+   +-------------+   +-----------+
             |               |               |
             +---------------+---------------+
                             |
                             v
                   Users authenticate using
                   centralized LDAP data
```

The main benefit is consistency. If a user changes their password or leaves the organization, the change can be made centrally.

### Directory

An LDAP directory is similar to a database, but it is optimized for reading, searching, and browsing structured information.

A normal relational database is often used for frequent transactions, joins, and complex updates.

An LDAP directory is usually optimized for:

- fast lookups
- many read operations
- hierarchical organization
- attribute-based searching
- centralized identity data

A directory stores entries such as:

- users
- groups
- departments
- devices
- services
- policies

Each entry has attributes.

### Entries and Attributes

An entry is one object in the LDAP directory.

Examples of entries:

- a user account
- a group
- an organizational unit
- a computer
- a printer

Each entry contains attributes.

For example, a user entry might contain:

```text id="skb5ob"
uid: jdoe
cn: John Doe
sn: Doe
mail: jdoe@example.com
loginShell: /bin/bash
homeDirectory: /home/jdoe
```

The entry is the object. The attributes describe the object.

```text id="b7dqaf"
Entry:
uid=jdoe,ou=users,dc=example,dc=com

Attributes:
uid: jdoe
cn: John Doe
sn: Doe
mail: jdoe@example.com
```

### Distinguished Names

A Distinguished Name, or DN, uniquely identifies an entry in the LDAP directory.

It works like a full path to the entry.

Example:

```text id="qvhki6"
uid=jdoe,ou=users,dc=example,dc=com
```

This DN means:

- uid=jdoe        the user entry
- ou=users        inside the users organizational unit
- dc=example      inside the example domain component
- dc=com          inside the com domain component

The DN is read from left to right as specific to general.

A helpful comparison:

```text id="m36wk3"
Filesystem path:
/home/users/jdoe

LDAP DN:
uid=jdoe,ou=users,dc=example,dc=com
```

Both describe where something is located in a hierarchy.

### Common DN Components

- dc   domain component
- ou   organizational unit
- uid  user identifier
- cn   common name

Examples:

- dc=example,dc=com
- ou=users,dc=example,dc=com
- uid=alice,ou=users,dc=example,dc=com
- cn=admins,ou=groups,dc=example,dc=com

Meaning:

- dc=example,dc=com                 example.com domain
- ou=users                           users container
- uid=alice                          user named alice
- cn=admins                          group named admins

### Directory Information Tree

LDAP stores entries in a hierarchy called the Directory Information Tree, or DIT.

```text id="v9zqqa"
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

In this example:

- dc=example,dc=com is the base domain.
- ou=users stores user entries.
- ou=groups stores group entries.
- uid=alice and uid=bob are user entries.
- cn=admins and cn=users are group entries.

### Base DN

The base DN is the starting point for LDAP searches.

For the domain `example.com`, the base DN is often:

```text id="azy1ti"
dc=example,dc=com
```

A search using this base can search everything under the example.com directory tree.

A narrower search base might be:

```text id="sgwptj"
ou=users,dc=example,dc=com
```

This searches only under the `users` organizational unit.

### Schema

An LDAP schema defines what kinds of entries are allowed and what attributes they can contain.

The schema controls:

- object classes
- required attributes
- optional attributes
- attribute syntax
- valid structure

An object class defines a type of entry.

Examples:

- organization
- organizationalUnit
- inetOrgPerson
- posixAccount
- posixGroup
- shadowAccount

For example, `inetOrgPerson` is commonly used for user information such as names and email addresses.

For Linux login accounts, user entries often also need `posixAccount` and sometimes `shadowAccount`.

That is important because a simple address-book-style LDAP user is not always enough for Linux login.

### LDAP User Entry Example

A basic informational user might look like this:

```ldif id="snfevy"
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
uid: jdoe
cn: John Doe
sn: Doe
givenName: John
mail: jdoe@example.com
userPassword: {SSHA}encrypted_password_here
```

For Linux authentication through NSS/PAM, a more complete user entry usually needs POSIX attributes:

```ldif id="vcqj88"
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: jdoe
cn: John Doe
sn: Doe
givenName: John
mail: jdoe@example.com
uidNumber: 10000
gidNumber: 10000
homeDirectory: /home/jdoe
loginShell: /bin/bash
userPassword: {SSHA}encrypted_password_here
```

Important fields:

- uidNumber       numeric Linux user ID
- gidNumber       primary Linux group ID
- homeDirectory   home directory path
- loginShell      login shell
- userPassword    stored password hash

Without POSIX attributes, `getent passwd jdoe` may not return a valid Linux account.

### LDAP Group Entry Example

A Linux-compatible group can use `posixGroup`.

```ldif id="pl8n83"
dn: cn=developers,ou=groups,dc=example,dc=com
objectClass: posixGroup
cn: developers
gidNumber: 10000
memberUid: jdoe
```

This defines a group named `developers`.

The user `jdoe` is listed as a member using `memberUid`.

### LDIF

LDIF stands for LDAP Data Interchange Format.

It is a plain text format used to add, modify, delete, export, and import LDAP entries.

Example LDIF entry:

```ldif id="fip7c7"
dn: ou=users,dc=example,dc=com
objectClass: organizationalUnit
ou: users
```

LDIF files are commonly used with commands such as:

- ldapadd
- ldapmodify
- ldapdelete
- ldapsearch

### Common LDAP Operations

LDAP supports several common operations.

- bind       authenticate to the LDAP server
- search     find entries
- compare    check whether an attribute has a value
- add        create an entry
- modify     change an entry
- delete     remove an entry
- unbind     close the session

### Bind

Bind means authenticate to the LDAP server.

An anonymous bind does not provide a username or password.

An authenticated bind provides a DN and password.

Example:

```bash id="n1jw60"
ldapwhoami -x -D "uid=jdoe,ou=users,dc=example,dc=com" -W
```

Options:

- -x   use simple authentication
- -D   bind DN
- -W   prompt for password

Example output:

```text id="t2te53"
Enter LDAP Password:
dn:uid=jdoe,ou=users,dc=example,dc=com
```

Interpretation:

- The bind succeeded.
- The server recognizes the authenticated identity as this DN.

### Search

Search retrieves entries matching a filter.

Example:

```bash id="o1k3qe"
ldapsearch -x -b "dc=example,dc=com" "(uid=jdoe)"
```

Options:

- -x                    simple authentication
- -b                    base DN
- "(uid=jdoe)"          search filter

Example output:

```text id="piuic3"
dn: uid=jdoe,ou=users,dc=example,dc=com
uid: jdoe
cn: John Doe
sn: Doe
mail: jdoe@example.com

## search result
result: 0 Success

## numEntries: 1
```

Interpretation:

- The search succeeded.
- One matching entry was found.
- The matching user is jdoe.

### Add

The add operation creates a new entry.

Example:

```bash id="r3q2gh"
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f user.ldif
```

Example output:

```text id="tvz3fj"
adding new entry "uid=jdoe,ou=users,dc=example,dc=com"
```

Interpretation:

- The entry from user.ldif was added to the directory.

### Modify

The modify operation changes an existing entry.

Example modify file:

```ldif id="hinbel"
dn: uid=jdoe,ou=users,dc=example,dc=com
changetype: modify
replace: mail
mail: john.doe@example.com
```

Apply it:

```bash id="paqdk5"
ldapmodify -x -D "cn=admin,dc=example,dc=com" -W -f modify_jdoe.ldif
```

Example output:

```text id="w4fzti"
modifying entry "uid=jdoe,ou=users,dc=example,dc=com"
```

Interpretation:

- The mail attribute was replaced with the new value.

### Delete

The delete operation removes an entry.

Example:

```bash id="mhb2j3"
ldapdelete -x -D "cn=admin,dc=example,dc=com" -W \
"uid=jdoe,ou=users,dc=example,dc=com"
```

Example output may be silent if successful.

Interpretation:

- No error usually means the entry was deleted.
- Verify with ldapsearch.

### LDAP Search Filters

Search filters control which entries are returned.

Basic equality filter:

```text id="bbl4l9"
(uid=jdoe)
```

Find entries with an email address:

```text id="acm1hk"
(mail=*)
```

AND filter:

```text id="ahqax6"
(&(objectClass=person)(mail=*))
```

OR filter:

```text id="creytb"
(|(uid=alice)(uid=bob))
```

NOT filter:

```text id="bprtim"
(!(uid=jdoe))
```

Find users with usernames beginning with `a`:

```text id="sjwnif"
(uid=a*)
```

A search filter is one of the most important LDAP skills because almost every LDAP integration depends on correct filters.

### LDAP Authentication Flow

When LDAP is used for authentication, the client application usually asks LDAP whether a user’s credentials are valid.

```text id="ul4smn"
User                Client Host             LDAP Server
 |                       |                       |
 |---Login Request------>|                       |
 |                       |---Bind/Search-------> |
 |                       |                       |
 |                       |<--Result------------- |
 |<--Access Granted/Denied---------------------- |
```

Typical steps:

1. User enters username and password.
2. Client finds the user entry in LDAP.
3. Client tries to bind as that user or verify the password.
4. LDAP returns success or failure.
5. Client grants or denies access.

### Installing an LDAP Server

On Debian or Ubuntu, install OpenLDAP and LDAP utilities:

```bash id="f6owsp"
sudo apt-get update
sudo apt-get install slapd ldap-utils
```

If configuration prompts do not appear, run:

```bash id="lg3v69"
sudo dpkg-reconfigure slapd
```

Typical configuration values:

- DNS domain name: example.com
- Organization name: Example Company
- Admin DN: cn=admin,dc=example,dc=com
- Database backend: MDB
- Remove database when slapd is purged: No
- Move old database: Yes

For the domain:

```text id="mkkidq"
example.com
```

the base DN is:

```text id="w1x84c"
dc=example,dc=com
```

### Creating the Base Directory Structure

Create `base.ldif`:

```ldif id="xaoof0"
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

Load it:

```bash id="aa8uxt"
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f base.ldif
```

Expected output:

```text id="vlyngj"
adding new entry "dc=example,dc=com"

adding new entry "ou=users,dc=example,dc=com"

adding new entry "ou=groups,dc=example,dc=com"
```

Interpretation:

- The base domain and two organizational units were created.
- The directory now has containers for users and groups.

### Generating a Password Hash

Use `slappasswd`:

```bash id="ea3fe1"
slappasswd
```

Example output:

```text id="xd7nr5"
{SSHA}r3wP3fH0QpK8vF5yBEXAMPLEHASH
```

Use this value in the `userPassword` attribute.

Avoid storing plain text passwords in LDIF files.

### Adding a Linux-Compatible User

Create `jdoe.ldif`:

```ldif id="c37fzx"
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: jdoe
cn: John Doe
sn: Doe
givenName: John
mail: jdoe@example.com
uidNumber: 10000
gidNumber: 10000
homeDirectory: /home/jdoe
loginShell: /bin/bash
userPassword: {SSHA}encrypted_password_here
```

Add it:

```bash id="xczfda"
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f jdoe.ldif
```

Expected output:

```text id="okaiu8"
adding new entry "uid=jdoe,ou=users,dc=example,dc=com"
```

### Adding a Group

Create `developers.ldif`:

```ldif id="r8s1kq"
dn: cn=developers,ou=groups,dc=example,dc=com
objectClass: posixGroup
cn: developers
gidNumber: 10000
memberUid: jdoe
```

Add it:

```bash id="pnif02"
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f developers.ldif
```

Expected output:

```text id="otkgal"
adding new entry "cn=developers,ou=groups,dc=example,dc=com"
```

### Searching for Users and Groups

Search for a user:

```bash id="zueg3k"
ldapsearch -x -b "ou=users,dc=example,dc=com" "(uid=jdoe)" uid cn mail
```

Example output:

```text id="j4gwe5"
dn: uid=jdoe,ou=users,dc=example,dc=com
uid: jdoe
cn: John Doe
mail: jdoe@example.com

## numEntries: 1
```

Search for a group:

```bash id="donz8t"
ldapsearch -x -b "ou=groups,dc=example,dc=com" "(cn=developers)"
```

Example output:

```text id="uv301v"
dn: cn=developers,ou=groups,dc=example,dc=com
objectClass: posixGroup
cn: developers
gidNumber: 10000
memberUid: jdoe
```

### Configuring a Linux Client for LDAP Login

A Linux client needs a way to use LDAP for identity lookup and authentication.

Common approaches include:

- SSSD
- nslcd with libnss-ldapd and libpam-ldapd
- older libnss-ldap and libpam-ldap

The older packages may still appear in tutorials, but many modern systems prefer SSSD or nslcd-based setups.

The client-side job is to connect Linux account lookup and login authentication to LDAP.

The system components are:

- NSS     resolves users and groups
- PAM     handles authentication sessions
- LDAP    stores users and groups

Flow:

```text id="yiu1gq"
getent passwd jdoe
        |
        v
NSS asks LDAP
        |
        v
LDAP returns user attributes
        |
        v
Linux sees jdoe as a valid user
```

### Verifying LDAP Identity Lookup

After configuring the client, test user lookup:

```bash id="erl589"
getent passwd jdoe
```

Expected output:

```text id="xn2xit"
jdoe:x:10000:10000:John Doe:/home/jdoe:/bin/bash
```

Interpretation:

- The operating system can resolve jdoe through NSS.
- The LDAP user is visible as a Linux account.

Check group information:

```bash id="dxote4"
getent group developers
```

Expected output:

```text id="y0hnp8"
developers:*:10000:jdoe
```

Check user identity:

```bash id="slen42"
id jdoe
```

Expected output:

```text id="qlb1y7"
uid=10000(jdoe) gid=10000(developers) groups=10000(developers)
```

### Home Directory Creation

If LDAP users can authenticate but have no home directory, configure PAM to create it automatically.

Install the needed module:

```bash id="s079op"
sudo apt-get install libpam-mkhomedir
```

Add to the PAM session configuration:

```conf id="k01hd3"
session required pam_mkhomedir.so skel=/etc/skel umask=077
```

Expected behavior:

```text id="nfieyy"
When jdoe logs in for the first time,
Linux creates /home/jdoe automatically.
```

### Testing LDAP Server Connectivity

Test anonymous access:

```bash id="ikzdeq"
ldapwhoami -x -H ldap://localhost
```

Expected output:

```text id="szp884"
anonymous
```

Test authenticated bind:

```bash id="w4cfo2"
ldapwhoami -x -D "cn=admin,dc=example,dc=com" -W -H ldap://localhost
```

Expected output:

```text id="m3p4mi"
dn:cn=admin,dc=example,dc=com
```

Interpretation:

- The LDAP server is reachable.
- The admin DN and password work.

### Securing LDAP with TLS

Simple LDAP authentication sends a DN and password to the server.

This should be protected with encryption.

LDAP can be secured in two common ways:

- StartTLS over ldap://
- LDAPS over ldaps://

StartTLS begins as a normal LDAP connection and upgrades to TLS.

Example StartTLS test:

```bash id="xmfw04"
ldapwhoami -x -ZZ -D "uid=jdoe,ou=users,dc=example,dc=com" -W -H ldap://ldap.example.com
```

The `-ZZ` option requires StartTLS.

If TLS cannot be established, the command fails.

### TLS Configuration Concept

The server needs:

- certificate authority certificate
- server certificate
- server private key

The client needs to trust the CA certificate.

A conceptual TLS flow:

```text id="e2mr9o"
LDAP client
    |
    | StartTLS request
    v
LDAP server presents certificate
    |
    v
Client verifies certificate
    |
    v
Encrypted LDAP session begins
```

If certificate validation fails, the client should refuse the connection.

### Password Policies

LDAP can enforce password rules through password policy support.

Common policy rules include:

- minimum password length
- password expiration
- failed login lockout
- password change on first login
- lockout duration

Example policy ideas:

- pwdMinLength: 8
- pwdMaxFailure: 5
- pwdLockout: TRUE
- pwdLockoutDuration: 900
- pwdMustChange: TRUE

Password policies help reduce weak passwords and repeated brute-force attempts.

### Backups

LDAP should be backed up regularly.

A common backup command is:

```bash id="ty8e50"
slapcat > ldap-backup.ldif
```

This exports the directory database to LDIF.

A restore may use:

```bash id="ig9svi"
slapadd -l ldap-backup.ldif
```

Typical safe backup workflow:

1. Export LDAP data with slapcat.
2. Store backup securely.
3. Test restore on a separate system.
4. Protect backup files because they may contain password hashes.

### Replication

LDAP replication means keeping multiple LDAP servers synchronized.

A typical layout:

```text id="xos8qd"
              +-------------------+
              | Primary LDAP      |
              | ldap1.example.com |
              +---------+---------+
                        |
             replication updates
                        |
              +---------v---------+
              | Secondary LDAP    |
              | ldap2.example.com |
              +-------------------+
```

Replication improves:

- availability
- read scalability
- fault tolerance
- geographic distribution

If the primary server fails, clients may still authenticate using a replica if configured correctly.

### Access Control

LDAP access control determines who can read or modify entries.

Common rules include:

- users can read public attributes
- users can change their own password
- admins can modify users and groups
- anonymous users have limited access
- password hashes are protected

Access control is important because LDAP contains sensitive identity data.

Poor access control can expose user information or allow unauthorized changes.

### Scenario 1: Simulate “LDAP Server Is Down”

Practice identifying a server availability problem.

#### Simulate the Problem

On a test LDAP server:

```bash id="fhzbi6"
sudo systemctl stop slapd
```

#### Check with `ldapwhoami`

```bash id="vrcruh"
ldapwhoami -x -H ldap://localhost
```

Example output:

```text id="a8zucp"
ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)
```

#### Check Service Status

```bash id="te19ma"
systemctl status slapd
```

Example output:

```text id="picnwp"
● slapd.service - LSB: OpenLDAP standalone server
   Active: inactive (dead)
```

Interpretation:

- The LDAP client cannot contact the server.
- The slapd service is stopped.
- This is a service availability issue, not a password or search filter issue.

#### Fix

```bash id="hc26vq"
sudo systemctl start slapd
```

Verify:

```bash id="cbdfie"
ldapwhoami -x -H ldap://localhost
```

Expected output:

```text id="ykgkv1"
anonymous
```

### Scenario 2: Simulate Wrong LDAP URI or Port

Practice diagnosing connection target mistakes.

#### Simulate the Problem

Use the wrong port:

```bash id="d84ff6"
ldapsearch -x -H ldap://localhost:1389 -b "dc=example,dc=com" "(objectClass=*)"
```

Example output:

```text id="zailxs"
ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)
```

#### Check Listening Ports

```bash id="x63sce"
ss -tulnp | grep slapd
```

Example output:

```text id="fnlc8i"
tcp LISTEN 0 128 0.0.0.0:389 0.0.0.0:* users:(("slapd",pid=1200,fd=8))
```

Interpretation:

- slapd is listening on port 389.
- The client tried port 1389.
- The problem is the wrong LDAP URI or port.

#### Fix

Use the correct URI:

```bash id="w1hx8w"
ldapsearch -x -H ldap://localhost:389 -b "dc=example,dc=com" "(objectClass=*)"
```

### Scenario 3: Simulate Invalid Credentials

Practice identifying authentication failure.

#### Simulate the Problem

Run a bind with the wrong password:

```bash id="si8k4d"
ldapwhoami -x -D "cn=admin,dc=example,dc=com" -W -H ldap://localhost
```

Enter the wrong password.

Example output:

```text id="sb6wux"
ldap_bind: Invalid credentials (49)
```

Interpretation:

- The LDAP server is reachable.
- The bind DN exists or was accepted syntactically.
- The password is wrong, or the DN/password combination is invalid.

#### Check

Try a known working bind:

```bash id="vv7wun"
ldapwhoami -x -D "cn=admin,dc=example,dc=com" -W -H ldap://localhost
```

Expected output:

```text id="p38xhh"
dn:cn=admin,dc=example,dc=com
```

### Scenario 4: Simulate Wrong Base DN

Practice recognizing search base mistakes.

#### Simulate the Problem

Use the wrong base DN:

```bash id="h2tu79"
ldapsearch -x -H ldap://localhost -b "dc=wrong,dc=com" "(uid=jdoe)"
```

Example output:

```text id="rrp4sl"
## search result
search: 2
result: 32 No such object
```

Interpretation:

- The server is reachable.
- The search base does not exist.
- This is not a network problem.
- The base DN is wrong.

#### Check the Correct Base

Search from the correct base:

```bash id="i74yao"
ldapsearch -x -H ldap://localhost -b "dc=example,dc=com" "(uid=jdoe)"
```

Expected result:

```text id="xvfh68"
result: 0 Success
## numEntries: 1
```

### Scenario 5: Simulate Search Filter That Finds Nothing

Distinguish between “search succeeded but no entries matched” and “LDAP error.”

#### Simulate the Problem

Search for a nonexistent user:

```bash id="afhop8"
ldapsearch -x -H ldap://localhost -b "dc=example,dc=com" "(uid=nosuchuser)"
```

Example output:

```text id="cf366v"
## search result
search: 2
result: 0 Success

## numResponses: 1
## numEntries: 0
```

Interpretation:

- The search worked.
- The base DN exists.
- The filter matched no entries.
- This is a data or filter issue, not a server issue.

#### Fix

Check known users:

```bash id="acdzvb"
ldapsearch -x -H ldap://localhost -b "ou=users,dc=example,dc=com" "(objectClass=inetOrgPerson)" uid
```

### Scenario 6: Simulate Missing POSIX Attributes

Show why an LDAP user may exist but not appear as a Linux login user.

#### Simulate the Problem

Create a user with only `inetOrgPerson` attributes and no `uidNumber`, `gidNumber`, `homeDirectory`, or `loginShell`.

Search finds the user:

```bash id="maxjp3"
ldapsearch -x -b "ou=users,dc=example,dc=com" "(uid=jdoe)"
```

Example output:

```text id="gidcnb"
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
uid: jdoe
cn: John Doe
sn: Doe
mail: jdoe@example.com
```

But Linux lookup fails:

```bash id="x50ugz"
getent passwd jdoe
```

Example output:

```text id="z1jo22"
```

No output.

Interpretation:

- LDAP contains the user as a directory entry.
- However, the user is not a valid POSIX login account.
- NSS needs POSIX attributes such as uidNumber, gidNumber, homeDirectory, and loginShell.

#### Fix

Add the required object classes and attributes:

- objectClass: posixAccount
- objectClass: shadowAccount
- uidNumber: 10000
- gidNumber: 10000
- homeDirectory: /home/jdoe
- loginShell: /bin/bash

Then test again:

```bash id="pd8sdr"
getent passwd jdoe
```

Expected output:

```text id="gjmcf0"
jdoe:x:10000:10000:John Doe:/home/jdoe:/bin/bash
```

### Scenario 7: Simulate TLS Failure

Practice diagnosing TLS certificate or StartTLS problems.

#### Simulate the Problem

Require StartTLS against a server that is not correctly configured for TLS:

```bash id="n87xti"
ldapwhoami -x -ZZ -H ldap://localhost
```

Example output:

```text id="bhdn7x"
ldap_start_tls: Connect error (-11)
additional info: TLS error -8172:Peer's certificate issuer has been marked as not trusted
```

Interpretation:

- The server was contacted.
- TLS negotiation failed.
- The client does not trust the certificate issuer, or the certificate configuration is wrong.

#### Check Client TLS Config

```bash id="nss2y8"
grep -v '^#' /etc/ldap/ldap.conf
```

Example:

```text id="l22c45"
TLS_CACERT /etc/ssl/certs/ca-certificates.crt
TLS_REQCERT demand
```

#### Fix

Possible fixes:

- install the correct CA certificate
- point TLS_CACERT to the correct CA file
- fix server certificate hostname mismatch
- verify server certificate permissions
- restart slapd after TLS changes

Then test again:

```bash id="g7f5w7"
ldapwhoami -x -ZZ -H ldap://localhost
```

Expected output:

```text id="knz3sa"
anonymous
```

### Scenario 8: Simulate LDAP Client Login Lookup Failure

Practice diagnosing NSS integration problems.

#### Simulate the Problem

Assume LDAP search works:

```bash id="t5b0n7"
ldapsearch -x -b "dc=example,dc=com" "(uid=jdoe)"
```

but Linux lookup fails:

```bash id="vsrttg"
getent passwd jdoe
```

Example output:

```text id="fr95uw"
```

No output.

#### Check NSS Configuration

```bash id="h2zvon"
grep '^passwd\|^group\|^shadow' /etc/nsswitch.conf
```

Example broken output:

```text id="h5if8f"
passwd: files systemd
group:  files systemd
shadow: files
```

Interpretation:

- LDAP search works directly.
- But NSS is not configured to ask LDAP.
- Linux account lookup only checks local files and systemd.

#### Fix

Depending on the client stack, configure NSS to include LDAP or SSSD.

Example concept:

```text id="atolix"
passwd: files systemd ldap
group:  files systemd ldap
shadow: files ldap
```

Then restart the relevant cache/client service:

```bash id="cwgngy"
sudo systemctl restart nscd
```

or, if using SSSD:

```bash id="rxt9zw"
sudo systemctl restart sssd
```

Test again:

```bash id="gnv7p2"
getent passwd jdoe
```

### Scenario 9: Simulate LDAP Authorization Problem

Show the difference between authentication and authorization.

A user may authenticate successfully but still not be allowed to access a service.

#### Simulate the Problem

Assume `jdoe` can bind successfully:

```bash id="kph66f"
ldapwhoami -x -D "uid=jdoe,ou=users,dc=example,dc=com" -W
```

Expected output:

```text id="tssif7"
dn:uid=jdoe,ou=users,dc=example,dc=com
```

But the application requires membership in:

```text id="revnrr"
cn=admins,ou=groups,dc=example,dc=com
```

Search group membership:

```bash id="mugw4y"
ldapsearch -x -b "ou=groups,dc=example,dc=com" "(cn=admins)"
```

Example output:

```text id="r511vs"
dn: cn=admins,ou=groups,dc=example,dc=com
objectClass: posixGroup
cn: admins
gidNumber: 10001
memberUid: alice
```

Interpretation:

- jdoe can authenticate.
- However, jdoe is not listed as a member of admins.
- The problem is authorization, not authentication.

#### Fix

Add `jdoe` to the required group.

Example modify LDIF:

```ldif id="ooek8g"
dn: cn=admins,ou=groups,dc=example,dc=com
changetype: modify
add: memberUid
memberUid: jdoe
```

Apply:

```bash id="gv1ryy"
ldapmodify -x -D "cn=admin,dc=example,dc=com" -W -f add_jdoe_to_admins.ldif
```

### Scenario 10: Simulate Slow LDAP Searches

Understand how broad LDAP searches can become slow and how to inspect them.

#### Simulate the Problem

Run a broad search from the top of the directory:

```bash id="hcvpqu"
time ldapsearch -x -H ldap://localhost -b "dc=example,dc=com" "(objectClass=*)" > /tmp/all_ldap_entries.txt
```

Example output:

```text id="hgunhm"
real    0m4.820s
user    0m0.120s
sys     0m0.040s
```

#### Compare with a Narrow Search

```bash id="fghkka"
time ldapsearch -x -H ldap://localhost -b "ou=users,dc=example,dc=com" "(uid=jdoe)" uid cn
```

Example output:

```text id="bnyir8"
real    0m0.080s
user    0m0.020s
sys     0m0.010s
```

Interpretation:

- The broad search scans much more of the directory.
- The narrow search is faster because it uses a specific base DN and filter.
- If broad searches are common, applications may overload LDAP.

#### Fix Ideas

- use narrower base DNs
- use specific filters
- request only needed attributes
- index frequently searched attributes
- avoid repeated full-tree searches
- cache results where appropriate

Example better search:

```bash id="i81l4o"
ldapsearch -x -b "ou=users,dc=example,dc=com" "(uid=jdoe)" uid cn mail
```

This requests only selected attributes instead of everything.

### LDAP Troubleshooting Workflow

When LDAP fails, troubleshoot in layers.

1. Is the server running?
2. Is the port reachable?
3. Can the client bind?
4. Is the base DN correct?
5. Does the search filter match entries?
6. Are required attributes present?
7. Does NSS/PAM integration work?
8. Is TLS configured correctly?
9. Are access controls blocking the request?
10. Are logs showing errors?

### Step 1: Check Server Status

```bash id="b746c4"
systemctl status slapd
```

Expected healthy state:

```text id="w19xmr"
Active: active (running)
```

### Step 2: Check Listening Port

```bash id="psijwd"
ss -tulnp | grep slapd
```

Expected output:

```text id="mn203f"
tcp LISTEN 0 128 0.0.0.0:389 0.0.0.0:* users:(("slapd",pid=1200,fd=8))
```

If using LDAPS:

```text id="fxgt31"
port 636
```

### Step 3: Test Basic Connectivity

```bash id="gsixv6"
ldapwhoami -x -H ldap://localhost
```

Expected:

```text id="qetoo7"
anonymous
```

If this fails, check service status, firewall, port, URI, and network connectivity.

### Step 4: Test Authenticated Bind

```bash id="o3byxw"
ldapwhoami -x -D "cn=admin,dc=example,dc=com" -W -H ldap://localhost
```

Expected:

```text id="f90g1l"
dn:cn=admin,dc=example,dc=com
```

If this fails with invalid credentials, check the DN and password.

### Step 5: Test Search Base

```bash id="xu76e0"
ldapsearch -x -H ldap://localhost -b "dc=example,dc=com" "(objectClass=*)"
```

If the result is:

```text id="ae2mr7"
No such object
```

then the base DN may be wrong or missing.

### Step 6: Test Specific User Search

```bash id="tgw3ew"
ldapsearch -x -H ldap://localhost -b "ou=users,dc=example,dc=com" "(uid=jdoe)"
```

If `numEntries` is 0, the user may not exist or the filter is wrong.

### Step 7: Test Linux Account Resolution

```bash id="v7pkj9"
getent passwd jdoe
id jdoe
```

If LDAP search works but `getent` fails, check NSS, SSSD, nslcd, or PAM configuration.

### Step 8: Check Logs

Server logs may be available through systemd:

```bash id="dd7vf4"
journalctl -u slapd -b
```

Kernel-level or authentication logs may also help:

```bash id="jwz9ug"
journalctl -xe
sudo less /var/log/auth.log
```

Look for messages about:

- bind failures
- TLS errors
- schema violations
- access denied
- invalid DN syntax
- database errors

### Common LDAP Error Codes

- 0    Success
- 32   No such object
- 49   Invalid credentials
- 50   Insufficient access
- 68   Entry already exists
- 80   Other server-side error

Examples:

- Invalid credentials (49):
    - password or bind DN problem

- No such object (32):
    - base DN or target DN does not exist

- Insufficient access (50):
    - ACL or permission problem

- Entry already exists (68):
    - trying to add an entry that already exists

### Useful LDAP Command Summary

Connectivity:

```bash id="rbsld6"
ldapwhoami -x -H ldap://localhost
ldapwhoami -x -D "cn=admin,dc=example,dc=com" -W -H ldap://localhost
ldapwhoami -x -ZZ -H ldap://localhost
```

Search:

```bash id="yln5rd"
ldapsearch -x -b "dc=example,dc=com" "(objectClass=*)"
ldapsearch -x -b "ou=users,dc=example,dc=com" "(uid=jdoe)"
ldapsearch -x -b "ou=groups,dc=example,dc=com" "(cn=developers)"
```

Add, modify, delete:

```bash id="epn7fy"
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f entry.ldif
ldapmodify -x -D "cn=admin,dc=example,dc=com" -W -f modify.ldif
ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "uid=jdoe,ou=users,dc=example,dc=com"
```

Linux identity lookup:

```bash id="mska1c"
getent passwd jdoe
getent group developers
id jdoe
```

Server checks:

```bash id="id9uyw"
systemctl status slapd
ss -tulnp | grep slapd
journalctl -u slapd -b
```

Backup:

```bash id="bg2l3w"
slapcat > ldap-backup.ldif
```

### Practical Challenges

1. Install OpenLDAP on a test Linux system and configure the base domain as `dc=example,dc=com`.
2. Create organizational units for users, groups, and services.
3. Add at least three user entries using LDIF.
4. Add at least two groups and assign users to them.
5. Use `ldapsearch` to find users by `uid`, `mail`, and `objectClass`.
6. Use `ldapwhoami` to test anonymous and authenticated binds.
7. Configure a Linux client to resolve LDAP users with `getent passwd`.
8. Configure automatic home directory creation for LDAP users.
9. Enable StartTLS and test it with `ldapwhoami -ZZ`.
10. Simulate common LDAP issues: stopped server, wrong base DN, invalid credentials, missing POSIX attributes, TLS failure, and group authorization failure. For each issue, record the command used, output, interpretation, and fix.
