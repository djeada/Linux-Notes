## SELinux

SELinux stands for Security-Enhanced Linux.

It is a Linux security system that adds an extra layer of access control on top of normal Linux file permissions.

Traditional Linux permissions are based on users, groups, and file modes such as:

- owner
- group
- other

- read
- write
- execute

SELinux goes further. It controls what processes are allowed to do, even if normal Linux permissions would allow the action.

The main idea is:

```text id="vgn1kx"
Normal permissions ask:
Does this user have access?

SELinux asks:
Is this process type allowed to access this object type?
```

SELinux is especially useful on servers because it limits damage if a service is compromised.

For example, if a web server is hacked, SELinux can prevent the web server process from reading private user files, modifying system files, or accessing resources outside its allowed policy.

### DAC vs MAC

Linux normally uses Discretionary Access Control, or DAC.

SELinux adds Mandatory Access Control, or MAC.

- DAC = controlled by file owners and normal permissions
- MAC = controlled by system security policy

With DAC, a user who owns a file can usually decide who can read or write it.

With MAC, the system policy can still block access, even if the file owner gives permission.

Example:

- File permissions allow access.
- SELinux policy denies access.
- Result: access is denied.

This is one of the most important SELinux concepts.

SELinux does not replace normal permissions. Both must allow the action.

```text id="rfye0d"
Access allowed only if:

DAC allows it
AND
SELinux allows it
```

### Big Picture

SELinux labels processes and resources.

These labels are called security contexts.

When a process tries to access a file, socket, port, or other object, SELinux compares the process context with the object context and checks the loaded policy.

```text id="c1tqxl"
+-------------------+
| Process           |
| Example: httpd    |
| Context: httpd_t  |
+---------+---------+
          |
          | wants to read
          v
+-------------------+
| File              |
| /var/www/html     |
| Context:          |
| httpd_sys_content_t
+---------+---------+
          |
          v
+-------------------+
| SELinux Policy    |
| Is httpd_t allowed|
| to read           |
| httpd_sys_content_t?
+---------+---------+
          |
          v
+-------------------+
| Allow or Deny     |
+-------------------+
```

The key decision is usually based on the type.

For processes, the type is often called a domain.

For files and other objects, the type is usually just called a type.

- Process domain: httpd_t
- File type:      httpd_sys_content_t

SELinux policy defines what domains can do to what types.

### SELinux Architecture

A simplified SELinux architecture looks like this:

```text id="uccnxa"
+---------------------------------------------------+
|                   User Process                    |
|        Example: web server, SSH daemon, app       |
+----------------------+----------------------------+
                       |
                       | 1. Access request
                       |    read, write, execute,
                       |    bind port, connect socket
                       v
+---------------------------------------------------+
|             SELinux Security Server               |
|             Policy Decision Point                 |
|                                                   |
| Checks loaded policy and security contexts        |
+----------------------+----------------------------+
                       |
                       | 2. Allow or deny decision
                       v
+---------------------------------------------------+
|       Object Manager and Access Vector Cache      |
|       Policy Enforcement Point                    |
|                                                   |
| Enforces decision and caches previous results     |
+----------------------+----------------------------+
                       |
                       | 3. Operation allowed or blocked
                       v
+---------------------------------------------------+
|                  Linux Kernel                     |
+---------------------------------------------------+
```

The important parts are:

| Component                     | Description                                                             |
| ----------------------------- | ----------------------------------------------------------------------- |
| **Subject**                   | The process trying to perform an action.                                |
| **Object**                    | The resource being accessed.                                            |
| **Policy**                    | The SELinux rules that define permitted actions.                        |
| **Decision**                  | The result of policy evaluation: **allow** or **deny**.                 |
| **AVC (Access Vector Cache)** | Caches SELinux access decisions and records access denials for logging. |

### Subjects and Objects

A subject is usually a process.

Examples:

- sshd process
- httpd process
- nginx process
- named process
- mysqld process
- user shell process

An object is something the process tries to access.

Examples:

- file
- directory
- socket
- TCP port
- device
- pipe
- filesystem

Example:

```text id="v8dwwl"
Subject:
httpd process running as httpd_t

Object:
index.html labeled httpd_sys_content_t

Action:
read
```

SELinux checks whether `httpd_t` is allowed to read `httpd_sys_content_t`.

### SELinux Contexts

Every SELinux-labeled process and object has a security context.

A context usually has four parts:

```text id="n8yb2b"
SELinux user : role : type : level
```

Example file context:

```text id="sgetfu"
system_u:object_r:httpd_sys_content_t:s0
```

Breakdown:

| Component               | Description                                |
| ----------------------- | ------------------------------------------ |
| **system_u**            | SELinux user                               |
| **object_r**            | SELinux role for objects                   |
| **httpd_sys_content_t** | SELinux type (domain/type label)           |
| **s0**                  | Sensitivity level (MLS/MCS security level) |

The type is usually the most important part for everyday troubleshooting.

```text id="q2yyg7"
In most common SELinux troubleshooting:
focus on the type.
```

### Process Context Example

To view process contexts:

```bash id="muo5j3"
ps -eZ | grep sshd
```

Example output:

```text id="mr30yg"
system_u:system_r:sshd_t:s0-s0:c0.c1023  1234 ? 00:00:00 sshd
```

Interpretation:

- The sshd process is running in the sshd_t domain.
- SELinux policy controls what sshd_t can access.

### File Context Example

To view file contexts:

```bash id="c15tmz"
ls -Z /var/www/html/index.html
```

Example output:

```text id="irkgyi"
-rw-r--r--. root root system_u:object_r:httpd_sys_content_t:s0 /var/www/html/index.html
```

Interpretation:

- The file is labeled httpd_sys_content_t.
- This is a normal type for web content served by Apache or Nginx.

### Why Labels Matter

SELinux does not only care about file paths.

It cares strongly about labels.

For example, two files may have the same normal permissions:

```text id="latl1v"
-rw-r--r-- index.html
-rw-r--r-- secret.txt
```

But they may have different SELinux types:

```text id="xzi1bh"
index.html   httpd_sys_content_t
secret.txt   user_home_t
```

A web server may be allowed to read `httpd_sys_content_t` but denied access to `user_home_t`.

This means a file can be readable by Unix permissions but still blocked by SELinux.

### SELinux Modes

SELinux has three major modes:

- Enforcing
- Permissive
- Disabled

### Enforcing Mode

In enforcing mode, SELinux policy is active.

Unauthorized actions are blocked and logged.

```text id="g18ov8"
SELinux policy says deny
        |
        v
Action is blocked
        |
        v
Denial is logged
```

This is the normal recommended mode for production systems.

### Permissive Mode

In permissive mode, SELinux does not block actions, but it still logs what would have been denied.

```text id="h1lar2"
SELinux policy says deny
        |
        v
Action is allowed anyway
        |
        v
Denial is logged
```

Permissive mode is useful for troubleshooting because it lets you see SELinux problems without breaking the application.

It should usually be temporary.

### Disabled Mode

In disabled mode, SELinux is turned off.

No SELinux policy is enforced, and SELinux denials are not logged.

This is usually not recommended.

A key difference:

- Permissive:
- SELinux is active but not enforcing.

- Disabled:
- SELinux is not active.

Switching from disabled back to enabled may require relabeling the filesystem.

### Checking SELinux Mode

Use:

```bash id="hgk97p"
getenforce
```

Example outputs:

```text id="xn2ez9"
Enforcing
```

or:

```text id="w5vcno"
Permissive
```

or:

```text id="r0gbtz"
Disabled
```

For more detail:

```bash id="ky492l"
sestatus
```

Example output:

```text id="cxixy5"
SELinux status:                 enabled
Current mode:                   enforcing
Mode from config file:          enforcing
Policy name:                    targeted
```

Interpretation:

- SELinux is enabled.
- It is currently enforcing policy.
- The configured policy type is targeted.

### Temporarily Changing SELinux Mode

To switch to permissive mode temporarily:

```bash id="b0g8ze"
sudo setenforce 0
```

or:

```bash id="lq6f8g"
sudo setenforce Permissive
```

To switch back to enforcing:

```bash id="bqro73"
sudo setenforce 1
```

or:

```bash id="fqpisl"
sudo setenforce Enforcing
```

Verify:

```bash id="oyy9d7"
getenforce
```

Important:

- setenforce changes the mode only until reboot.
- It cannot enable SELinux if SELinux is disabled.

### Permanently Changing SELinux Mode

The main configuration file is:

```text id="i3df91"
/etc/selinux/config
```

Open it:

```bash id="i5ec2b"
sudo nano /etc/selinux/config
```

Example:

```text id="s07jqs"
SELINUX=enforcing
SELINUXTYPE=targeted
```

Possible `SELINUX` values:

- enforcing
- permissive
- disabled

A reboot is usually required for this file to fully take effect.

Use caution before setting SELinux to disabled.

### SELinux Policy Types

SELinux policy defines the rules.

Common policy types include:

- targeted
- strict
- MLS/MCS-based policies

For most systems, the common policy is:

```text id="hge8b0"
targeted
```

### Targeted Policy

Targeted policy confines selected services while allowing many normal user processes to run unconfined.

This is the default on many SELinux-enabled distributions.

Examples of commonly confined services:

- httpd
- sshd
- named
- mysqld
- postgresql
- samba
- ftp

Targeted policy is a good balance between security and usability.

### Strict Policy

Strict policy applies SELinux controls much more broadly.

It can provide stronger confinement but requires much more planning and administration.

It is more likely to break normal workflows if not carefully configured.

For most learners and administrators, targeted policy is the practical starting point.

### Common SELinux Tools

Useful commands include:

- getenforce
- sestatus
- setenforce
- ls -Z
- ps -eZ
- chcon
- restorecon
- semanage
- getsebool
- setsebool
- ausearch
- sealert
- audit2why
- audit2allow
- semodule

Some commands may require packages such as:

- policycoreutils
- policycoreutils-python-utils
- setroubleshoot
- audit

Package names vary by distribution.

### Viewing Contexts

View file context:

```bash id="znnqe7"
ls -Z /path/to/file
```

View directory context:

```bash id="rk5od6"
ls -Zd /path/to/directory
```

Example:

```bash id="i7r0k5"
ls -Zd /var/www/html
```

Output:

```text id="r1z2dy"
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 /var/www/html
```

View process context:

```bash id="psuu6z"
ps -eZ | grep httpd
```

or:

```bash id="wt7d6z"
ps -eZ | grep nginx
```

Example:

```text id="r6jpar"
system_u:system_r:httpd_t:s0  2345 ? 00:00:00 nginx
```

Interpretation:

```text id="xjqgpx"
The web service process is running in the httpd_t domain.
```

Some systems label Apache and Nginx web server processes using the same SELinux domain family, such as `httpd_t`.

Always check your actual system with `ps -eZ`.

### Changing Contexts with `chcon`

The `chcon` command changes a file or directory context directly.

Example:

```bash id="l7i0um"
sudo chcon -t httpd_sys_content_t /srv/mywebsite/index.html
```

This changes only the type.

To apply recursively:

```bash id="abz7en"
sudo chcon -R -t httpd_sys_content_t /srv/mywebsite
```

Important:

- chcon changes are immediate.
- chcon changes may be lost after restorecon or relabeling.

Use `chcon` for quick tests, not usually for permanent configuration.

### Restoring Default Contexts with `restorecon`

The `restorecon` command restores files to their expected default SELinux context based on policy rules.

Example:

```bash id="ncyzzw"
sudo restorecon -Rv /var/www/html
```

Options:

- -R   recursive
- -v   verbose

Example output:

```text id="j5co9b"
Relabeled /var/www/html/index.html from unconfined_u:object_r:default_t:s0 to system_u:object_r:httpd_sys_content_t:s0
```

Interpretation:

- The file had the wrong context.
- restorecon changed it back to the expected web content context.

### Persistent Context Rules with `semanage fcontext`

For custom directories, use `semanage fcontext`.

Example:

```bash id="g3m8wx"
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/mywebsite(/.*)?"
```

Then apply it:

```bash id="yck1zu"
sudo restorecon -Rv /srv/mywebsite
```

This is the correct persistent approach for custom paths.

- semanage fcontext defines the rule.
- restorecon applies the rule.

### `chcon` vs `semanage fcontext`

chcon:
- quick manual label change
- useful for testing
- not persistent against relabeling

semanage fcontext:
- persistent label rule
- survives restorecon
- best for permanent custom paths

A good rule:

- Use chcon to test.
- Use semanage fcontext for permanent fixes.

### SELinux Booleans

SELinux booleans are policy switches.

They let administrators adjust policy behavior without writing a new policy module.

List all booleans:

```bash id="tjtd1v"
getsebool -a
```

Filter for web server booleans:

```bash id="vm7czz"
getsebool -a | grep httpd
```

Example output:

```text id="t8v1y2"
httpd_can_network_connect --> off
httpd_enable_homedirs --> off
httpd_read_user_content --> off
```

Interpretation:

- These booleans control optional web server permissions.
- Currently, these permissions are disabled.

### Temporarily Changing a Boolean

Example:

```bash id="h0q6bh"
sudo setsebool httpd_can_network_connect on
```

This applies until reboot.

### Permanently Changing a Boolean

Use `-P`:

```bash id="qa8xzr"
sudo setsebool -P httpd_can_network_connect on
```

The `-P` option makes it persistent.

Common booleans:

- httpd_can_network_connect      allow web server scripts to make network connections
- httpd_enable_homedirs          allow web server to serve user home directories
- ftp_home_dir                   allow FTP access to user home directories
- samba_enable_home_dirs         allow Samba access to home directories

Only enable booleans that are actually needed.

### SELinux Ports

SELinux can also control which services may bind to which network ports.

For example, a web server is normally allowed to bind to ports labeled as HTTP ports.

View HTTP port mappings:

```bash id="aapobw"
sudo semanage port -l | grep http_port_t
```

Example output:

```text id="ced7m3"
http_port_t    tcp    80, 81, 443, 488, 8008, 8009, 8443
```

Interpretation:

- Services running in the web server domain may bind to these ports.
- A custom port may need to be added.

Add a custom HTTP port:

```bash id="v77dwp"
sudo semanage port -a -t http_port_t -p tcp 8081
```

If the port already exists under another type, modify instead:

```bash id="dkbs6e"
sudo semanage port -m -t http_port_t -p tcp 8081
```

### Audit Logs and AVC Denials

SELinux denials are usually logged as AVC messages.

AVC means Access Vector Cache.

Main log location:

```text id="vtog7v"
/var/log/audit/audit.log
```

Search for SELinux denials from today:

```bash id="qzib85"
sudo ausearch -m avc -ts today
```

Search by command name:

```bash id="lfng6i"
sudo ausearch -m avc -c nginx
```

or:

```bash id="ibtixf"
sudo ausearch -m avc -c httpd
```

Example AVC denial:

```text id="og5l29"
type=AVC msg=audit(1609459200.123:456): avc:  denied  { read } for  pid=1234 comm="nginx" name="index.html" dev="sda1" ino=56789 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
```

Breakdown:

- denied { read }                 the blocked action was read
- pid=1234                        process ID
- comm="nginx"                    command name
- name="index.html"               object name
- scontext=...:httpd_t:s0         source/process context
- tcontext=...:default_t:s0       target/file context
- tclass=file                     target object class

Interpretation:

- A process in httpd_t tried to read a file labeled default_t.
- SELinux denied the read.
- The file probably has the wrong label for web content.

### Explaining Denials with `audit2why`

Use:

```bash id="rycthe"
sudo ausearch -m avc -ts today | audit2why
```

Example output:

```text id="kde1nc"
type=AVC ... denied { read } ...
Was caused by:
Missing type enforcement rule.
```

Interpretation:

- SELinux policy does not allow this process type to access this object type.
- Fix the label, boolean, port type, or policy depending on the case.

### Using `sealert`

If `setroubleshoot` is installed:

```bash id="e6588j"
sudo sealert -a /var/log/audit/audit.log
```

`sealert` can provide human-readable explanations and suggested fixes.

Use it as guidance, but do not blindly apply every suggestion.

### Custom Policies with `audit2allow`

As a last resort, you can generate a custom policy module from audit logs.

Example:

```bash id="va266v"
sudo grep nginx /var/log/audit/audit.log | audit2allow -M nginx_custom
sudo semodule -i nginx_custom.pp
```

Important warning:

- Do not blindly install audit2allow-generated policies.
- First check whether the real problem is a wrong file label, wrong port label, missing boolean, or bad application design.

A custom policy should be reviewed carefully.

### Standard SELinux Troubleshooting Workflow

When something fails and SELinux may be involved:

1. Confirm the normal Linux permissions.
2. Check SELinux mode.
3. Check source process context.
4. Check target file, directory, or port context.
5. Search AVC denials.
6. Interpret the denial.
7. Fix the label, boolean, port type, or policy.
8. Retest.
9. Avoid disabling SELinux as the first fix.

Useful commands:

```bash id="btfxtj"
getenforce
sestatus
ls -Z path
ps -eZ | grep service
sudo ausearch -m avc -ts recent
sudo restorecon -Rv path
sudo semanage fcontext -a -t TYPE "PATH_REGEX"
sudo setsebool -P boolean_name on
```

### Scenario 1: Check SELinux Mode and Temporarily Switch to Permissive

#### Goal

Learn how to check and temporarily change SELinux enforcement.

#### Check Mode

```bash id="j4t4zn"
getenforce
```

Example output:

```text id="l4ypd5"
Enforcing
```

#### Simulate Troubleshooting Mode

```bash id="lunhrz"
sudo setenforce 0
getenforce
```

Example output:

```text id="eufki1"
Permissive
```

#### Interpretation

- SELinux is still enabled.
- It will log policy violations but will not block them.
- This is useful for troubleshooting.

#### Restore Enforcing Mode

```bash id="vhf6vk"
sudo setenforce 1
getenforce
```

Expected output:

```text id="dzbi6w"
Enforcing
```

#### Important Lesson

- Permissive mode is a diagnostic tool.
- It should not be used as a permanent fix on production systems.

### Scenario 2: Simulate a Web Server File Context Problem

#### Goal

Show how a service can fail because files have the wrong SELinux label.

#### Situation

A web server is configured to serve files from:

```text id="fygor9"
/srv/mywebsite
```

The file permissions are correct, but the site returns:

```text id="bd474v"
403 Forbidden
```

or the service logs show access denied.

#### Simulate the Problem

Create test content:

```bash id="a5jef1"
sudo mkdir -p /srv/mywebsite
echo "Hello from SELinux test" | sudo tee /srv/mywebsite/index.html
```

Check context:

```bash id="g3f13z"
ls -Z /srv/mywebsite/index.html
```

Example output:

```text id="sl8pc0"
-rw-r--r--. root root unconfined_u:object_r:default_t:s0 /srv/mywebsite/index.html
```

#### Interpretation

- The file is labeled default_t.
- A web server process running as httpd_t is usually not allowed to read default_t.
- This can cause access denial even when normal permissions look correct.

#### Check AVC Denial

```bash id="z5qyod"
sudo ausearch -m avc -ts recent -c nginx
```

or:

```bash id="ehcxa5"
sudo ausearch -m avc -ts recent -c httpd
```

Example output:

```text id="ihbcm0"
type=AVC msg=audit(...): avc:  denied  { open } for  pid=1234 comm="nginx" path="/srv/mywebsite/index.html" scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
```

#### Interpretation

- The web server process is httpd_t.
- The file is default_t.
- SELinux denied file open.
- The likely fix is to label the directory as web content.

#### Temporary Test Fix with `chcon`

```bash id="g47r77"
sudo chcon -R -t httpd_sys_content_t /srv/mywebsite
ls -Z /srv/mywebsite/index.html
```

Expected context:

```text id="xv06yw"
unconfined_u:object_r:httpd_sys_content_t:s0
```

#### Permanent Fix with `semanage fcontext`

```bash id="gdfvkw"
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/mywebsite(/.*)?"
sudo restorecon -Rv /srv/mywebsite
```

Example output:

```text id="wdpw86"
Relabeled /srv/mywebsite/index.html from unconfined_u:object_r:default_t:s0 to system_u:object_r:httpd_sys_content_t:s0
```

#### Final Interpretation

- The content now has the correct SELinux type.
- The web server should be allowed to read it.
- This fixes the root SELinux labeling problem.

### Scenario 3: Demonstrate `chcon` Is Temporary

#### Goal

Show why `chcon` is not the best permanent fix.

#### Simulate

```bash id="fec4w0"
sudo chcon -R -t httpd_sys_content_t /srv/mywebsite
ls -Z /srv/mywebsite/index.html
```

Example output:

```text id="s3vui0"
unconfined_u:object_r:httpd_sys_content_t:s0 index.html
```

Now run:

```bash id="uwbcl6"
sudo restorecon -Rv /srv/mywebsite
```

If no persistent `semanage fcontext` rule exists, example output may show:

```text id="p5s9mq"
Relabeled /srv/mywebsite/index.html from unconfined_u:object_r:httpd_sys_content_t:s0 to unconfined_u:object_r:default_t:s0
```

#### Interpretation

- restorecon reverted the file to the default label for that path.
- The chcon change did not define a permanent labeling rule.

#### Permanent Fix

```bash id="uqwij5"
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/mywebsite(/.*)?"
sudo restorecon -Rv /srv/mywebsite
```

#### Lesson

- chcon changes labels.
- semanage fcontext changes the labeling rule.
- restorecon applies labeling rules.

### Scenario 4: Simulate a Web Server Network Connection Denied by Boolean

#### Goal

Show how SELinux booleans control optional service behavior.

#### Situation

A web application needs to connect from the web server to a backend service or database over the network.

The application fails even though networking and firewall rules are correct.

#### Check Boolean

```bash id="eq1ghg"
getsebool httpd_can_network_connect
```

Example output:

```text id="qm1440"
httpd_can_network_connect --> off
```

#### Check AVC Denial

```bash id="in5kii"
sudo ausearch -m avc -ts recent | grep name_connect
```

Example output:

```text id="lju6rh"
avc:  denied  { name_connect } for  pid=2222 comm="nginx" dest=5432 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:postgresql_port_t:s0 tclass=tcp_socket
```

#### Interpretation

- The web server process tried to make an outbound network connection.
- SELinux denied name_connect.
- The boolean httpd_can_network_connect may be required.

#### Fix

Temporarily:

```bash id="uz360r"
sudo setsebool httpd_can_network_connect on
```

Persistently:

```bash id="avhtjs"
sudo setsebool -P httpd_can_network_connect on
```

Verify:

```bash id="ihffru"
getsebool httpd_can_network_connect
```

Expected output:

```text id="d92t24"
httpd_can_network_connect --> on
```

#### Lesson

```text id="s087er"
Booleans are safer than custom policy when the policy already provides a supported switch.
```

### Scenario 5: Simulate a Service Binding to a Nonstandard Port

#### Goal

Show how SELinux controls network port usage.

#### Situation

A web server is configured to listen on port:

```text id="td89my"
8081
```

The service fails to start.

#### Check Logs

```bash id="sl8ms3"
sudo ausearch -m avc -ts recent | grep name_bind
```

Example output:

```text id="aue8od"
avc: denied { name_bind } for pid=3333 comm="nginx" src=8081 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:unreserved_port_t:s0 tclass=tcp_socket
```

#### Interpretation

```text id="z2c0n1"
The web server tried to bind to TCP port 8081.
SELinux does not currently label that port as an allowed HTTP port.
```

#### Check Allowed HTTP Ports

```bash id="k7tl4y"
sudo semanage port -l | grep http_port_t
```

Example output:

```text id="hlsp2p"
http_port_t tcp 80, 81, 443, 488, 8008, 8009, 8443
```

#### Fix

Add port 8081 as an HTTP port:

```bash id="ucn4pv"
sudo semanage port -a -t http_port_t -p tcp 8081
```

Verify:

```bash id="zo7t2s"
sudo semanage port -l | grep http_port_t
```

Expected output includes:

```text id="q63qdd"
8081
```

Restart service:

```bash id="fz208c"
sudo systemctl restart nginx
```

or:

```bash id="rxivz4"
sudo systemctl restart httpd
```

#### Lesson

- If a confined service uses a nonstandard port, label the port correctly.
- Do not disable SELinux just because a port changed.

### Scenario 6: Simulate FTP Access to Home Directories Blocked by SELinux

#### Goal

Show how booleans can allow or deny service access to user home directories.

#### Situation

FTP login works, but users cannot access files in their home directories.

#### Check Boolean

```bash id="k7qz5z"
getsebool ftp_home_dir
```

Example output:

```text id="zwlw6l"
ftp_home_dir --> off
```

#### Check AVC Denial

```bash id="w4f05e"
sudo ausearch -m avc -ts recent -c vsftpd
```

Example output:

```text id="x6i3wi"
avc: denied { read } for pid=4444 comm="vsftpd" name="notes.txt" scontext=system_u:system_r:ftpd_t:s0 tcontext=unconfined_u:object_r:user_home_t:s0 tclass=file
```

#### Interpretation

- The FTP service is running in ftpd_t.
- The file is labeled user_home_t.
- SELinux policy blocks FTP from reading home directory files unless allowed.

#### Fix

```bash id="txknmn"
sudo setsebool -P ftp_home_dir on
```

Verify:

```bash id="idtot0"
getsebool ftp_home_dir
```

Expected output:

```text id="w2z171"
ftp_home_dir --> on
```

#### Lesson

```text id="dj6i48"
SELinux booleans allow common optional behaviors without writing custom policy.
```

### Scenario 7: Simulate Permissive Mode Logging

#### Goal

Understand the difference between permissive and enforcing behavior.

#### Step 1: Put SELinux in Permissive Mode

```bash id="b8fpi0"
sudo setenforce 0
getenforce
```

Expected output:

```text id="kk09y1"
Permissive
```

#### Step 2: Trigger a Known SELinux Issue

For example, use a web content file with the wrong label:

```bash id="e0gfps"
sudo chcon -R -t default_t /srv/mywebsite
```

Access it through the web server.

#### Step 3: Check Logs

```bash id="vxw908"
sudo ausearch -m avc -ts recent
```

Example output:

```text id="sj46yf"
avc: denied { read } for pid=1234 comm="nginx" path="/srv/mywebsite/index.html" scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file permissive=1
```

#### Interpretation

- The denial was logged.
- permissive=1 means the action was allowed because SELinux is in permissive mode.
- In enforcing mode, this would likely be blocked.

#### Restore Enforcing Mode

```bash id="r63r0i"
sudo setenforce 1
```

#### Lesson

- Permissive mode helps find policy problems before enforcing them.
- It is useful during troubleshooting and policy development.

### Scenario 8: Diagnose “Permission Denied” When Unix Permissions Look Correct

#### Goal

Show the standard SELinux troubleshooting pattern.

#### Situation

A service fails with:

```text id="srzymi"
Permission denied
```

But normal permissions look correct:

```bash id="k17sxu"
ls -l /srv/mywebsite/index.html
```

Example output:

```text id="qqi7hz"
-rw-r--r--. root root 25 Jun 1 12:00 /srv/mywebsite/index.html
```

#### Step 1: Check SELinux Mode

```bash id="rgz7lq"
getenforce
```

Example:

```text id="vf6jkp"
Enforcing
```

#### Step 2: Check File Context

```bash id="r84cjh"
ls -Z /srv/mywebsite/index.html
```

Example:

```text id="t2024a"
unconfined_u:object_r:default_t:s0 index.html
```

#### Step 3: Check Process Context

```bash id="yrk2y6"
ps -eZ | grep nginx
```

Example:

```text id="yq5w0y"
system_u:system_r:httpd_t:s0  1234 ? 00:00:00 nginx
```

#### Step 4: Check AVC Logs

```bash id="s5fsnm"
sudo ausearch -m avc -ts recent -c nginx
```

Example:

```text id="c53fed"
avc: denied { read } for comm="nginx" scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
```

#### Interpretation

- Unix permissions allow reading.
- SELinux denies reading because the file type is default_t.
- The correct fix is to label the file as web content.

#### Fix

```bash id="obhagq"
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/mywebsite(/.*)?"
sudo restorecon -Rv /srv/mywebsite
```

### Scenario 9: Use `audit2why` Before Making Changes

#### Goal

Use audit tools to understand denials before fixing them.

#### Search and Explain

```bash id="pzh520"
sudo ausearch -m avc -ts recent | audit2why
```

Example output:

```text id="sjbn9e"
type=AVC ... denied { read } ...
Was caused by:
Missing type enforcement rule.

Possible mismatch between source and target contexts.
```

#### Interpretation

- The tool confirms SELinux policy blocked the action.
- Before creating a policy module, check whether the target has the wrong label.

#### Good Fix Order

1. Fix wrong labels.
2. Enable correct booleans.
3. Fix port labels.
4. Only then consider custom policy.

### Scenario 10: Generate a Custom Policy Only as a Last Resort

#### Goal

Understand how custom policy modules are created and why they require caution.

#### Simulate

Suppose a custom application `myapp` is denied access and there is no existing boolean or label fix.

Collect relevant denials:

```bash id="m2ma96"
sudo ausearch -m avc -ts recent -c myapp
```

Generate a policy module:

```bash id="sgpj88"
sudo ausearch -m avc -ts recent -c myapp | audit2allow -M myapp_local
```

This creates files such as:

- myapp_local.te
- myapp_local.pp

Inspect the `.te` file before installing:

```bash id="fxbd02"
cat myapp_local.te
```

Example rule:

```text id="dhv1wy"
allow myapp_t var_log_t:file read;
```

#### Interpretation

- The generated policy would allow myapp_t to read files labeled var_log_t.
- You must decide whether this access is actually appropriate.

Install only after review:

```bash id="eszwbk"
sudo semodule -i myapp_local.pp
```

#### Lesson

- audit2allow can solve problems by allowing more access.
- That can also weaken security if used carelessly.
- Review every generated rule.

### Scenario 11: Full Troubleshooting Example for Custom Web Directory

#### Goal

Perform a complete SELinux troubleshooting workflow.

#### Symptom

A web server returns:

```text id="z9iw4t"
403 Forbidden
```

for content under:

```text id="pj9ta3"
/srv/mywebsite
```

#### Check Normal Permissions

```bash id="s3n1sj"
ls -ld /srv/mywebsite
ls -l /srv/mywebsite/index.html
```

Example:

```text id="k4y88m"
drwxr-xr-x. root root /srv/mywebsite
-rw-r--r--. root root index.html
```

Interpretation:

- Normal permissions appear readable.
- The problem may be SELinux or web server configuration.

#### Check SELinux Mode

```bash id="lb7kt7"
getenforce
```

Example:

```text id="ozidmg"
Enforcing
```

#### Check Context

```bash id="rn4ewc"
ls -Zd /srv/mywebsite
ls -Z /srv/mywebsite/index.html
```

Example:

```text id="i1ey6e"
unconfined_u:object_r:default_t:s0 /srv/mywebsite
unconfined_u:object_r:default_t:s0 /srv/mywebsite/index.html
```

#### Check Denials

```bash id="wkmn3m"
sudo ausearch -m avc -ts recent -c nginx
```

Example:

```text id="a6dmvm"
avc: denied { getattr open read } for comm="nginx" path="/srv/mywebsite/index.html" scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
```

#### Interpret

- The web server process is httpd_t.
- The target file is default_t.
- SELinux denied access.
- The file needs a web content context.

#### Fix Permanently

```bash id="jrelci"
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/mywebsite(/.*)?"
sudo restorecon -Rv /srv/mywebsite
```

#### Verify

```bash id="iamfbe"
ls -Z /srv/mywebsite/index.html
```

Expected:

```text id="igvnrq"
system_u:object_r:httpd_sys_content_t:s0 index.html
```

#### Retest

Restart or reload the web service if needed:

```bash id="m3fve5"
sudo systemctl reload nginx
```

or:

```bash id="fxwyjq"
sudo systemctl reload httpd
```

Then test the page again.

#### Check for Remaining Denials

```bash id="d8f33p"
sudo ausearch -m avc -ts recent -c nginx
```

If no new denial appears, the SELinux labeling issue is resolved.

### Scenario 12: Relabel a Filesystem After SELinux Was Disabled

#### Goal

Understand why relabeling may be needed after SELinux has been disabled.

#### Situation

SELinux was disabled for a while, then re-enabled. Some files may not have correct labels.

#### Safe Relabel Trigger

Create the autorelabel marker:

```bash id="yawqap"
sudo touch /.autorelabel
sudo reboot
```

During boot, the system relabels files according to SELinux policy.

#### Interpretation

- Relabeling restores expected SELinux contexts.
- This can take time on large filesystems.
- It is often needed when enabling SELinux after it has been disabled.

#### Caution

- Plan relabeling during maintenance time.
- A full relabel can slow boot.

### Common SELinux Problems and Fixes

#### Problem: File Has Wrong Context

Symptoms:

- service gets permission denied
- Unix permissions look correct
- AVC denial shows target type default_t or user_home_t

Check:

```bash id="nigcwz"
ls -Z path
sudo ausearch -m avc -ts recent
```

Fix:

```bash id="go8rbd"
sudo restorecon -Rv path
```

or for custom paths:

```bash id="rpgot0"
sudo semanage fcontext -a -t correct_type "path_regex"
sudo restorecon -Rv path
```

### Problem: Service Needs Optional Access

Symptoms:

- service works partly
- AVC denial suggests network connect, home directory access, or similar optional behavior

Check booleans:

```bash id="qd9qlh"
getsebool -a | grep service_name
```

Fix:

```bash id="c8ejaq"
sudo setsebool -P boolean_name on
```

### Problem: Service Uses Nonstandard Port

Symptoms:

- service cannot bind to custom port
- AVC denial includes name_bind

Check:

```bash id="vcm34s"
sudo semanage port -l | grep service_port_type
```

Fix:

```bash id="zlv5mv"
sudo semanage port -a -t correct_port_type -p tcp PORT
```

### Problem: SELinux Denial but No Audit Logs

Possible causes:

- auditd is not running
- logs are elsewhere
- denials are being rate-limited
- SELinux is disabled
- the issue is not SELinux

Check:

```bash id="m96d8p"
getenforce
sudo systemctl status auditd
sudo journalctl -t setroubleshoot
sudo dmesg | grep -i avc
```

### Problem: Someone Suggests “Just Disable SELinux”

Better approach:

- Do not disable SELinux first.
- Check the denial.
- Understand the source and target contexts.
- Fix labels, booleans, or port types.
- Use permissive mode only temporarily for diagnosis.

Disabling SELinux removes a major security layer.

### Useful Command Summary

Mode and status:

```bash id="hq6x8y"
getenforce
sestatus
sudo setenforce 0
sudo setenforce 1
```

View contexts:

```bash id="rhkyot"
ls -Z file
ls -Zd directory
ps -eZ
ps -eZ | grep service
```

Fix file contexts:

```bash id="tqxqxp"
sudo chcon -t TYPE file
sudo restorecon -Rv path
sudo semanage fcontext -a -t TYPE "path_regex"
sudo restorecon -Rv path
```

Booleans:

```bash id="r99tgz"
getsebool -a
getsebool -a | grep httpd
sudo setsebool boolean_name on
sudo setsebool -P boolean_name on
```

Ports:

```bash id="u0lhx4"
sudo semanage port -l
sudo semanage port -l | grep http_port_t
sudo semanage port -a -t http_port_t -p tcp 8081
sudo semanage port -m -t http_port_t -p tcp 8081
```

Audit and troubleshooting:

```bash id="zz4ezr"
sudo ausearch -m avc -ts today
sudo ausearch -m avc -ts recent
sudo ausearch -m avc -c nginx
sudo ausearch -m avc -ts recent | audit2why
sudo sealert -a /var/log/audit/audit.log
```

Custom policy:

```bash id="og2o5o"
sudo ausearch -m avc -ts recent -c myapp | audit2allow -M myapp_local
cat myapp_local.te
sudo semodule -i myapp_local.pp
```

Relabeling:

```bash id="w4kc15"
sudo touch /.autorelabel
sudo reboot
```

### Safe Lab Rules

SELinux labs should be done carefully.

- Use a test VM if possible.
- Do not disable SELinux as a first troubleshooting step.
- Prefer permissive mode for temporary diagnosis.
- Record every change you make.
- Use restorecon to undo incorrect labels.
- Review audit2allow output before installing custom policy.
- Be careful with recursive chcon on large or important directories.

### Practical Challenges

1. Use `getenforce` and `sestatus` to check SELinux mode, policy type, and status.
2. Use `ls -Z` and `ps -eZ` to compare file contexts and process contexts.
3. Create a test directory under `/srv/mywebsite`, add an `index.html` file, and inspect its default SELinux context.
4. Change a file context with `chcon`, then run `restorecon` and observe whether the context changes back.
5. Add a persistent context rule with `semanage fcontext`, apply it with `restorecon`, and verify the result with `ls -Z`.
6. Search for recent AVC denials with `ausearch -m avc -ts recent`.
7. Use `audit2why` to explain an SELinux denial.
8. List web-related booleans with `getsebool -a | grep httpd`, then explain what `httpd_can_network_connect` does.
9. Add a custom HTTP port with `semanage port`, then verify it appears under `http_port_t`.
10. Write a short troubleshooting report for one SELinux denial. Include the symptom, mode, process context, file or port context, AVC output, interpretation, and fix.
