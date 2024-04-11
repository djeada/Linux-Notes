## Services

A service in computing is a background process that performs specific tasks or offers various functionalities to other programs. These services typically communicate using methods such as sockets or inter-process communication (IPC). The primary purposes of a service include:

- Running in the background without user intervention.
- Automatically starting during the system's boot process.
- Being accessible system-wide, providing functionalities to various components.

Services can be managed through various actions like starting or stopping them on demand, or enabling or disabling them to automatically start or stop during system boot. Common examples of services include the `sshd` service, which initiates an SSH server, and the `httpd` service, responsible for web server functionalities using HTTP and/or HTTPS protocols.

In modern Unix-like operating systems, `SystemD` is a prevalent tool for managing services. SystemD orchestrates the system's startup sequence by handling various scripts known as units. These units encompass services, mount points, sockets, and more. To view all units managed by SystemD, use the command `systemctl list-units`. The `systemctl` utility, a command-line interface, interacts with SystemD to manage these units, including starting, stopping, and configuring services.


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

Daemons are specialized background processes designed to perform tasks or provide services autonomously. They are typically launched during the system's startup process but can also be initiated manually. Unlike interactive user programs, daemons operate independently of user control.

Daemons are traditionally managed using `rc` (run commands) and `init` (initialization) scripts, commonly located in `/etc/rc.d` and `/etc/init.d` directories. On systems utilizing `init.d` scripts, you can list all services using `ls /etc/init.d`. Tools like `systemctl` (for SystemD-based systems), `service`, and `chkconfig` (for SysV-init systems) are used to manage these scripts.

While `SystemD` has become the standard for service and daemon management in modern Unix-like systems, some older systems still rely on `rc` and `init` scripts. A program can function as both a service and a daemon, depending on its configuration and role.

## Daemons vs services

The distinction between daemons and services primarily lies in their roles and operational contexts. Daemons are designed for specific tasks or to provide particular services autonomously. They are generally system-started and can also be manually initiated, operating independently of direct user control, managed via `rc` and `init` scripts.

In contrast, services are background processes that interface with other programs, often necessitating system-wide availability, starting with the system boot, and running continuously in the background. They are managed by starting, stopping, enabling, or disabling them as needed.

The fundamental difference lies in their operational scope and interaction: daemons typically perform dedicated tasks or services autonomously, while services facilitate interactions with other system components.

## Managing Services

Services, being integral background processes, offer functionalities or services to other programs or the system. Their management involves starting, stopping, enabling, or disabling them, with the specific commands and tools varying based on the service type and the operating system.

### Enabling and Disabling Services

Enabling and disabling services are crucial tasks in system administration, determining whether a service starts automatically during the system boot process.

#### Enabling Services

To enable a service means to configure it to start automatically when the system boots up. This is particularly useful for services that are essential for system operations or that provide critical functionalities. The command to enable a service varies depending on the system's initialization system. Here are common examples:

I. Using `chkconfig` for SysV-init systems:

```bash
chkconfig httpd on
```

This command sets the httpd service to start automatically.

II. Using `systemctl` for SystemD-based systems:

```bash
systemctl enable httpd.service
```

This command creates a symbolic link for the httpd.service unit file, ensuring it's activated on boot.

#### Disabling Services

Disabling a service prevents it from starting automatically during system boot, which is useful for non-essential services or for troubleshooting conflicts. The specific command also depends on the system's initialization system:

I. Using `chkconfig` for SysV-init systems:

```bash
chkconfig httpd off
```

This command removes the httpd service from the system's startup sequence.

II. Using `systemctl` for SystemD-based systems:

```bash
systemctl disable httpd.service
```

This command removes the symbolic link for the httpd.service, preventing it from starting at boot.

### Starting and Stopping Services

Apart from enabling or disabling services for automatic startup, you might need to manually start or stop a service for immediate effect, testing, or troubleshooting.

#### Starting Services

To start a service means to initiate its operation immediately. This is often done after installing a new service or making configuration changes.

I. Using `chkconfig` for SysV-init systems:

```bash
service httpd start
```

This command triggers the immediate start of the httpd service.

II. Using `systemctl` for SystemD-based systems:

```bash
systemctl start httpd.service
```

This command tells systemd to start the httpd service right away.

#### Stopping Services

Conversely, stopping a service halts its operation. This can be necessary for maintenance, updates, or to resolve performance issues.

I. Using `chkconfig` for SysV-init systems:

```bash
service httpd stop
```

This command stops the httpd service immediately, freeing up resources.

II. Using `systemctl` for SystemD-based systems:

```bash
systemctl stop httpd.service
```

This command instructs systemd to terminate the httpd service.

### Checking the Status of a Service

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

I. Using `chkconfig` for SysV-init systems:

```
chkconfig --list httpd
```

II. Using `systemctl` for SystemD-based systems:

```
systemctl status httpd.service
```

### Checking Service Dependencies

Understanding service dependencies is crucial for effective system administration, particularly when managing startup sequences and troubleshooting service issues. To check whether a particular service is dependent on a specific target or another service, the `systemctl` command can be utilized in conjunction with `grep`. Here's how to do it:
Using this command sets Adam as the owner and assigns the "admins" group to the file.txt.
```bash
systemctl list-dependencies [target/service] | grep [service-name]
```

For example to determine if the httpd service depends on `multi-user.target`:

```bash
systemctl list-dependencies multi-user.target | grep httpd
```

Interpretation of Results:

- **Output Present**: If the httpd service is listed in the output, this indicates that it indeed has a dependency on the specified `multi-user.target`.
- **No Output**: If there is no output, it implies that httpd does not depend on `multi-user.target`.

Note that the syntax of the list-dependencies command and the target you specify may vary depending on the operating system and the version of systemctl being used.

## Creating a Custom Service with SystemD

Creating a custom service in SystemD involves writing a service unit file. This file is a configuration script that provides instructions to SystemD on how to manage and execute the service. These scripts are typically placed in the `/etc/systemd/system/` directory. A service script is divided into several sections, each serving a specific purpose.

### Common Sections in a Service Script

Most service scripts include the following sections:

- `[Unit]`: This section provides a description of the service and defines its dependencies. Key directives in this section can include `Description`, which gives a brief description of the service, `Documentation`, providing links to the relevant documentation, and `After`, specifying the order of service startup relative to other units.

- `[Service]`: This section details how the service should be started, stopped, and how it should respond under various conditions. Common directives here include `Type`, defining the startup behavior of the service; `ExecStart`, specifying the command to run when the service starts; `ExecStop` and `ExecReload`, defining the commands to stop and reload the service; and `Restart`, specifying the service's restart behavior.

- `[Install]`: This section is used to define how the service integrates into the system's boot process. It typically includes directives like `WantedBy` and `RequiredBy`, which specify the targets that should include this service during their initialization.

### Example of a Simple Service Script

Below is an example of a basic service script. This script configures SystemD to run a specific executable file at startup:

```systemd
[Unit]
Description=Sample Script Service

[Service]
Type=idle
ExecStart=/valid/path/to/an/executable/file

[Install]
WantedBy=multi-user.target
```

This script includes:

- `Description`: A brief explanation of the service.
- `Type=idle`: Indicates that the service should be started after all jobs are dispatched.
- `ExecStart`: The path to the executable file that will be run when the service starts.
- `WantedBy=multi-user.target`: Specifies that the service should be started under the `multi-user.target`, which is a standard target for creating a multi-user environment.

You can read more about targets <a href="https://github.com/djeada/Linux-Notes/blob/main/notes/system_startup.md">here</a>.

### Additional Notes

After creating or modifying a service script, use `systemctl daemon-reload` to reload the SystemD configuration and `systemctl enable [service-name].service` to enable the service.

In the context of SystemD service management, `[service-name]` refers to the name of your service unit file, minus the `.service` extension. It's a unique identifier for your service within the SystemD framework. When you create a custom service script:

1. The file is named with a `.service` extension, for example, `my_custom_service.service`.
2. The `[service-name]` is the filename without the `.service` extension, i.e., `my_custom_service` in this example.

So, when enabling, starting, or checking the status of your service with SystemD commands, you reference it by this `[service-name]`. For example:

- To enable the service: `systemctl enable my_custom_service.service`
- To start the service: `systemctl start my_custom_service.service`
- To check the service status: `systemctl status my_custom_service.service`

## Challenges

1. Use SystemD to list all timers and determine which corresponding services are enabled on your system.
2. Install and configure a DHCP server using the `isc-dhcp-server` package. This service should be set up to automatically provide network configuration to client devices.
3. Use the `nfs-kernel-server` package to set up an NFS server. Ensure it allows clients to access files over the network seamlessly.
4. Install the `openssh-server` package and configure an SSH server for secure, remote connections to your server.
5. Utilize the `bind9` package to set up a DNS server. This server should effectively translate human-readable domain names into IP addresses.
6. Choose between the `postfix` or `sendmail` packages to set up a mail server, capable of handling email delivery and management.
7. Select and configure one of these packages - `nginx`, `apache`, `caddy`, or `traefik`, to establish a web server. This server should be able to serve content over HTTP or HTTPS.
8. Install and configure a database server using either `mysql` or `postgres`. This server should provide robust data storage and management capabilities.
