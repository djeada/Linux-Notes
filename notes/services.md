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

### Daemons

Daemons are specialized background processes designed to perform tasks or provide services autonomously. They are typically launched during the system's startup process but can also be initiated manually. Unlike interactive user programs, daemons operate independently of user control.

Daemons are traditionally managed using `rc` (run commands) and `init` (initialization) scripts, commonly located in `/etc/rc.d` and `/etc/init.d` directories. On systems utilizing `init.d` scripts, you can list all services using `ls /etc/init.d`. Tools like `systemctl` (for SystemD-based systems), `service`, and `chkconfig` (for SysV-init systems) are used to manage these scripts.

While `SystemD` has become the standard for service and daemon management in modern Unix-like systems, some older systems still rely on `rc` and `init` scripts. A program can function as both a service and a daemon, depending on its configuration and role.

### Daemons vs services

The distinction between daemons and services primarily lies in their roles and operational contexts. Daemons are designed for specific tasks or to provide particular services autonomously. They are generally system-started and can also be manually initiated, operating independently of direct user control, managed via `rc` and `init` scripts.

In contrast, services are background processes that interface with other programs, often necessitating system-wide availability, starting with the system boot, and running continuously in the background. They are managed by starting, stopping, enabling, or disabling them as needed.

| **Aspect**        | **Daemon**                                              | **Service**                                            |
|-------------------|---------------------------------------------------------|--------------------------------------------------------|
| **Definition**    | A background process running continuously, often from boot time. | A software function provided to users or other programs. |
| **Purpose**       | To handle tasks regularly, automatically, or on demand without user interaction. | To perform a specific function for the system or other applications. |
| **Run Model**     | Always running in the background (continuous).           | Can be continuous (always running) or on-demand.       |
| **Examples**      | `httpd` (Apache web server), `sshd` (SSH server), `crond` (cron scheduler) | Web server, database server, file-sharing service, etc. |
| **How It's Managed** | By the system (often via tools like `systemd`, `init.d`, etc.). | By system administrators or service management tools.  |
| **Startup**       | Generally starts at boot time and runs until shutdown.   | May start at boot, run on demand, or be manually started/stopped. |
| **Scope**         | Background operation; typically not interacted with directly by users. | May be accessible to users or other programs as a function or API. |
| **Naming**        | Often ends with "d" (e.g., `httpd`, `sshd`).             | Name is usually descriptive of the function (e.g., web server). |
| **Relationship**  | Provides specific services by running in the background. | Can be implemented as a daemon but not always required to be one. |

- A **daemon** describes *how* a task runs (continuously and in the background).
- A **service** describes *what* a task provides (a specific function).
  
Daemons are often services, but not all services need to be daemons.

### Managing Services

Services, being integral background processes, offer functionalities or services to other programs or the system. Their management involves starting, stopping, enabling, or disabling them, with the specific commands and tools varying based on the service type and the operating system.

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

#### Checking the Status of a Service

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

#### Checking Service Dependencies

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

### Example: Operating FTP Server

### 1. **Installing FTP Server using Package Managers (RPM and YUM)**

#### **1.1. Using YUM Package Manager**

**Step 1: Search for FTP packages**

```bash
yum list | grep ftp
```

**Expected Output**:
```bash
vsftpd.x86_64      3.0.2-29.el7   @base
lftp.x86_64        4.4.8-9.el7    @base
```

- `vsftpd` is the FTP server package we are interested in.
- `lftp` is a command-line FTP client package.
- The `@base` indicates that these packages are from the base repository.

**Step 2: Install vsftpd (FTP server)**

```bash
yum install vsftpd
```

**Expected Output**:

```bash
Dependencies Resolved
================================================================================
 Package             Arch               Version                  Repository
================================================================================
Installing:
 vsftpd              x86_64             3.0.2-29.el7             base
...
Is this ok [y/d/N]: y
```

It resolves dependencies and asks for confirmation to proceed with the installation. Press `y` to install.

#### **1.2. Using RPM Package Manager**

**Step 1: Search for FTP package using RPM**

```bash
rpm -qa | grep ftp
```

**Expected Output**:

```bash
vsftpd-3.0.2-29.el7.x86_64
lftp-4.4.8-9.el7.x86_64
```

- This lists already installed FTP-related packages.
- `vsftpd` is the FTP server; if it's listed, you don’t need to install it again.

**Step 2: Install vsftpd using RPM**

```bash
rpm -ivh vsftpd-3.0.2-29.el7.x86_64.rpm
```

**Expected Output**:

```bash
Preparing...                     ################################# [100%]
Updating / installing...
   1:vsftpd-3.0.2-29.el7         ################################# [100%]
```

The package installs successfully if no errors appear.

### 2. **Configuring and Starting the FTP Server**

**Step 1: Edit the configuration file**

```bash
vi /etc/vsftpd/vsftpd.conf
```

Look for these key options:

- `anonymous_enable=YES` or `NO` (depends on if you want anonymous access).
- `local_enable=YES` (to allow local users).
- `write_enable=YES` (if you want to allow file uploads).

**Step 2: Enable and start vsftpd service**
```bash
systemctl enable vsftpd
systemctl start vsftpd
```

**Expected Output (Enable command)**:

```bash
Created symlink from /etc/systemd/system/multi-user.target.wants/vsftpd.service to /usr/lib/systemd/system/vsftpd.service.
```

The `systemctl enable` command sets the service to start on boot. The symlink confirmation indicates success.

**Expected Output (Start command)**:
```bash
No output (command completes silently)
```

No output means the service started successfully. Use `systemctl status` to verify.

**Step 3: Check service status**
```bash
systemctl status vsftpd
```

**Expected Output**:

```bash
● vsftpd.service - Vsftpd ftp daemon
   Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-10-05 12:30:50 UTC; 5min ago
```

**Interpretation**: 
- `Active: active (running)` indicates that the FTP service is running.

### 3. **Checking on Which Port FTP Operates**

**Step 1: Check the port being used**
```bash
netstat -tulnp | grep ftp
```

**Expected Output**:
```bash
tcp   0  0 0.0.0.0:21     0.0.0.0:*       LISTEN      1234/vsftpd
tcp6  0  0 :::21          :::*            LISTEN      1234/vsftpd
```

- This shows that the FTP server is listening on port `21` (the standard FTP port).
- `1234` is the process ID (PID) of the vsftpd service.
- `LISTEN` means it’s actively waiting for incoming connections.

### 4. **Checking if the Port is Free**

**Step 1: Check if port 21 is in use**
```bash
netstat -an | grep 21
```

**Expected Output**:
```bash
tcp   0  0 0.0.0.0:21     0.0.0.0:*       LISTEN
```

If you see `LISTEN` on port `21`, it means the port is in use by FTP. If there's no output, the port is free.

**Alternative:**

```bash
ss -an | grep 21
```

**Expected Output**:

```bash
LISTEN     0      100    0.0.0.0:21      0.0.0.0:*
```

### 5. **Testing the FTP Server**

**Step 1: Verify that the FTP service is running**
```bash
ps -ef | grep vsftpd
```

**Expected Output**:
```bash
root     1234     1  0 12:30 ?        00:00:00 /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf
```

This output shows that vsftpd is running with PID `1234`.

**Step 2: Test FTP connection on localhost**
```bash
ftp localhost
```

**Expected Output**:
```bash
Connected to localhost (127.0.0.1).
220 (vsFTPd 3.0.2)
Name (localhost:user):
```

- The `220 (vsFTPd 3.0.2)` message indicates the FTP server is ready.
- You can enter a username to continue, or test anonymous access with `anonymous`.

**Step 3: Test FTP connection from another machine**
```bash
ftp <server_ip>
```

**Expected Output**:
```bash
Connected to <server_ip>.
220 (vsFTPd 3.0.2)
Name (<server_ip>:user):
```

**Interpretation**: 
- This output shows that the FTP server is accessible from the network.

**Step 4: Upload and download test files**
1. **Upload file**:
```bash
put testfile.txt
```
**Expected Output**:
```bash
200 PORT command successful.
150 Ok to send data.
226 Transfer complete.
```

**Interpretation**: The file `testfile.txt` was successfully uploaded.

2. **Download file**:
```bash
get testfile.txt
```
**Expected Output**:
```bash
200 PORT command successful.
150 Opening BINARY mode data connection.
226 Transfer complete.
```

**Interpretation**: The file was successfully downloaded.

**Step 5: Exit the FTP session**
```bash
bye
```

**Expected Output**:

```bash
221 Goodbye.
```

### 6. **Check FTP Server Logs**

```bash
tail -f /var/log/vsftpd.log
```

**Expected Output**:

```
Mon Oct  5 12:35:15 2024 [pid 1235] CONNECT: Client "::1"
Mon Oct  5 12:35:16 2024 [pid 1235] [anonymous] OK LOGIN: Client "::1"
Mon Oct  5 12:36:20 2024 [pid 1236] [user] UPLOAD: Client "::1", "/home/user/testfile.txt"
```

This shows connection and file transfer logs, which can be helpful for debugging.

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

#### Additional Notes

After creating or modifying a service script, use `systemctl daemon-reload` to reload the SystemD configuration and `systemctl enable [service-name].service` to enable the service.

In the context of SystemD service management, `[service-name]` refers to the name of your service unit file, minus the `.service` extension. It's a unique identifier for your service within the SystemD framework. When you create a custom service script:

1. The file is named with a `.service` extension, for example, `my_custom_service.service`.
2. The `[service-name]` is the filename without the `.service` extension, i.e., `my_custom_service` in this example.

So, when enabling, starting, or checking the status of your service with SystemD commands, you reference it by this `[service-name]`. For example:

- To enable the service: `systemctl enable my_custom_service.service`
- To start the service: `systemctl start my_custom_service.service`
- To check the service status: `systemctl status my_custom_service.service`

### Challenges

1. Use SystemD to list all timers and determine which corresponding services are enabled on your system.
2. Install and configure a DHCP server using the `isc-dhcp-server` package. This service should be set up to automatically provide network configuration to client devices.
3. Use the `nfs-kernel-server` package to set up an NFS server. Ensure it allows clients to access files over the network seamlessly.
4. Install the `openssh-server` package and configure an SSH server for secure, remote connections to your server.
5. Utilize the `bind9` package to set up a DNS server. This server should effectively translate human-readable domain names into IP addresses.
6. Choose between the `postfix` or `sendmail` packages to set up a mail server, capable of handling email delivery and management.
7. Select and configure one of these packages - `nginx`, `apache`, `caddy`, or `traefik`, to establish a web server. This server should be able to serve content over HTTP or HTTPS.
8. Install and configure a database server using either `mysql` or `postgres`. This server should provide robust data storage and management capabilities.
