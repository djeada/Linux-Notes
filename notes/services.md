## Services

A service is a background program that talks to other programs. Services use communication methods, like sockets, to talk to other programs. You usually use a service to:

* Run in the background.
* Start when the computer starts.
* Be available for the whole system.

You can control services by starting or stopping them (one time) or enabling or disabling them (starting and stopping when the computer starts). Examples of common services are the `sshd` service, which starts an SSH server, and the `httpd` service, which acts as a server using the HTTP and/or HTTPS network.

In modern Unix-like systems, the most common tool for managing services is SystemD. SystemD is a manager used to run various scripts when the computer starts. These scripts, called units, include services, mounts, and sockets. To list all units managed by SystemD, use the command `systemctl -t help`. The systemctl utility is a command-line tool used to talk to SystemD and is often used to start, stop, and manage services.

```
+--------------------------------------------------+
|                Linux Operating System            |
|                                                  |
|    +------------------------+   +-------------+  |
|    |     Service Manager    |   |             |  |
|    |     (e.g., systemd)    |<--|  User       |  |
|    +------------------------+   |  Commands   |  |
|         |         ^             | (e.g.,      |  |
|         |         |             |  systemctl  |  |
|    Start|         |Stop/Restart |  start/stop |  |
|     /Enable       | /Disable    |  /status)   |  |
|         v         |             +-------------+  |
|    +------------------------+                    |
|    |      Linux Service     |                    |
|    |         (Daemon)       |                    |
|    |                        |                    |
|    | - Runs in background   |                    |
|    | - Performs tasks       |                    |
|    | - Listens to events    |                    |
|    | - Logs activity        |                    |
|    | - Responds to          |                    |
|    |   service manager      |                    |
|    +------------------------+                    |
|                                                  |
+--------------------------------------------------+
```

## Daemons

A daemon is a background program used to do a task or provide a service. Daemons are usually started by the system but can also be started manually. Unlike programs run by a user, a daemon is not directly controlled by a user.

Daemons are set up using rc and init scripts, usually found in `/etc/rc.d` and `/etc/init.d`. On systems using `init.d` scripts, you can list all services by using the command `ls /etc/init.d`. Several tools can be used to edit rc and init scripts, including systemctl for SystemD, service, and chkconfig for SysV.

SystemD is the most common tool for managing services and daemons in modern Unix-like systems, but some older systems may still use rc and init scripts. A program can also act as both a service and a daemon, depending on its configuration and use.

## Daemons vs services

A daemon is a background program used to do a task or provide a service. Daemons are usually started by the system and can also be started manually. They are not directly controlled by a user and are set up using rc and init scripts.

A service is a background program that talks to other programs. Services are usually used when you want a program to run in the background, start when the computer starts, or be available for the whole system. Services can be controlled by starting or stopping them (one time), or enabling or disabling them (starting and stopping when the computer starts).

The main difference between a daemon and a service is how they are used and the tasks they do. Daemons usually do specific tasks or provide services, while services talk to other programs.

## Managing Services

Services are background programs that provide specific functions or services to other programs. Services can be controlled by starting, stopping, enabling, or disabling them. The tools and commands used to manage services depend on the type of service and the operating system being used.

### Checking the Status of a Service

To check the status of a service, you can use the status command. The way this command is used depends on the tool being used. Here are some examples:

Using chkconfig:

```
chkconfig httpd status
```

Using systemd:

```
systemctl status httpd.service
```

### Enabling and Disabling Services

To enable a service, you can use the enable command. This will make the service start when the system starts. The way this command is used depends on the tool being used. Here are some examples:

Using chkconfig:

```
chkconfig httpd on
```

Using systemd:

```
systemctl enable httpd.service
```

To disable a service, you can use the disable command. This will stop the service from starting when the system starts. The way this command is used depends on the tool being used. Here are some examples:

Using chkconfig: 

```
chkconfig httpd off
```

Using systemd: 

```
systemctl disable httpd.service
```

### Starting and Stopping Services

To start a service, you can use the start command. This will make the service run right away. The way this command is used depends on the tool being used. Here are some examples:

Using chkconfig:

```bash
service httpd start
```

Using systemd:

```bash
systemctl start httpd.service
```

To stop a service, you can use the stop command. This will make the service stop running. The way this command is used depends on the tool being used. Here are some examples:

Using chkconfig:

```bash
service httpd stop
```
 
Using systemd:

```bash
systemctl stop httpd.service
```

## Checking the Status of a Service

The status of a service shows its current state and if it is active or not. Some common service statuses include:

| Status | Description |
| --- | --- |
| `Loaded` | The unit file was processed, and the unit is now active. |
| `Active(running)` | The unit is active with one or more processes.|
| `Active(exited)` | A one-time task was successfully performed. |
| `Active(waiting)` | The unit is active and waiting for an event. |
| `Inactive` | The unit is not running.  |
| `Enabled` | The unit will be started at boot time. |
| `Disabled` |The unit will not be started at boot time. |
| `Static` | The unit can't be enabled, but can be started by another unit manually. |

To check the status of a service, you can use the status command. The way this command is used depends on the tool being used. Here are some examples:

Using chkconfig:

```bash
chkconfig httpd status
```

Using systemd:

```bash
systemctl status httpd.service
```

### Checking service dependencies

To check if a service depends on a specific target, you can use the `list-dependencies` command with `grep`. For example, to check if the httpd service depends on the `multi-user.target`, use:

```bash
systemctl list-dependencies multi-user.target | grep httpd
```

If the httpd service depends on the `multi-user.target`, it will be listed in the output. If the service does not depend on the target, the command will not show any output.

Note that the syntax of the list-dependencies command and the target you specify may vary depending on the operating system and the version of systemctl being used.

## Creating a Custom Service with SystemD

To create a custom service with SystemD, you need to create a service script and put it in the /etc/systemd/system/ directory. The service script is a configuration file that tells SystemD how to manage the service. It has several sections, each with a specific purpose.

Common Sections in a Service Script

There are three common sections in most service scripts:

* `[Unit]`: This section describes the unit and defines dependencies. It may include options such as Description, Documentation, and After.
* `[Service]`: This section describes how to start and stop the service and request status installation. It may include options such as Type, ExecStart, ExecStop, ExecReload, and Restart.
* `[Install]`: This section tells SystemD when the service should start during the boot process. It may include options such as WantedBy and RequiredBy.


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
2. Set up a DHCP (Dynamic Host Configuration Protocol) server using the `isc-dhcp-server` package. This service allows clients to automatically obtain network configuration information, such as IP addresses, from a DHCP server.
3. Set up an NFS (Network File System) server using the `nfs-kernel-server` package. This service allows clients to access files over a network as if they were stored locally.
4. Set up an SSH (Secure Shell) server using the `openssh-server` package. This service allows you to remotely connect to a server over an encrypted connection.
5. Set up a DNS (Domain Name System) server using the `bind9` package. This service translates human-readable domain names into numerical IP addresses.
6. Set up a mail server using either the `postfix` or `sendmail` package. This service handles the delivery of email messages.
7. Set up a web server using one of the following packages: `nginx`, `apache`, `caddy`, or `traefik`. This service serves content over the HTTP or HTTPS protocol.
8. Set up a database server using either the `mysql` or `postgres` package. This service allows you to store and manage data in a structured way.
