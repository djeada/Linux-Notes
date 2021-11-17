<h1>What are services?</h1>
Services are pften used to run programs at boot time, but you can start and stop services at any time. An example of a systemd service is the <code>sshd</code> service. It starts the SSH server when the system boots. Anoter example is the <code>cron</code> service. It runs the cron daemon. A service usually responds to requests from other programs. It uses inter-process communication mechanisms,like sockets, to communicate with other programs. Web servers may provide serivces, like HTTP, HTTPS, FTP, and SSH.

<h1>What is a daemon?</h1>
A daemon is a program that runs in the background. It is usually used to perform a task, like monitoring a system, or to provide a service. Daemons are usually started by the system, but you can start them manually. In constrasts to programs run by the user, a daemon is not under the direct control of a user. Daemons are configured with rc and init scripts, that are typically located in /etc/rc.d and /etc/init.d.

<h1>Create a custom service</h1>

Systemd services should be placed at /etc/systemd/system/.

An example of a foo.service script:

```bash
[Unit]
Description=Sample Script Startup

[Service]
Type=idle
ExecStart=/valid/path/to/an/executable/file

[Install]
WantedBy=multi-user.target
```

<h1>systemctl</h1>

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

<h1>systemd timers</h1>
<i>systemd</i> is currently included in all major Linux distributions. It may be used to start and stop services as well as perform activities at particular periods using "timers."

Use the following command to determine which services are enabled on your system: 

```bash
systemctl list-timers
```

<h1>Challenges</h1> 
1. Look at the systemd timers and determine which services are enabled on your system.
2. Write a custom service that starts MySql docker container when the system boots.
