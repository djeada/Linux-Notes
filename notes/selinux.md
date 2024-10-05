## SELinux Notes

SELinux, or Security-Enhanced Linux, is a mandatory access control (MAC) security mechanism implemented in the Linux kernel. It enforces security policies on a system to limit the access and capabilities of users and applications, preventing unauthorized access to system resources.

```
+-------------------------+
|        User Process     |
|   (e.g., SSH Daemon)    |
+-----------+-------------+
            |
            | Access Request (e.g., Read File)
            v
+-------------------------+
|     SELinux Policy      |
|  (Rules and Definitions)|
+-----------+-------------+
            |
            | Decision (Allow/Deny)
            v
+-------------------------+
|    Linux Kernel (MAC)   |
|   Enforces Decision     |
+-------------------------+
```

Explanation:

1. **User Process**: Attempts an action (e.g., reading a file).
2. **SELinux Policy**: The kernel consults the policy to determine if the action is permitted based on the security contexts of the process and the file.
3. **Enforcement**: The kernel allows or denies the action accordingly.

## SELinux Modes

SELinux can operate in three modes:

1. **Enforcing**: All policies are enforced, and any attempted policy violations are blocked and logged.
2. **Permissive**: Policy violations are allowed but logged, which can help administrators to identify potential issues before switching to enforcing mode.
3. **Disabled**: SELinux is entirely disabled, and no policies are enforced or logged.

## SELinux Policy Types

There are two main types of SELinux policies:

1. **Targeted**: This policy type provides protection for specific, targeted system daemons, while the rest of the system runs in unconfined mode. It is the default policy for many Linux distributions and provides a balance between security and ease of use.
2. **Strict**: This policy type enforces SELinux policies on all system processes and provides maximum security. However, it can be more challenging to configure and maintain.

## SELinux Contexts

SELinux uses contexts to define the security attributes of files, processes, and other objects. A context is a string composed of four fields: user, role, type (or domain), and level. For example:

```
user_u:role_r:type_t:s0
```

In SELinux, processes run in domains, and files have types. The policy rules define which domains are allowed to access which types.

## Managing SELinux

To determine the current SELinux mode, run:

```
getenforce
```

To temporarily change the SELinux mode, use the `setenforce` command followed by either 'Enforcing', 'Permissive', or '0' (Permissive) or '1' (Enforcing):

```
sudo setenforce 0
```

To permanently change the SELinux mode, edit the `/etc/selinux/config` file and update the `SELINUX=` line accordingly:

```
SELINUX=enforcing
```

Restart the system to apply the changes.

## Working with SELinux Contexts

To display the SELinux context of a file or directory, use the `-Z` option with the `ls` command:

```
ls -Z /path/to/file
```

To change the context of a file or directory, use the `chcon` command:

```
sudo chcon -t httpd_sys_content_t /path/to/web/content
```

This example sets the type to `httpd_sys_content_t`, which allows the Apache web server to access the specified content.

## SELinux Troubleshooting

When troubleshooting SELinux issues, the following tools and logs can be helpful:

1. **ausearch**: Searches the audit log for specific SELinux events.
2. **sealert**: Analyzes SELinux denials and provides suggestions for resolving issues.
3. **/var/log/audit/audit.log**: Contains detailed SELinux logs, including denied actions and AVC messages.

## Challenges

1. Research and write a brief comparison between Discretionary Access Control (DAC) and Mandatory Access Control (MAC). Include how each is implemented in Linux and their roles in system security. Prepare a document detailing your findings and insights.
2. Create a short guide that explains the three modes of SELinux: Enforcing, Permissive, and Disabled. In your guide, include scenarios or use cases for each mode, explaining why and when each mode is best utilized.
3. Find or create a file and directory on a Linux system with SELinux enabled. Change their SELinux contexts using the `chcon` or `semanage fcontext` commands. Document the process and explain why changing contexts might be necessary in real-world scenarios.
4. Simulate or identify a common SELinux issue on a Linux system (such as a denied service start-up). Utilize SELinux logs (like `/var/log/audit/audit.log`) and tools (like `sealert`) to diagnose and suggest a solution. Write a troubleshooting report detailing your steps and findings.
5. Devise a hypothetical scenario where a Linux system is at risk (e.g., a web server exposed to the internet). Propose an SELinux policy implementation that would mitigate the risks. Outline your policy decisions, including the types and rules you would enforce, and explain how these choices contribute to system security.
6. On a test Linux system, switch between different SELinux modes (Enforcing, Permissive, Disabled) and observe the system behavior and logs. Document how the system's security posture changes with each mode and the implications of these changes.
7. Write a basic custom SELinux policy module for a specific application or service. Compile and apply this policy to your Linux system, and then test its effectiveness and impact on the application's functionality.
8. Analyze a set of audit logs from an SELinux-enabled system. Identify any policy violations or anomalies and propose adjustments to SELinux policies or system configuration to address these issues.
