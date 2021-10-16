<h1>systemctl</h1>

To display the status of a service, use:

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
