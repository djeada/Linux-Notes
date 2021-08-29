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
