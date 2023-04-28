## LDAP (Lightweight Directory Access Protocol)

LDAP is an open, vendor-neutral application protocol used to manage and access distributed directory services over an IP network. It allows for storing and organizing data in a hierarchical manner, such as users, groups, and other resources. LDAP is commonly used for authentication and authorization purposes, as well as managing other types of directory-based data.

### Key Components

1. **Directory**: A hierarchical tree-like structure of entries, where each entry represents an object, such as a user, group, or organizational unit.
2. **Entry**: A collection of attributes that represent an object in the directory, such as a user, group, or device.
3. **Attribute**: A name-value pair that describes a characteristic of an entry, such as first name, email address, or phone number.
4. **Schema**: A set of rules that define the structure and types of entries, attributes, and the relationships between them.

### LDAP Operations

Common LDAP operations include:

1. **Bind**: Authenticate a user to the LDAP server.
2. **Search**: Retrieve information about entries in the directory.
3. **Add**: Create a new entry in the directory.
4. **Modify**: Update the attributes of an existing entry.
5. **Delete**: Remove an entry from the directory.

### LDAP Data Model

LDAP organizes data in a hierarchical manner using a tree-like structure called a Directory Information Tree (DIT). Each entry in the tree is identified by a unique string called a Distinguished Name (DN). The DN consists of one or more Relative Distinguished Names (RDNs), which are attribute-value pairs that uniquely identify an entry within its parent.

Example:

```
uid=jdoe,ou=people,dc=example,dc=com
```

In this example, `uid=jdoe` is the RDN of the user entry, and `ou=people,dc=example,dc=com` is the DN of the parent entry.

### LDAP Search Filters

To search for entries in an LDAP directory, you can use search filters. Filters are expressions that define the criteria an entry must meet to be included in the search results. Filters can be combined using logical operators like AND, OR, and NOT.

Example:

```
(&(objectClass=person)(uid=jdoe))
```

This filter would search for entries with the object class "person" and a user ID (uid) of "jdoe".

### LDAP Tools

There are several tools available to interact with LDAP directories, such as:

1. **ldapsearch**: A command-line tool for searching and retrieving information from an LDAP directory.
2. **ldapadd**: A command-line tool for adding new entries to an LDAP directory.
3. **ldapmodify**: A command-line tool for modifying existing entries in an LDAP directory.
4. **ldapdelete**: A command-line tool for deleting entries from an LDAP directory.
5. **JXplorer**: A graphical tool for browsing and managing LDAP directories.

### Example Scenario

A company wants to centralize the storage and management of employee information, such as names, email addresses, and phone numbers. They decide to implement an LDAP server to achieve this goal.

1. The company sets up an LDAP directory with a schema that defines user entries and their attributes, such as first name, last name, email address, and phone number.
2. The company adds entries for each employee to the directory.
3. Employees can use an LDAP client to search for and retrieve information about their colleagues.
4. Administrators can use LDAP tools to add, modify, or delete entries as needed.
5. The company can also use the LDAP directory for authentication and authorization purposes, such as granting access to specific resources based on group membership.

## Using LDAP for Centralized Authentication Across Multiple Servers

To enable centralized authentication for your users across multiple servers, you can set up an LDAP server to store and manage user credentials. This allows users to have the same credentials on all servers and simplifies the administration of user accounts.

### Steps to Implement LDAP for Centralized Authentication

1. **Set up an LDAP server**: Install OpenLDAP on a dedicated server or one of your existing servers.

```
sudo apt-get update
sudo apt-get install slapd ldap-utils
```

Reconfigure the slapd package to set the LDAP domain and admin password:

```
sudo dpkg-reconfigure slapd
```

2. **Define the schema**: Create an LDIF file containing the base structure for your directory, including the organization and organizational unit entries.

Example base.ldif:

```
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
```

Add the base structure to the LDAP directory:

```
sudo ldapadd -x -D "cn=admin,dc=example,dc=com" -w your_admin_password -f base.ldif
```

3. **Populate the directory**: Add entries for each user to the LDAP directory, including their credentials and any necessary attributes.

Example user.ldif:

```
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
uid: jdoe
cn: John Doe
givenName: John
sn: Doe
mail: jdoe@example.com
userPassword: {CLEARTEXT}your_password
```

Add the user entry to the LDAP directory:

```
sudo ldapadd -x -D "cn=admin,dc=example,dc=com" -w your_admin_password -f user.ldif
```

4. **Configure the servers to use LDAP for authentication**: On each of the three servers, install and configure the LDAP client to authenticate users against the LDAP server.

Install the necessary packages:

```
sudo apt-get install libnss-ldap libpam-ldap nscd
```

During installation, you'll be prompted for the LDAP server URI, search base, and admin credentials. Enter the appropriate information to configure the client.

Ensure that the client is configured to connect securely to the LDAP server by modifying the `/etc/ldap/ldap.conf` file:

```
TLS_REQCERT demand
```

5. **Test authentication**: Verify that users can log in to each server using their LDAP credentials. Ensure that access control is working as expected based on group membership or other relevant attributes.

6. **Maintain and update the directory**: As users are added, removed, or have their credentials changed, update the LDAP directory accordingly. Administrators can use LDAP tools (such as `ldapadd`, `ldapmodify`, or `ldapsearch`) to manage user entries.
