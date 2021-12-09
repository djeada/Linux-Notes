<h1>What are services?</h1>
You can use services, when you want to run a program:

- In the background.
- Start automatically when the computer boots up.
- Run various applications in a specific order after the boot up.
- Make it globally available within the system.

<code>Systemd</code> executes different scripts at boot time, those scripts are known as <code>units</code>. Units include services, mounts and sockets. To display all of them, use:

```bash
systemctl -t help
```

Thus, services are often used to run programs at boot time, but you can start and stop services at any time. 

1. An example of a systemd service is the <code>sshd</code> service. It starts the SSH server when the system boots. 
2. Anoter example is the <code>httpd</code> service. It acts as a server in a client-server architecture, employing the HTTP and/or HTTPS network protocols. 

A service usually responds to requests from other programs. It uses inter-process communication mechanisms, like sockets, to communicate with other programs. Web servers may provide serivces, like HTTP, HTTPS, FTP, and SSH.

<h1>What is a daemon?</h1>
A daemon is a program that runs in the background. It is usually used to perform a task, like monitoring a system, or to provide a service. Daemons are usually started by the system, but it is also possible to start them manually. In constrasts to programs run by the user, a daemon is not under the direct control of a user. Daemons are configured with <code>rc</code> and <code>init</code> scripts, that are typically located in /etc/rc.d and /etc/init.d.

<h1>Create a custom service</h1>

Systemd services should be placed at /etc/systemd/system/.

Common sections include:

* <code>[Unit]</code> describes the unit and defines dependencies.
* <code>[Service]</code> describes how to start and stop the service and request status installation.
* <code>[Install]</code> informs systemd when the service should be launched during the boot process. 

An example of a foo.service script:

```bash
[Unit]
Description=Sample Script

[Service]
Type=idle
ExecStart=/valid/path/to/an/executable/file

[Install]
WantedBy=multi-user.target
```

<h1>Target types</h1>

| Target type | Runlevel |
| --- | --- |
| <code>poweroff.target</code> | runlevel 0 |
| <code>rescue.target</code> | runlevel 1 |
| <code>emergency.target</code> | runlevel 2 |
| <code>multi-user.target</code> | runlevel 3 |
| <code>graphical.target</b></code> | runlevel 5 |
| <code>reboot.target</code> | runlevel 6 |

<h1>Service statuses</h1>

| Status | Description |
| --- | --- |
| <code>Loaded</code> | The unit file was processed, and the unit is now active. |
| <code>Active(running)</code> | The unit is active with one or more processes. |
| <code>Active(exited)</code> | A one-time task was successfully performed. |
| <code>Active(waiting)</code> | The unit is active and waiting for an event. |
| <code>Inactive</b></code> | The unit is not running.  |
| <code>Enabled</code> | The unit will be started at boot time. |
| <code>Disabled</code> |The unit will not be started at boot time. |
| <code>Static</code> | The unit can't be enabled, but can be started by another unit manually. |

<h1>The systemctl command</h1>

Some services are always running, whereas others run once and then stop. To display the status of a service, use:

```bash
systemctl status httpd
```

To start a service, use:

```bash
systemctl start httpd
```

To check if service is enabled, use:

```bash
systemctl is-enable httpd
```

To enable a service, use:

```bash
systemctl enable httpd
```

To check if service is dependent on a specific target, use:

```bash
systemctl list-dependencies multi-user.target | grep httpd
```

<h1>Systemd timers</h1>
<code>Systemd</code> is currently included in all major Linux distributions. It may be used to start and stop services as well as perform activities at particular periods using "timers."

Use the following command to determine which services are enabled on your system: 

```bash
systemctl list-timers
```

<h1>Challenges</h1> 
1. Look at the systemd timers and determine which services are enabled on your system.
2. Write a custom service that starts MySql docker container when the system boots.
