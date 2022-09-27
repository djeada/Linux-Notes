## What are services?
You can use services, when you want to run a program:

- In the background.
- Start automatically when the computer boots up.
- Run various applications in a specific order after the boot up.
- Make it globally available within the system.

What can you do with services?

- Start/stop (single time)
- Enable/disable (starting and stopping automatically on system startup)

`Systemd` executes different scripts at boot time, those scripts are known as `units`. Units include services, mounts and sockets. To display all of them, use:

```bash
systemctl -t help
```

Don't mix up `systemd` and `systemctl`! `Systemd` is what all major distros use to manage their services, while `systemctl` is a command line tool used to communicate with `systemd`. The `systemctl` utility is like a swiss knife for everything that has to do with services.

Thus, services are often used to run programs at boot time, but you can start and stop services at any time. 

1. An example of a systemd service is the `sshd` service. It starts the SSH server when the system boots. 
2. Anoter example is the `httpd` service. It acts as a server in a client-server architecture, employing the HTTP and/or HTTPS network protocols. 

A service usually responds to requests from other programs. It uses inter-process communication mechanisms, like sockets, to communicate with other programs.

## What is a daemon?
A daemon is a program that runs in the background. It is usually used to perform a task, like monitoring a system, or to provide a service. Daemons are usually started by the system, but it is also possible to start them manually. In constrasts to programs run by the user, a daemon is not under the direct control of a user. Daemons are configured with `rc` and `init` scripts, that are typically located in /etc/rc.d and /etc/init.d.

## Create a custom service

Systemd services should be placed at /etc/systemd/system/.

Common sections include:

* `[Unit]` describes the unit and defines dependencies.
* `[Service]` describes how to start and stop the service and request status installation.
* `[Install]` informs systemd when the service should be launched during the boot process. 

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

You can read more about targets <a href="https://github.com/djeada/Linux-Notes/edit/main/notes/booting.md">here</a>.

## Service statuses

| Status | Description |
| --- | --- |
| `Loaded` | The unit file was processed, and the unit is now active. |
| `Active(running)` | The unit is active with one or more processes. |
| `Active(exited)` | A one-time task was successfully performed. |
| `Active(waiting)` | The unit is active and waiting for an event. |
| `Inactive</b>` | The unit is not running.  |
| `Enabled` | The unit will be started at boot time. |
| `Disabled` |The unit will not be started at boot time. |
| `Static` | The unit can't be enabled, but can be started by another unit manually. |

## The systemctl command

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

## Systemd timers
`Systemd` is currently included in all major Linux distributions. It may be used to start and stop services as well as perform activities at particular periods using "timers."

Use the following command to determine which services are enabled on your system: 

```bash
systemctl list-timers
```

## Challenges

1. Look at the systemd timers and determine which services are enabled on your system.
1. Set up the following services: 
  - dhcpd, 
  - NFS, 
  - sshd, 
  - DNS (bind), 
  - mail (postfix, Sendmail), 
  - web (Nginx, apache, caddy, traefik), 
  - database(MySQL, Postgres);
