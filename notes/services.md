## What are services?

A service usually responds to requests from other programs. It uses inter-process communication mechanisms, like sockets, to communicate with other programs.

You can use services, when you want to have a program that:

- Runs in the background.
- Starts automatically when the computer boots up.
- Is globally available within the system.

Or perhaps you just want to execute various  programs in a specific order after booting up. 

What can you do with services?

- You can tell them to start or stop executing (single time).
- You can enable or disable them (starting and stopping automatically on system startup).

How it works internally?

`SystemD` executes different scripts at boot time, those scripts are known as `units`. Units include services, mounts and sockets. To display all of them, use:

```bash
systemctl -t help
```

Don't mix up `SystemD` and `systemctl`! `SystemD` is what all major distros use to manage their services, while `systemctl` is a command line tool used to communicate with `SystemD`. The `systemctl` utility is like a swiss knife for everything that has to do with services.

What are some examples of services?

1. An example of a `SystemD` service is the `sshd` service. It starts a `SSH` server when the system boots. 
2. Anoter example is the `httpd` service. It acts as a server in a client-server architecture, employing the HTTP and/or HTTPS network protocols. 

## What is a daemon?
A daemon is a program that runs in the background. It is usually used to perform a task, like monitoring a system, or to provide a service. Daemons are usually started by the system, but it is also possible to start them manually. In constrasts to programs run by the user, a daemon is not under the direct control of a user. Daemons are configured with `rc` and `init` scripts, that are typically located in `/etc/rc.d` and `/etc/init.d`.

To list the services intalled on the current system, use:

```bash
ls /etc/init.d
```

The tools that you can use to edit those files include:

* `systemctl` for `SystemD`
* `service` or `chkconfig` for `SysV`

## Managing services

Some services are always running, whereas others run once and then stop. 

To display the status of a service (in this example httpd), use one of the following:

```bash
# chkconfig 
chkconfig httpd status

# systemd 
systemctl status httpd.service
```

To enable a service (in this example httpd), use one of the following:

```bash
# chkconfig 
chkconfig httpd on

# systemd 
systemctl enable httpd.service
```

To disable a service (in this example httpd), use one of the following:

```bash
# chkconfig 
chkconfig httpd off

# systemd 
systemctl disable httpd.service
```

To start a service (in this example httpd), use one of the following:

```bash
# chkconfig 
service httpd start

# systemd 
systemctl start httpd.service
```

To stop a service (in this example httpd), use one of the following:

```bash
# chkconfig 
service httpd stop

# systemd 
systemctl stop httpd.service
```

To check if service (in this example httpd) is dependent on a specific target, use one of the following:

```bash
systemctl list-dependencies multi-user.target | grep httpd
```

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

## Create a custom service

`SystemD` services should be placed at `/etc/systemd/system/`.

Common sections include:

* `[Unit]` describes the unit and defines dependencies.
* `[Service]` describes how to start and stop the service and request status installation.
* `[Install]` informs `SystemD` when the service should be launched during the boot process. 

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

You can read more about targets <a href="https://github.com/djeada/Linux-Notes/blob/main/notes/system_startup.md">here</a>.

## Challenges

1. Look at the `SystemD` timers and determine which services are enabled on your system.
1. Set up the following services: 
  - dhcpd, 
  - NFS, 
  - sshd, 
  - DNS (bind), 
  - mail (postfix, Sendmail), 
  - web (Nginx, apache, caddy, traefik), 
  - database(MySQL, Postgres);
