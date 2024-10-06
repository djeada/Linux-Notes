## SELinux

Security-Enhanced Linux (SELinux) is a robust security module integrated into the Linux kernel that provides a mechanism for supporting access control security policies. Unlike traditional discretionary access control (DAC) systems where users have control over their own files and processes, SELinux implements mandatory access control (MAC), ensuring that the system enforces security policies regardless of user actions. 

SELinux works by assigning labels, or security contexts, to all processes and objects (like files and sockets) on the system. These contexts are then used to make decisions about whether a process can access a resource. By enforcing least privilege, SELinux confines user programs and system services to the minimum required permissions, greatly reducing the potential damage from malicious or misconfigured software.

Developed by the United States National Security Agency (NSA) and released to the open-source community, SELinux has become a cornerstone of Linux security, particularly in environments where security is paramount, such as servers handling sensitive data or systems exposed to the internet.

### Overview of SELinux Architecture

Understanding the architecture of SELinux is key to leveraging its full potential. SELinux operates within the kernel and works alongside existing Linux security mechanisms to enforce its policies.

#### Architecture Diagram

```
+---------------------------------------------------+
|                   User Process                    |
|             (e.g., Web Server, SSH Daemon)        |
+----------------------+----------------------------+
                           |
                           | 1. Access Request (Read/Write)
                           v
+----------------------+----------------------------+
|               SELinux Security Server             |
|          (Policy Decision Point - PDP)            |
+----------------------+----------------------------+
                           |
                           | 2. Policy Decision (Allow/Deny)
                           v
+----------------------+----------------------------+
|          SELinux Object Manager and AVC           |
|          (Policy Enforcement Point - PEP)         |
+----------------------+----------------------------+
                           |
                           | 3. Enforce Decision
                           v
+----------------------+----------------------------+
|                    Linux Kernel                   |
|             (Executes Allowed Operations)         |
+---------------------------------------------------+
```

#### Detailed Explanation

I. User Process (Subject):

- Any running application or service, such as a web server (`httpd`), an SSH daemon (`sshd`), or a user application.
- The process attempts to perform an action, like reading a file, writing to a socket, or executing a program.
- This action is considered an access request to an object (resource).

II. SELinux Security Server (Policy Decision Point - PDP):

- Intercepts the access request and consults the loaded SELinux policies.
- Determines whether the requested action is permitted based on the security contexts of the subject and object.
- Allow or Deny.

III. SELinux Object Manager and Access Vector Cache (AVC) (Policy Enforcement Point - PEP):

- Enforces the policy decision by either permitting or denying the action.
- Caches previous decisions to optimize performance, reducing the overhead of policy checks.

IV. Linux Kernel:

- If the action is allowed, the kernel proceeds to execute the operation.
- If denied, the kernel blocks the operation and logs the denial.

### SELinux Modes of Operation

SELinux can operate in different modes, allowing administrators to balance security enforcement with system usability.

| **Mode**           | **Description**                                                                                         | **Behavior**                                                                                  | **Use Cases**                                                                                               |
|--------------------|---------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Enforcing Mode**  | SELinux policies are actively enforced. Unauthorized access attempts are blocked, and denials are logged.| - Denied actions are prevented from occurring. <br> - Denials are logged to audit logs.        | - Production environments where security is critical. <br> - Systems that have been properly configured.     |
| **Permissive Mode** | SELinux policies are not enforced, but violations are logged. Allows all actions but records denials.    | - Actions that violate policies are allowed. <br> - Denials are logged for troubleshooting.    | - Debugging and policy development. <br> - Temporarily used when adjusting system configurations.            |
| **Disabled Mode**   | SELinux is completely turned off. No policies are loaded or enforced, and no logging occurs.             | - All SELinux functions are disabled. <br> - System relies on traditional UNIX permissions.    | - Not recommended due to security risks. <br> - May be used where SELinux compatibility is an issue.         |

#### Mode Comparison Table

```
+------------------+------------------+------------------+
|  Enforcing Mode  | Permissive Mode  |  Disabled Mode   |
+------------------+------------------+------------------+
| Policies Enforced| Policies Not     | Policies Not     |
|                  | Enforced         | Loaded           |
| Denials Blocked  | Denials Logged   | No SELinux       |
| and Logged       |                  | Functionality    |
+------------------+------------------+------------------+
```

**Note:** Switching between modes can impact system security and functionality. Always ensure that mode changes are intentional and understood.

### SELinux Policy Types

SELinux policies define the rules that govern how processes and resources interact. There are two main policy types:

| **Policy**       | **Description**                                                                                                     | **Behavior**                                                                                                 | **Use Cases**                                                                                               |
|------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Strict Policy** | Applies SELinux rules to all processes, including user-level and system processes, enforcing security on all aspects.| - Enforces security policies on all processes, whether system or user. <br> - More comprehensive and restrictive. | - High-security environments where every process needs to be secured. <br> - Systems requiring detailed security control. |
| **Targeted Policy** | Applies SELinux rules only to specific targeted processes (e.g., system services), while other processes run unconfined. | - Only critical system services are restricted by SELinux. <br> - Non-targeted processes run without SELinux restrictions. | - Default policy in many Linux distributions. <br> - Systems where a balance between security and ease of use is needed. |

- **Targeted Policy** is recommended for most users due to its balance between security and usability.
- **Strict Policy** offers more security but requires extensive configuration and may impact system functionality.

### SELinux Contexts and Labels

SELinux uses security contexts (also known as labels) to make decisions about access control. Every object and process in the system has a context consisting of:

| **Component**      | **Description**                                                                                               | **Details**                                                                                                    |
|--------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **User Identity**   | Represents the SELinux user, which may differ from the UNIX user.                                              | - Controls the roles a user can assume.                                                                       |
| **Role**           | Defines what domains a user or process can enter.                                                              | - Common roles include `system_r` for system processes and `object_r` for objects.                            |
| **Type (Domain)**  | The most critical part for access control.                                                                     | - Types are assigned to objects, and domains are types assigned to processes. <br> - Policies define domain access to types. |
| **Level**          | Used in Multi-Level Security (MLS) and Multi-Category Security (MCS).                                           | - Defines the sensitivity and categories for the context.                                                     |

#### Example Context

```
system_u:object_r:httpd_sys_content_t:s0
```

- **system_u**: SELinux user identity.
- **object_r**: Role indicating it's an object.
- **httpd_sys_content_t**: Type for HTTP server content.
- **s0**: Sensitivity level.

**Importance of Correct Labeling:**
Incorrect contexts can cause SELinux to deny access to resources, even if UNIX permissions allow it. Proper labeling ensures that policies are enforced as intended.

### Managing SELinux Modes

#### Checking the Current Mode

Use `getenforce` to check the current SELinux mode:

```bash
getenforce
```

**Possible Outputs:**

- `Enforcing`
- `Permissive`
- `Disabled`

**Example:**

```bash
$ getenforce
Enforcing
```

#### Temporarily Changing the Mode

To temporarily switch between enforcing and permissive modes:

```bash
sudo setenforce [Enforcing|Permissive|1|0]
```

- **Enforcing or 1**: Enables enforcing mode.
- **Permissive or 0**: Enables permissive mode.

**Example:**

```bash
sudo setenforce 0   # Switch to permissive mode
```

**Verification:**

```bash
getenforce
```

#### Permanently Changing the Mode

Edit the SELinux configuration file `/etc/selinux/config`:

```bash
sudo nano /etc/selinux/config
```

Change the line:

```bash
SELINUX=enforcing
```

Options:

- `enforcing`
- `permissive`
- `disabled`

**Note:** Reboot the system to apply changes.

**Example:**

```bash
SELINUX=permissive
```

### Working with SELinux Contexts

#### Viewing Contexts

List files with their SELinux contexts:

```bash
ls -Z /path/to/file
```

**Sample Output:**

```
-rw-r--r--. root root system_u:object_r:etc_t:s0 /etc/passwd
```

List processes with their contexts:

```bash
ps -eZ | grep sshd
```

**Sample Output:**

```
system_u:system_r:sshd_t:s0-s0:c0.c1023  1234 ? 00:00:00 sshd
```

#### Using `chcon`

Change the type of a file:

```bash
sudo chcon -t httpd_sys_content_t /var/www/html/index.html
```

**Explanation:**

- `-t`: Specifies the new type.
- Changes are immediate but not persistent across relabels.

#### Restoring Default Contexts

Use `restorecon` to reset contexts to their default values:

```bash
sudo restorecon -Rv /var/www/html/
```

- `-R`: Recursively apply to all files in the directory.
- `-v`: Verbose output.

#### Using `semanage fcontext` for Persistent Changes

Add a context mapping:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/mywebsite(/.*)?"
```

Apply the context:

```bash
sudo restorecon -Rv /srv/mywebsite/
```

**Explanation:**

- `semanage fcontext` adds a persistent mapping.
- `restorecon` applies the mapping to existing files.

### SELinux Booleans

Booleans allow administrators to modify SELinux policy behavior without writing new policies.

#### Listing Booleans

List all Booleans and their statuses:

```bash
sudo getsebool -a
```

**Filter Booleans:**

```bash
sudo getsebool -a | grep httpd
```

#### Temporarily Changing a Boolean

```bash
sudo setsebool httpd_enable_cgi on
```

#### Permanently Changing a Boolean

```bash
sudo setsebool -P httpd_enable_cgi on
```

- `-P` makes the change persistent across reboots.

**Common Booleans:**

- `httpd_can_network_connect`: Allows HTTPD scripts and modules to connect to the network.
- `ftp_home_dir`: Allows FTP to read and write files in user home directories.

### SELinux Troubleshooting

#### Audit Log

- **Location**: `/var/log/audit/audit.log`
- **Contains**: Detailed records of all SELinux denials and other security events.

#### Access Vector Cache (AVC) Messages

- **Contain**: Denied access attempts.
- **Example Entry:**

```
type=AVC msg=audit(1609459200.123:456): avc:  denied  { read } for  pid=1234 comm="nginx" name="index.html" dev="sda1" ino=56789 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
```

#### `ausearch`

Search for AVC denials:

```bash
sudo ausearch -m avc -ts today
```

- `-m avc`: Search for AVC messages.
- `-ts today`: Start time of today.

#### `sealert`

Analyzes SELinux denials and provides recommendations:

```bash
sudo sealert -a /var/log/audit/audit.log
```

Requires the `setroubleshoot` package.

#### Common Troubleshooting Steps

I. Identify Denials

Use `ausearch` or check `/var/log/audit/audit.log` for recent denials.

II. Understand Denials

Use `sealert` or `audit2why` to get explanations.

```bash
sudo cat /var/log/audit/audit.log | audit2why
```

III. Adjust Contexts

Ensure files and directories have correct contexts.

```bash
sudo restorecon -Rv /path/to/directory
```

IV. Modify Booleans

Enable relevant Booleans if necessary.

```bash
sudo setsebool -P httpd_can_network_connect on
```

V. Create Custom Policies

As a last resort, use `audit2allow` to generate custom policies.

```bash
sudo grep nginx /var/log/audit/audit.log | audit2allow -M nginx_custom
sudo semodule -i nginx_custom.pp
```

**Caution:** Review custom policies carefully to avoid security risks.

### Practical Example: Allowing Nginx to Serve Content from a Custom Directory

You have Nginx installed and want it to serve content from `/srv/mywebsite/`. However, accessing the site results in a 403 Forbidden error, and SELinux is suspected to be the cause.

#### 1. Verify SELinux Denials

Check for AVC denials related to Nginx:

```bash
sudo ausearch -m avc -c nginx
```

**Sample Output:**

```
type=AVC msg=audit(1609459200.123:456): avc:  denied  { open } for  pid=1234 comm="nginx" path="/srv/mywebsite/index.html" dev="sda1" ino=56789 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
```

#### 2. Assign the Correct Context

Define the context mapping:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/mywebsite(/.*)?"
```

Apply the context:

```bash
sudo restorecon -Rv /srv/mywebsite/
```

#### 3. Verify the Context

```bash
ls -Z /srv/mywebsite/
```

**Sample Output:**

```
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 index.html
```

#### 4. Check for Remaining Denials

```bash
sudo ausearch -m avc -c nginx
```

- If no denials are found, the issue is resolved.

#### 5. Adjust Booleans if Necessary

If Nginx requires additional permissions (e.g., connecting to the network):

```bash
sudo setsebool -P httpd_can_network_connect on
```

### Challenges

1. Research and write a brief comparison between Discretionary Access Control (DAC) and Mandatory Access Control (MAC). Include how each is implemented in Linux and their roles in system security. Prepare a document detailing your findings and insights.
2. Create a short guide that explains the three modes of SELinux: Enforcing, Permissive, and Disabled. In your guide, include scenarios or use cases for each mode, explaining why and when each mode is best utilized.
3. Find or create a file and directory on a Linux system with SELinux enabled. Change their SELinux contexts using the `chcon` or `semanage fcontext` commands. Document the process and explain why changing contexts might be necessary in real-world scenarios.
4. Simulate or identify a common SELinux issue on a Linux system (such as a denied service start-up). Utilize SELinux logs (like `/var/log/audit/audit.log`) and tools (like `sealert`) to diagnose and suggest a solution. Write a troubleshooting report detailing your steps and findings.
5. Devise a hypothetical scenario where a Linux system is at risk (e.g., a web server exposed to the internet). Propose an SELinux policy implementation that would mitigate the risks. Outline your policy decisions, including the types and rules you would enforce, and explain how these choices contribute to system security.
6. On a test Linux system, switch between different SELinux modes (Enforcing, Permissive, Disabled) and observe the system behavior and logs. Document how the system's security posture changes with each mode and the implications of these changes.
7. Write a basic custom SELinux policy module for a specific application or service. Compile and apply this policy to your Linux system, and then test its effectiveness and impact on the application's functionality.
8. Analyze a set of audit logs from an SELinux-enabled system. Identify any policy violations or anomalies and propose adjustments to SELinux policies or system configuration to address these issues.
