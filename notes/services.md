## Services

A service is a program that runs in the background and responds to requests from other programs. Services use inter-process communication mechanisms, such as sockets, to communicate with other programs. Services are typically used when you want a program to:

* Run in the background.
* Start automatically when the computer boots up.
* Be globally available within the system.

You can control services by telling them to start or stop executing (single time), or by enabling or disabling them (causing them to start and stop automatically on system startup). Examples of common services include the `sshd` service, which starts an SSH server when the system boots, and the `httpd` service, which acts as a server in a client-server architecture using the HTTP and/or HTTPS network protocols.

In modern Unix-like systems, the most common tool for managing services is SystemD. SystemD is a system and service manager that is used to execute various scripts at boot time. These scripts, known as units, include services, mounts, and sockets. To list all of the units managed by SystemD, you can use the command `systemctl -t help`. The systemctl utility is a command-line tool used to communicate with SystemD, and it is often used to start, stop, and manage services.

## Daemons

A daemon is a program that runs in the background and is usually used to perform a specific task or provide a service. Daemons are usually started by the system, but it is also possible to start them manually. Unlike programs run by a user, a daemon is not under the direct control of a user.

Daemons are configured using rc and init scripts, which are typically located in `/etc/rc.d` and `/etc/init.d`. On systems using `init.d` scripts, you can list all of the installed services by using the command `ls /etc/init.d`. There are several tools that can be used to edit rc and init scripts, including systemctl for SystemD, service, and chkconfig for SysV.

It is important to note that SystemD is the most common tool for managing services and daemons in modern Unix-like systems, but some older systems may still use rc and init scripts. It is also possible for a program to act as both a service and a daemon, depending on how it is configured and how it is used.

## Daemons vs services

A daemon is a program that runs in the background and is usually used to perform a specific task or provide a service. Daemons are typically started by the system, but they can also be started manually. They are not under the direct control of a user and are configured using rc and init scripts.

A service is a program that runs in the background and responds to requests from other programs. Services are typically used when you want a program to run in the background, start automatically when the computer boots up, or be globally available within the system. Services can be controlled by telling them to start or stop executing (single time), or by enabling or disabling them (causing them to start and stop automatically on system startup).

In summary, the main difference between a daemon and a service is the way they are used and the tasks they are designed to perform. Daemons are typically used to perform specific tasks or provide services, while services are used to respond to requests from other programs.

## Managing Services

Services are programs that run in the background and provide specific functionality or services to other programs. Services can be controlled by starting, stopping, enabling, or disabling them. The tools and commands used to manage services depend on the type of service and the operating system being used.

### Checking the Status of a Service

To check the status of a service, you can use the status command. The syntax for this command varies depending on the tool being used. Here are some examples:

Using chkconfig:

```
chkconfig httpd status
```

Using systemd:

```
systemctl status httpd.service
```

### Enabling and Disabling Services

To enable a service, you can use the enable command. This will cause the service to start automatically when the system boots up. The syntax for this command varies depending on the tool being used. Here are some examples:

Using chkconfig:

```
chkconfig httpd on
```

Using systemd:

```
systemctl enable httpd.service
```

To disable a service, you can use the disable command. This will prevent the service from starting automatically when the system boots up. The syntax for this command varies depending on the tool being used. Here are some examples:

Using chkconfig

```
chkconfig httpd off
```

Using systemd
```
systemctl disable httpd.service
```

### Starting and Stopping Services

To start a service, you can use the start command. This will cause the service to start running immediately. The syntax for this command varies depending on the tool being used. Here are some examples:

Using chkconfig

```bash
service httpd start
```

Using systemd

```bash
systemctl start httpd.service
```

To stop a service, you can use the stop command. This will cause the service to stop running. The syntax for this command varies depending on the tool being used. Here are some examples:

Using chkconfig

```bash
service httpd stop
```
 
Using systemd

```bash
systemctl stop httpd.service
```

### Checking the Status of a Service

The status of a service indicates its current state and whether it is active or inactive. Some common service statuses include:

| Status | Description |
| --- | --- |
| `Loaded` | The unit file was processed, and the unit is now active. |
| `Active(running)` | The unit is active with one or more processes. |
| `Active(exited)` | A one-time task was successfully performed. |
| `Active(waiting)` | The unit is active and waiting for an event. |
| `Inactive` | The unit is not running.  |
| `Enabled` | The unit will be started at boot time. |
| `Disabled` |The unit will not be started at boot time. |
| `Static` | The unit can't be enabled, but can be started by another unit manually. |

To check the status of a service, you can use the status command. The syntax for this command varies depending on the tool being used. Here are some examples:

Using chkconfig:

```bash
chkconfig httpd status
```

Using systemd:

```bash
systemctl status httpd.service
```

### Checking service dependencies

To check if a service is dependent on a specific target, you can use the list-dependencies command along with `grep`. For example, to check if the `httpd` service is dependent on the `multi-user.target`, use:

```bash
systemctl list-dependencies multi-user.target | grep httpd
```

If the httpd service is dependent on the `multi-user.target`, it will be listed in the output. If the service is not dependent on the target, the command will not return any output.

It is important to note that the syntax of the list-dependencies command and the target you specify may vary depending on the operating system and the version of systemctl being used.

## Creating a Custom Service with SystemD

To create a custom service with SystemD, you will need to create a service script and place it in the /etc/systemd/system/ directory. The service script is a configuration file that tells SystemD how to manage the service. It consists of several sections, each of which has a specific purpose.
Common Sections in a Service Script

There are three common sections that you will find in most service scripts:

* `[Unit]`: This section describes the unit and defines dependencies. It may include options such as Description, Documentation, and After.
* `[Service]`: This section describes how to start and stop the service and request status installation. It may include options such as Type, ExecStart, ExecStop, ExecReload, and Restart.
* `[Install]`: This section informs SystemD when the service should be launched during the boot process. It may include options such as WantedBy and RequiredBy.

Here is an example of a simple service script that runs a sample script at startup:

```
[Unit]
Description=Sample Script

[Service]
Type=idle
ExecStart=/valid/path/to/an/executable/file

[Install]
WantedBy=multi-user.target
```

In this example, the `[Unit]` section includes a Description option that provides a brief description of the service. The `[Service]` section includes a Type option that specifies the type of service (in this case, idle) and an ExecStart option that specifies the path to the executable file that will be run when the service starts. The `[Install]` section includes a WantedBy option that specifies the target (`multi-user.target`) that the service should be started with.

You can read more about targets <a href="https://github.com/djeada/Linux-Notes/blob/main/notes/system_startup.md">here</a>.

## Challenges

1. List all the SystemD timers on your system and determine which services are enabled.
1. Set up a DHCP (Dynamic Host Configuration Protocol) server using the `isc-dhcp-server` package. This service allows clients to automatically obtain network configuration information, such as IP addresses, from a DHCP server.
1. Set up an NFS (Network File System) server using the `nfs-kernel-server` package. This service allows clients to access files over a network as if they were stored locally.
1. Set up an SSH (Secure Shell) server using the `openssh-server` package. This service allows you to remotely connect to a server over an encrypted connection.
1. Set up a DNS (Domain Name System) server using the `bind9` package. This service translates human-readable domain names into numerical IP addresses.
1. Set up a mail server using either the `postfix` or `sendmail` package. This service handles the delivery of email messages.
1. Set up a web server using one of the following packages: `nginx`, `apache`, `caddy`, or `traefik`. This service serves content over the HTTP or HTTPS protocol.
1. Set up a database server using either the `mysql` or `postgres` package. This service allows you to store and manage data in a structured way.
