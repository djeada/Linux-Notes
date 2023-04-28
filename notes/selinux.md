## SELinux Notes

SELinux, or Security-Enhanced Linux, is a mandatory access control (MAC) security mechanism implemented in the Linux kernel. It enforces security policies on a system to limit the access and capabilities of users and applications, preventing unauthorized access to system resources.

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

1. Explain the difference between discretionary access control (DAC) and mandatory access control (MAC).
2. What are the three modes of SELinux, and when would you use each?
3. How do you change the SELinux context of a file or directory?
4. What tools and logs can help you troubleshoot SELinux issues?
5. Describe a scenario where SELinux could help the security?
