## SELinux

SELinux (Security Enhanced Linux) is a security module for the Linux kernel that provides a way to enforce mandatory access control policies on Linux systems. It was developed by the United States National Security Agency (NSA) as part of their efforts to secure the Linux operating system.

## Enabling SELinux

By default, SELinux is disabled on most Linux distributions. To enable it, you will need to edit the /etc/selinux/config file and set the SELINUX option to enforcing.

## SELinux Modes

There are three SELinux modes:

* Enforcing: SELinux policies are enforced. Any actions that violate the policies will be blocked.
* Permissive: SELinux policies are not enforced, but any actions that violate the policies will be logged.
* Disabled: SELinux is completely disabled and no policies are enforced.

You can check the current SELinux mode by running the sestatus command.

## SELinux Contexts

SELinux uses contexts to label files, processes, and other objects in the system. These contexts are used to determine whether a certain action is allowed or not.

There are four types of SELinux contexts:

* User: Identifies the user who owns the object.
* Role: Identifies the role of the object.
* Type: Identifies the type of the object (e.g. file, process, etc.).
* Domain: Identifies the domain in which the object is running.

You can view the SELinux context of an object by using the ls -Z command.

## SELinux Policies

SELinux policies are rules that define what processes can access certain resources. There are three types of policies:

* Targeted policy: Only targeted processes and resources are protected by SELinux.
* Strict policy: All processes and resources are protected by SELinux.
* MLS policy: Multi-Level Security policy, used in high security environments.

To view the current SELinux policy, use:

```
semodule -l
```
