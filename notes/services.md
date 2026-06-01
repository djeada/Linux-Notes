## Services, Daemons, and systemd
A service is a background program that provides a function to the system, users, or other programs.

Services usually run without direct user interaction. They may start automatically when the system boots, listen for network connections, process scheduled work, write logs, or respond to requests from other programs.

Common examples include:

| Service          | Description                 |
| ---------------- | --------------------------- |
| `sshd`           | SSH server for remote login |
| `nginx`          | Web server                  |
| `httpd`          | Apache web server           |
| `cron`           | Scheduled task service      |
| `mariadb`        | Database server             |
| `postgresql`     | Database server             |
| `vsftpd`         | FTP server                  |
| `NetworkManager` | Network management service  |

The main idea is:

- A service provides a function.
- A daemon is often the background process that provides that function.
- systemd manages services on many modern Linux systems.

### Service Management Big Picture
Modern Linux systems commonly use `systemd` to manage services.

The command-line tool used to control systemd is:

```bash id="jgjd0x"
systemctl
```

A simplified model looks like this:

```text id="elzvks"
+--------------------------------------------------+
|                Linux Operating System            |
|                                                  |
|    +------------------------+   +-------------+  |
|    |     Service Manager    |   | User        |  |
|    |       systemd          |<--| Commands    |  |
|    +------------------------+   | systemctl   |  |
|         |         ^             +-------------+  |
|         |         |                              |
|   start |         | stop/restart/status          |
| enable |         | disable                       |
|         v         |                              |
|    +------------------------+                    |
|    |      Linux Service     |                    |
|    |                        |                    |
|    | - runs in background   |                    |
|    | - performs tasks       |                    |
|    | - listens on ports     |                    |
|    | - writes logs          |                    |
|    | - responds to events   |                    |
|    +------------------------+                    |
|                                                  |
+--------------------------------------------------+
```

The administrator uses `systemctl` to ask systemd to start, stop, enable, disable, restart, reload, or inspect services.

### Services vs Processes
A process is a running instance of a program.

A service is a managed system function, usually represented by one or more processes.

For example:

```text id="vz8z1l"
Service:
sshd.service

Process:
PID 1234 running /usr/sbin/sshd
```

A service may have one process, several worker processes, or no long-running process if it is a one-shot task.

```text id="n9u8k7"
systemd unit: nginx.service
        |
        v
main process: nginx master
        |
        v
worker processes: nginx workers
```

So a service is not exactly the same thing as a process.

A service is the managed unit. A process is the actual running program.

### Daemons
A daemon is a background process that usually runs independently of direct user control.

Many daemon names end with the letter `d`.

Examples:

- sshd     SSH daemon
- httpd    HTTP daemon
- crond    cron daemon
- slapd    LDAP daemon
- vsftpd   Very Secure FTP daemon

A daemon often starts during boot and keeps running until shutdown.

The word daemon describes how the program runs:

- background
- non-interactive
- long-running
- system-managed

### Daemon vs Service
A daemon describes a background process.

A service describes a function provided to the system or users.

- Daemon = how it runs
- Service = what it provides

Example:

- sshd is a daemon process.
- sshd.service is the systemd service unit.
- The service provides remote SSH login.

Daemons are often services, but not every service is a traditional daemon.

For example, a one-shot service may run once, complete a task, and exit.

### systemd
`systemd` is a service manager and initialization system used by many modern Linux distributions.

It is responsible for:

- starting system services
- stopping services during shutdown
- tracking service state
- managing dependencies
- starting services in the correct order
- capturing service logs through journald
- handling sockets, timers, mounts, and targets

At boot time, systemd starts the services and units needed to bring the system into a usable state.

### Units
In systemd, a unit is something systemd can manage.

Common unit types include:

- .service   system service
- .socket    socket activation unit
- .target    group of units, similar to a boot milestone
- .timer     scheduled activation unit
- .mount     mount point
- .automount automatic mount point
- .path      path-based activation
- .device    device unit

A service unit usually ends in:

```text id="yic63t"
.service
```

Example:

- sshd.service
- nginx.service
- vsftpd.service
- postgresql.service

To list active units:

```bash id="hq6qbh"
systemctl list-units
```

To list all service units, including inactive ones:

```bash id="w69hx2"
systemctl list-units --type=service --all
```

### Service States
A service can have several important states.

- loaded      systemd successfully read the unit file
- active      the unit is currently active
- inactive    the unit is not active
- failed      the unit tried to start but failed
- enabled     the unit is configured to start at boot
- disabled    the unit is not configured to start at boot
- static      the unit cannot be enabled directly
- masked      the unit is blocked from being started

Important distinction:

- start/stop controls the current running state.
- enable/disable controls boot-time behavior.

For example:

- A service can be active but disabled.
- That means it is running now, but will not automatically start at boot.

- A service can be inactive but enabled.
- That means it is stopped now, but should start at boot.

### Checking Service Status
Use:

```bash id="eryt7y"
systemctl status sshd.service
```

or sometimes, depending on distribution:

```bash id="grm43e"
systemctl status ssh.service
```

Example output:

```text id="zrr0x8"
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-06-01 10:30:00 CEST; 5min ago
   Main PID: 1234 (sshd)
      Tasks: 1
     Memory: 6.2M
        CPU: 120ms
     CGroup: /system.slice/sshd.service
             └─1234 /usr/sbin/sshd -D
```

Interpretation: 


- Loaded means systemd found and loaded the unit file.
- enabled means the service is configured to start at boot.
- active (running) means it is currently running.
- Main PID shows the main service process.

If a service is broken, status output often includes recent log lines.

### Starting and Stopping Services
To start a service immediately:

```bash id="oyr7pr"
sudo systemctl start sshd.service
```

To stop it immediately:

```bash id="pedn3m"
sudo systemctl stop sshd.service
```

To restart it:

```bash id="wi14iy"
sudo systemctl restart sshd.service
```

To reload configuration without fully stopping the service, if supported:

```bash id="ho8tks"
sudo systemctl reload sshd.service
```

If you are not sure whether reload is supported, use:

```bash id="ngs5ji"
sudo systemctl reload-or-restart sshd.service
```

### Enabling and Disabling Services
To enable a service at boot:

```bash id="wj56sy"
sudo systemctl enable sshd.service
```

Example output:

```text id="xe1vs5"
Created symlink /etc/systemd/system/multi-user.target.wants/sshd.service → /usr/lib/systemd/system/sshd.service.
```

Interpretation: 


- systemd created a startup link.
- The service should start automatically at boot.

To disable a service at boot:

```bash id="vkrzab"
sudo systemctl disable sshd.service
```

This prevents automatic startup, but it does not necessarily stop the service right now.

To enable and start at the same time:

```bash id="a07pqc"
sudo systemctl enable --now sshd.service
```

To disable and stop at the same time:

```bash id="eo91uy"
sudo systemctl disable --now sshd.service
```

### Masking Services
Masking is stronger than disabling.

A disabled service can still be started manually.

A masked service cannot be started unless it is unmasked first.

Mask a service:

```bash id="ix4izt"
sudo systemctl mask service-name.service
```

Unmask it:

```bash id="wczkos"
sudo systemctl unmask service-name.service
```

Use masking carefully. It is useful when you want to prevent a service from being started by mistake or by another dependency.

### Listing Services
List active services:

```bash id="kkegp5"
systemctl list-units --type=service
```

List all services:

```bash id="w1s5cz"
systemctl list-units --type=service --all
```

List enabled services:

```bash id="vvqcna"
systemctl list-unit-files --type=service | grep enabled
```

List failed services:

```bash id="sdv395"
systemctl --failed
```

Example failed output:

```text id="izlutk"
UNIT                  LOAD   ACTIVE SUB    DESCRIPTION
myapp.service          loaded failed failed My Test Service
```

Interpretation: 


- myapp.service tried to run but failed.
- Use systemctl status and journalctl to inspect why.

### Service Logs with `journalctl`
systemd services usually log to the system journal.

To view logs for a service:

```bash id="mx8l67"
journalctl -u sshd.service
```

To view logs from the current boot:

```bash id="c4ueea"
journalctl -u sshd.service -b
```

To follow logs live:

```bash id="s2o1pb"
journalctl -u sshd.service -f
```

To show recent lines:

```bash id="rp4gk6"
journalctl -u sshd.service -n 50
```

Example output:

```text id="gdd8t4"
Jun 01 10:30:00 host systemd[1]: Started OpenSSH server daemon.
Jun 01 10:32:10 host sshd[1500]: Accepted publickey for adam from 192.168.1.20 port 53022
```

Interpretation: 


- The service started successfully.
- A user logged in using an SSH public key.

### Dependencies
Services may depend on other units.

For example, a web service may need the network to be online before it starts.

To list dependencies:

```bash id="bv3s7c"
systemctl list-dependencies nginx.service
```

To see what depends on a service:

```bash id="cep7x3"
systemctl list-dependencies --reverse nginx.service
```

To check dependencies of a target:

```bash id="c9wqji"
systemctl list-dependencies multi-user.target
```

Example:

```bash id="vz3lca"
systemctl list-dependencies multi-user.target | grep sshd
```

If output appears, `sshd.service` is part of that dependency tree.

### Targets
A target is a group of units.

Targets are similar to boot milestones.

Common targets:

- basic.target        basic system initialization
- multi-user.target   multi-user text/server mode
- graphical.target    graphical desktop mode
- rescue.target       rescue mode
- emergency.target    minimal emergency shell

To see the default target:

```bash id="ohqr4s"
systemctl get-default
```

Example output:

```text id="eybrvv"
graphical.target
```

Set default target:

```bash id="a0hjnq"
sudo systemctl set-default multi-user.target
```

### Older Service Management Tools
Older Linux systems may use SysV init scripts.

Common tools include:

- service
- chkconfig
- /etc/init.d/

List old init scripts:

```bash id="n44btd"
ls /etc/init.d
```

Start a service using the older interface:

```bash id="f6cj4v"
sudo service httpd start
```

Enable a service on older Red Hat-style systems:

```bash id="wxm9vz"
sudo chkconfig httpd on
```

Modern systems often keep the `service` command as a compatibility layer, but `systemctl` is preferred on systemd systems.

### Installing and Managing an FTP Server Example
The uploaded notes use `vsftpd` as an example service.

FTP is useful for learning service management, ports, logs, and testing, but it is usually not preferred for secure production file transfer unless configured carefully with encryption. For secure remote administration, SSH/SFTP is usually safer.

### Installing `vsftpd`
On Red Hat/CentOS-style systems:

```bash id="d423gy"
sudo yum install vsftpd
```

or newer systems:

```bash id="p2w2wy"
sudo dnf install vsftpd
```

On Debian/Ubuntu systems:

```bash id="i3d2gu"
sudo apt install vsftpd
```

Check if it is installed on RPM-based systems:

```bash id="sa9eth"
rpm -qa | grep vsftpd
```

Example output:

```text id="c54k8f"
vsftpd-3.0.2-29.el7.x86_64
```

Interpretation: 


```text id="orrfv1"
The vsftpd package is installed.
```

### Configuring `vsftpd`
The configuration file is commonly:

```text id="wcvv9x"
/etc/vsftpd/vsftpd.conf
```

Open it:

```bash id="gt4vcn"
sudo vi /etc/vsftpd/vsftpd.conf
```

Common options:

- anonymous_enable=NO
- local_enable=YES
- write_enable=YES

Meaning:

- anonymous_enable controls anonymous FTP access.
- local_enable allows local Linux users to log in.
- write_enable allows uploads and file changes.

After changing configuration, restart the service:

```bash id="vpfbdo"
sudo systemctl restart vsftpd.service
```

### Starting and Enabling `vsftpd`
Start now:

```bash id="u7ze5g"
sudo systemctl start vsftpd.service
```

Enable at boot:

```bash id="dj4s43"
sudo systemctl enable vsftpd.service
```

Enable and start together:

```bash id="jlvjjf"
sudo systemctl enable --now vsftpd.service
```

Check status:

```bash id="fxxggv"
systemctl status vsftpd.service
```

Example output:

```text id="t94vsb"
● vsftpd.service - Vsftpd ftp daemon
   Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2026-06-01 12:30:50 CEST; 5min ago
```

Interpretation: 


- The service is installed.
- It is enabled for boot.
- It is currently running.

### Checking Listening Ports
FTP normally listens on TCP port 21.

Use `ss`:

```bash id="ysh45q"
sudo ss -tulnp | grep ':21'
```

Example output:

```text id="zehwpm"
tcp LISTEN 0 32 0.0.0.0:21 0.0.0.0:* users:(("vsftpd",pid=1234,fd=3))
```

Interpretation: 


- vsftpd is listening on TCP port 21.
- The process ID is 1234.
- The service is ready for incoming FTP connections.

Older command:

```bash id="ojstjs"
sudo netstat -tulnp | grep ftp
```

On modern Linux, `ss` is usually preferred.

### Testing an FTP Service
Test locally:

```bash id="kesb4p"
ftp localhost
```

Example output:

```text id="rqjdk8"
Connected to localhost (127.0.0.1).
220 (vsFTPd 3.0.2)
Name (localhost:user):
```

Interpretation: 


- The FTP server accepted a connection.
- The 220 message means the server is ready.

Test from another machine:

```bash id="x1ndqu"
ftp SERVER_IP
```

If local testing works but remote testing fails, check:

- firewall rules
- network connectivity
- service listen address
- SELinux or security policy
- router or NAT rules

### Checking FTP Logs
Common log file:

```bash id="pg7kie"
sudo tail -f /var/log/vsftpd.log
```

Example output:

```text id="c3fa8k"
Mon Jun  1 12:35:15 2026 [pid 1235] CONNECT: Client "::1"
Mon Jun  1 12:35:16 2026 [pid 1235] [anonymous] OK LOGIN: Client "::1"
Mon Jun  1 12:36:20 2026 [pid 1236] [user] UPLOAD: Client "::1", "/home/user/testfile.txt"
```

Interpretation: 


- A client connected.
- Anonymous login succeeded.
- A file upload occurred.

You can also use systemd logs:

```bash id="l5sln6"
journalctl -u vsftpd.service -f
```

### Creating a Custom systemd Service
A custom service is defined using a unit file.

System-level service unit files are usually stored in:

```text id="le0gra"
/etc/systemd/system/
```

A simple service file has three main sections:

- [Unit]
- [Service]
- [Install]

### Unit File Sections
`[Unit]` describes the service and its ordering or dependencies.

Common directives:

- Description=
- Documentation=
- After=
- Wants=
- Requires=

`[Service]` describes how the service runs.

Common directives:

- Type=
- ExecStart=
- ExecStop=
- ExecReload=
- Restart=
- User=
- WorkingDirectory=
- Environment=

`[Install]` describes how the service is enabled at boot.

Common directive:

```text id="ikxhlh"
WantedBy=multi-user.target
```

### Simple Custom Service Example
Create an executable script:

```bash id="fsl6qo"
sudo tee /usr/local/bin/sample-service.sh > /dev/null <<'EOF'
#!/bin/bash
while true; do
    echo "$(date): sample service is running"
    sleep 10
done
EOF

sudo chmod +x /usr/local/bin/sample-service.sh
```

Create a service unit:

```bash id="qsg9na"
sudo tee /etc/systemd/system/sample.service > /dev/null <<'EOF'
[Unit]
Description=Sample Script Service

[Service]
Type=simple
ExecStart=/usr/local/bin/sample-service.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

Reload systemd:

```bash id="anxx8g"
sudo systemctl daemon-reload
```

Start the service:

```bash id="ydmklj"
sudo systemctl start sample.service
```

Check status:

```bash id="fitf0f"
systemctl status sample.service
```

Example output:

```text id="uw18h0"
● sample.service - Sample Script Service
     Loaded: loaded (/etc/systemd/system/sample.service; disabled)
     Active: active (running) since Mon 2026-06-01 13:00:00 CEST
   Main PID: 2401 (sample-service)
```

Interpretation: 


- The custom service is loaded.
- It is currently running.
- It is disabled, so it will not start at boot unless enabled.

Enable it:

```bash id="rjvbeo"
sudo systemctl enable sample.service
```

### Common Service Types
The `Type=` field controls how systemd decides whether a service has started successfully.

Common types:

- simple      process started by ExecStart is the main process
- exec        similar to simple, but waits until exec succeeds
- forking     service forks into background
- oneshot     command runs once and exits
- notify      service tells systemd when it is ready
- idle        waits until other startup jobs are dispatched

For most simple scripts, use:

```text id="tdenrd"
Type=simple
```

For one-time tasks, use:

```text id="j6e7no"
Type=oneshot
```

### Scenario 1: Simulate a Stopped Service

Practice identifying when a service is installed but not running.

#### Simulate the Problem
Use the sample service or another safe test service:

```bash id="t38yz0"
sudo systemctl stop sample.service
```

#### Check Status
```bash id="mgscmo"
systemctl status sample.service
```

Example output:

```text id="g41z80"
● sample.service - Sample Script Service
     Loaded: loaded (/etc/systemd/system/sample.service; enabled)
     Active: inactive (dead)
```

Interpretation: 

- The service exists.
- It is enabled for boot.
- It is not currently running.
- This is a runtime state problem, not a boot enablement problem.

#### Fix
```bash id="vi8d32"
sudo systemctl start sample.service
```

Verify:

```bash id="m9krvh"
systemctl status sample.service
```

Expected:

```text id="t1c86z"
Active: active (running)
```

### Scenario 2: Simulate a Disabled Service

Understand the difference between stopped and disabled.

#### Simulate the Problem
```bash id="p78d45"
sudo systemctl disable sample.service
```

Check:

```bash id="klr5w0"
systemctl is-enabled sample.service
```

Example output:

```text id="eqgr6t"
disabled
```

The service may still be running.

Check:

```bash id="g4g4wa"
systemctl is-active sample.service
```

Example output:

```text id="xqnhrf"
active
```

Interpretation: 

- The service is running now.
- But it will not automatically start at boot.
- This is boot-time configuration, not current runtime state.

#### Fix
```bash id="qbvhro"
sudo systemctl enable sample.service
```

Or enable and start:

```bash id="v6gdzg"
sudo systemctl enable --now sample.service
```

### Scenario 3: Simulate a Service That Fails Because ExecStart Is Wrong

Practice diagnosing a failed custom service.

#### Simulate the Problem
Create a broken unit:

```bash id="pcbv25"
sudo tee /etc/systemd/system/broken.service > /dev/null <<'EOF'
[Unit]
Description=Broken Service Example

[Service]
Type=simple
ExecStart=/not/a/real/path

[Install]
WantedBy=multi-user.target
EOF
```

Reload and start:

```bash id="xrqci5"
sudo systemctl daemon-reload
sudo systemctl start broken.service
```

#### Check Status
```bash id="vq9k3g"
systemctl status broken.service
```

Example output:

```text id="ez8v4z"
● broken.service - Broken Service Example
     Loaded: loaded (/etc/systemd/system/broken.service; disabled)
     Active: failed (Result: exit-code)
    Process: 2500 ExecStart=/not/a/real/path (code=exited, status=203/EXEC)
```

Interpretation: 

- status=203/EXEC usually means systemd could not execute the command.
- The ExecStart path is wrong, missing, or not executable.

#### Check Logs
```bash id="zfj1v1"
journalctl -u broken.service -b
```

Example output:

```text id="b87n12"
systemd[1]: broken.service: Failed to locate executable /not/a/real/path
systemd[1]: broken.service: Failed at step EXEC spawning /not/a/real/path: No such file or directory
```

#### Fix
Edit the unit:

```bash id="hpygx0"
sudo systemctl edit --full broken.service
```

Set a valid executable path.

Then reload and restart:

```bash id="s3uvhy"
sudo systemctl daemon-reload
sudo systemctl restart broken.service
```

### Scenario 4: Simulate a Service Crash and Auto-Restart

Show how `Restart=` affects service behavior.

#### Create a Crashing Script
```bash id="ng6fja"
sudo tee /usr/local/bin/crash-service.sh > /dev/null <<'EOF'
#!/bin/bash
echo "crash service started"
sleep 2
echo "crash service exiting with error"
exit 1
EOF

sudo chmod +x /usr/local/bin/crash-service.sh
```

Create the unit:

```bash id="dlky5q"
sudo tee /etc/systemd/system/crash.service > /dev/null <<'EOF'
[Unit]
Description=Crash Test Service

[Service]
Type=simple
ExecStart=/usr/local/bin/crash-service.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

Start it:

```bash id="u3uw7z"
sudo systemctl daemon-reload
sudo systemctl start crash.service
```

#### Check Status
```bash id="mjbkc1"
systemctl status crash.service
```

Example output:

```text id="xjrh4p"
● crash.service - Crash Test Service
     Loaded: loaded (/etc/systemd/system/crash.service; disabled)
     Active: activating (auto-restart) (Result: exit-code)
    Process: 2701 ExecStart=/usr/local/bin/crash-service.sh (code=exited, status=1/FAILURE)
```

Interpretation: 

- The service exits with an error.
- systemd is restarting it because Restart=always is set.
- This can create a restart loop if the underlying problem is not fixed.

#### Check Logs
```bash id="j8m5bb"
journalctl -u crash.service -f
```

Example output:

```text id="rzumc3"
crash-service.sh[2701]: crash service started
crash-service.sh[2701]: crash service exiting with error
systemd[1]: crash.service: Main process exited, code=exited, status=1/FAILURE
systemd[1]: crash.service: Scheduled restart job, restart counter is at 3.
```

#### Fix
Fix the script or change restart policy.

Stop the test:

```bash id="r0gcg9"
sudo systemctl stop crash.service
```

### Scenario 5: Simulate a Port Conflict

Understand why a network service may fail to start when its port is already in use.

#### Simulate the Problem
Start a temporary listener on port 8080:

```bash id="sb6w23"
python3 -m http.server 8080
```

In another terminal, check the port:

```bash id="bjjv0p"
ss -tulnp | grep ':8080'
```

Example output:

```text id="xi48yc"
tcp LISTEN 0 5 0.0.0.0:8080 0.0.0.0:* users:(("python3",pid=3001,fd=3))
```

Now start another service configured to use the same port.

Example failure log may look like:

```text id="gq5nhp"
Address already in use
Failed to bind to 0.0.0.0:8080
```

Interpretation: 

- The service is not failing because systemd is broken.
- It is failing because another process already owns the port.

#### Fix
Find and stop the conflicting process:

```bash id="j7hzi1"
sudo ss -tulnp | grep ':8080'
sudo kill 3001
```

Or configure one service to use a different port.

### Scenario 6: Simulate a Service Configuration Error

Practice checking service logs after a bad configuration change.

#### Simulate the Problem
For a real service like `nginx`, a bad config might cause restart failure.

For a safer custom example, create a script that exits when a config file contains `bad`.

```bash id="edoy8q"
sudo tee /usr/local/bin/config-check-service.sh > /dev/null <<'EOF'
#!/bin/bash
if grep -q bad /etc/config-check-service.conf; then
    echo "Bad configuration found"
    exit 1
fi

echo "Configuration OK"
sleep infinity
EOF

sudo chmod +x /usr/local/bin/config-check-service.sh
echo "bad=true" | sudo tee /etc/config-check-service.conf
```

Create service:

```bash id="xo13ak"
sudo tee /etc/systemd/system/config-check.service > /dev/null <<'EOF'
[Unit]
Description=Config Check Service

[Service]
Type=simple
ExecStart=/usr/local/bin/config-check-service.sh

[Install]
WantedBy=multi-user.target
EOF
```

Start it:

```bash id="tnxuu6"
sudo systemctl daemon-reload
sudo systemctl start config-check.service
```

#### Check Status
```bash id="l3xbim"
systemctl status config-check.service
```

Example output:

```text id="pnqyd8"
Active: failed (Result: exit-code)
Process: 3100 ExecStart=/usr/local/bin/config-check-service.sh (code=exited, status=1/FAILURE)
```

#### Check Logs
```bash id="bjjtrg"
journalctl -u config-check.service -b
```

Example output:

```text id="im36x1"
config-check-service.sh[3100]: Bad configuration found
```

Interpretation: 

- The service started successfully enough to run the script.
- The script rejected the configuration and exited.
- The issue is application configuration, not systemd itself.

#### Fix
```bash id="z499qh"
echo "good=true" | sudo tee /etc/config-check-service.conf
sudo systemctl restart config-check.service
```

### Scenario 7: Simulate a Missing Dependency or Wrong Startup Order

Understand service ordering with `After=` and `Wants=`.

Suppose a service needs the network before starting.

A unit may include:

```systemd id="gq0lbj"
[Unit]
Description=Network Dependent App
Wants=network-online.target
After=network-online.target
```

Meaning:

- Wants asks systemd to start network-online.target too.
- After controls ordering, so this service starts after network-online.target.

#### Check Dependencies
```bash id="xh7o87"
systemctl list-dependencies network-online.target
```

Check reverse dependencies:

```bash id="wdljpw"
systemctl list-dependencies --reverse network-online.target
```

Interpretation: 

- If a network-dependent service starts too early, it may fail because DNS or network routes are not ready.
- Use After= and Wants= carefully to express startup requirements.

Important note:

- After= only controls order.
- It does not automatically pull in the dependency.
- Use Wants= or Requires= when the other unit should also be started.

### Scenario 8: Simulate a Failed Service and Reset Its State

Understand failed state and how to clear it.

#### Simulate Failure
Use the broken service:

```bash id="ecw5vo"
sudo systemctl start broken.service
```

Check failed services:

```bash id="r72ez4"
systemctl --failed
```

Example output:

```text id="qg09d6"
UNIT             LOAD   ACTIVE SUB    DESCRIPTION
broken.service   loaded failed failed Broken Service Example
```

Interpretation: 

- systemd remembers that the service failed.
- Even after fixing the issue, the failed state may remain until reset.

#### Reset Failed State
```bash id="dmkh5p"
sudo systemctl reset-failed broken.service
```

Check again:

```bash id="m7hzhz"
systemctl --failed
```

Expected output:

```text id="lqqsx2"
0 loaded units listed.
```

### Scenario 9: Simulate a Masked Service

Understand why a service may refuse to start even though it exists.

#### Simulate
```bash id="vxa55x"
sudo systemctl mask sample.service
```

Try to start it:

```bash id="b3oj97"
sudo systemctl start sample.service
```

Example output:

```text id="igc140"
Failed to start sample.service: Unit sample.service is masked.
```

Interpretation: 

- The service is intentionally blocked.
- Starting it is not allowed while it is masked.

#### Fix
```bash id="x6izyl"
sudo systemctl unmask sample.service
sudo systemctl start sample.service
```

### Scenario 10: Simulate a Service Consuming Too Much CPU

Use service monitoring tools to identify a resource-heavy service.

#### Create a CPU-Heavy Service
```bash id="s146ys"
sudo tee /usr/local/bin/cpu-service.sh > /dev/null <<'EOF'
#!/bin/bash
while true; do
    :
done
EOF

sudo chmod +x /usr/local/bin/cpu-service.sh
```

Create unit:

```bash id="yh525g"
sudo tee /etc/systemd/system/cpu-test.service > /dev/null <<'EOF'
[Unit]
Description=CPU Test Service

[Service]
Type=simple
ExecStart=/usr/local/bin/cpu-service.sh

[Install]
WantedBy=multi-user.target
EOF
```

Start:

```bash id="w3qxkm"
sudo systemctl daemon-reload
sudo systemctl start cpu-test.service
```

#### Check with `systemctl status`
```bash id="tcv7tb"
systemctl status cpu-test.service
```

Example output:

```text id="k5ywc7"
● cpu-test.service - CPU Test Service
     Active: active (running)
   Main PID: 3500 (cpu-service.sh)
      Tasks: 1
        CPU: 1min 20s
```

#### Check with `top`
```bash id="kpcgww"
top -p 3500
```

Example output:

```text id="zp0jg9"
PID USER  PR NI  VIRT RES SHR S %CPU %MEM TIME+ COMMAND
3500 root 20  0  4000 900 800 R 99.9  0.0  1:20 cpu-service.sh
```

Interpretation: 

- The service is active.
- Its main process is consuming nearly one full CPU core.
- This is a service-level CPU bottleneck.

#### Fix
Stop the test service:

```bash id="rvonjp"
sudo systemctl stop cpu-test.service
```

For real services, investigate configuration, loops, workload spikes, or bugs.

### Scenario 11: Create a One-Shot Service

Understand services that run once and exit successfully.

Create script:

```bash id="zkk11a"
sudo tee /usr/local/bin/oneshot-task.sh > /dev/null <<'EOF'
#!/bin/bash
echo "$(date): oneshot task ran" >> /var/log/oneshot-task.log
EOF

sudo chmod +x /usr/local/bin/oneshot-task.sh
```

Create unit:

```bash id="wp6xy5"
sudo tee /etc/systemd/system/oneshot-task.service > /dev/null <<'EOF'
[Unit]
Description=One Shot Task Example

[Service]
Type=oneshot
ExecStart=/usr/local/bin/oneshot-task.sh

[Install]
WantedBy=multi-user.target
EOF
```

Run:

```bash id="kqij03"
sudo systemctl daemon-reload
sudo systemctl start oneshot-task.service
```

Check status:

```bash id="y9qeyx"
systemctl status oneshot-task.service
```

Example output:

```text id="p1ppf6"
Active: inactive (dead)
Process: 3600 ExecStart=/usr/local/bin/oneshot-task.sh (code=exited, status=0/SUCCESS)
```

Interpretation: 


- The service is inactive now because the task finished.
- This is normal for Type=oneshot.
- status=0/SUCCESS means it completed successfully.

### Scenario 12: Timers as Scheduled Services

Understand systemd timers as an alternative to cron.

A timer activates a service on a schedule.

Create a timer for the one-shot task:

```bash id="wkfsb7"
sudo tee /etc/systemd/system/oneshot-task.timer > /dev/null <<'EOF'
[Unit]
Description=Run oneshot task every minute

[Timer]
OnCalendar=*:0/1
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

Reload and start timer:

```bash id="rqcizk"
sudo systemctl daemon-reload
sudo systemctl enable --now oneshot-task.timer
```

List timers:

```bash id="nyfm3j"
systemctl list-timers --all
```

Example output:

```text id="vzi41v"
NEXT                        LEFT LAST                        PASSED UNIT                 ACTIVATES
Mon 2026-06-01 14:01:00     30s  Mon 2026-06-01 14:00:00     30s    oneshot-task.timer   oneshot-task.service
```

Interpretation: 


- The timer runs oneshot-task.service every minute.
- The ACTIVATES column shows which service the timer starts.

### Service Troubleshooting Workflow
When a service is not working, troubleshoot in layers.

1. Is the service installed?
2. Does systemd know about the unit?
3. Is it enabled for boot?
4. Is it active right now?
5. Did it fail?
6. What do the logs say?
7. Is the configuration valid?
8. Are required ports available?
9. Are dependencies ready?
10. Are permissions, users, or paths wrong?

### Step 1: Check Unit Exists
```bash id="z3rrrt"
systemctl status service-name.service
```

If output says:

```text id="x2pkl0"
Unit service-name.service could not be found.
```

then the package may not be installed, or the unit name may be wrong.

Search unit files:

```bash id="f7zl54"
systemctl list-unit-files | grep service-name
```

### Step 2: Check Active State
```bash id="hyao9y"
systemctl is-active service-name.service
```

Possible output:

- active
- inactive
- failed
- unknown

### Step 3: Check Boot State
```bash id="liqals"
systemctl is-enabled service-name.service
```

Possible output:

- enabled
- disabled
- static
- masked

### Step 4: Read Status
```bash id="g86ssz"
systemctl status service-name.service
```

Look for:

- Loaded
- Active
- Main PID
- status code
- recent log lines

### Step 5: Read Logs
```bash id="efgcmz"
journalctl -u service-name.service -b
```

Follow logs:

```bash id="jo6h0x"
journalctl -u service-name.service -f
```

### Step 6: Check Ports
For network services:

```bash id="nx931n"
sudo ss -tulnp
```

Example:

```bash id="kpp8ay"
sudo ss -tulnp | grep ':80'
```

This helps answer:

- Is the service listening?
- Is another process already using the port?
- Is it listening on localhost only or all interfaces?

### Step 7: Check Processes
```bash id="tupbe8"
ps -ef | grep service-name
```

or use systemd’s process tree:

```bash id="ivra74"
systemctl status service-name.service
```

### Step 8: Check Configuration
Many services have a built-in config test.

Examples:

```bash id="si0gwe"
sudo nginx -t
sudo apachectl configtest
sudo sshd -t
```

If available, always test configuration before restarting production services.

### Common Service Problems and Fixes
#### Problem: Service Not Found
Example:

```text id="tlgx6j"
Unit nginx.service could not be found.
```

Possible causes:

- package not installed
- wrong service name
- unit file not reloaded
- custom unit placed in wrong location

Fix:

```bash id="zch4ax"
sudo systemctl daemon-reload
systemctl list-unit-files | grep nginx
```

#### Problem: Service Failed to Start
Check:

```bash id="vwt11a"
systemctl status service-name.service
journalctl -u service-name.service -b
```

Common causes:

- bad configuration
- missing executable
- wrong permissions
- port already in use
- missing dependency
- invalid user or group
- missing directory

#### Problem: Service Running but Not Reachable
Check:

```bash id="hestz6"
systemctl status service-name.service
sudo ss -tulnp
journalctl -u service-name.service -b
```

Possible causes:

- service listens only on localhost
- firewall blocks access
- wrong port
- network problem
- application-level access control
- SELinux/AppArmor policy

#### Problem: Service Starts Manually but Not at Boot
Check:

```bash id="kwwvd4"
systemctl is-enabled service-name.service
systemctl status service-name.service
```

If disabled:

```bash id="tzohua"
sudo systemctl enable service-name.service
```

If enabled but still fails at boot, check:

```bash id="kpil7x"
journalctl -u service-name.service -b
systemctl list-dependencies service-name.service
```

Possible causes:

- starts before network is ready
- missing mount at boot
- environment differs at boot
- dependency missing
- permissions or path issue

#### Problem: Service Keeps Restarting
Check:

```bash id="jx23pk"
systemctl status service-name.service
journalctl -u service-name.service -b
```

Look for:

- Scheduled restart job
- restart counter
- exit-code
- core dump
- configuration errors

Possible causes:

- application crashes
- bad config
- missing file
- health check failure
- Restart=always hides repeated failure

### Useful Command Summary
Service state:

```bash id="lng7o0"
systemctl status service.service
systemctl is-active service.service
systemctl is-enabled service.service
systemctl --failed
```

Start and stop:

```bash id="s781jo"
sudo systemctl start service.service
sudo systemctl stop service.service
sudo systemctl restart service.service
sudo systemctl reload service.service
sudo systemctl reload-or-restart service.service
```

Boot behavior:

```bash id="dxaetx"
sudo systemctl enable service.service
sudo systemctl disable service.service
sudo systemctl enable --now service.service
sudo systemctl disable --now service.service
```

Masking:

```bash id="xicyv7"
sudo systemctl mask service.service
sudo systemctl unmask service.service
```

Listing:

```bash id="qy9f7v"
systemctl list-units --type=service
systemctl list-units --type=service --all
systemctl list-unit-files --type=service
systemctl list-timers --all
```

Logs:

```bash id="n3rqpj"
journalctl -u service.service
journalctl -u service.service -b
journalctl -u service.service -f
journalctl -u service.service -n 50
```

Dependencies:

```bash id="gu0fey"
systemctl list-dependencies service.service
systemctl list-dependencies --reverse service.service
```

Ports and processes:

```bash id="qc5i06"
sudo ss -tulnp
ps -ef | grep service-name
```

Custom units:

```bash id="bvh76z"
sudo systemctl daemon-reload
sudo systemctl edit --full service.service
sudo systemctl reset-failed service.service
```

### Safe Lab Cleanup
If you created the sample services, clean them up:

```bash id="en9ptc"
sudo systemctl stop sample.service broken.service crash.service config-check.service cpu-test.service oneshot-task.timer oneshot-task.service 2>/dev/null

sudo systemctl disable sample.service broken.service crash.service config-check.service cpu-test.service oneshot-task.timer oneshot-task.service 2>/dev/null

sudo rm -f /etc/systemd/system/sample.service
sudo rm -f /etc/systemd/system/broken.service
sudo rm -f /etc/systemd/system/crash.service
sudo rm -f /etc/systemd/system/config-check.service
sudo rm -f /etc/systemd/system/cpu-test.service
sudo rm -f /etc/systemd/system/oneshot-task.service
sudo rm -f /etc/systemd/system/oneshot-task.timer

sudo rm -f /usr/local/bin/sample-service.sh
sudo rm -f /usr/local/bin/crash-service.sh
sudo rm -f /usr/local/bin/config-check-service.sh
sudo rm -f /usr/local/bin/cpu-service.sh
sudo rm -f /usr/local/bin/oneshot-task.sh
sudo rm -f /etc/config-check-service.conf

sudo systemctl daemon-reload
sudo systemctl reset-failed
```

### Challenges
1. Use `systemctl list-units --type=service --all` to list active and inactive services. Pick five services and explain what each one does.
2. Choose one service and inspect it with `systemctl status`, `systemctl is-active`, and `systemctl is-enabled`. Explain the difference between active and enabled.
3. Start, stop, restart, enable, and disable a safe test service. Record the command and output for each action.
4. Use `journalctl -u service-name -b` to inspect logs for a service. Identify when it started and whether it produced errors.
5. Install and configure a simple service such as `vsftpd`, `nginx`, or `openssh-server` on a lab machine. Verify that it is running and listening on the expected port.
6. Use `ss -tulnp` to identify which services are listening on network ports.
7. Create a custom systemd service that runs a script. Start it, check its status, view logs, enable it, and then clean it up.
8. Create a broken service with an invalid `ExecStart`. Start it, inspect the failure, fix it, and restart it.
9. Create a one-shot service and a timer that runs it every minute. Use `systemctl list-timers --all` to verify the schedule.
10. Explain the difference between a process, daemon, and service using examples such as `sshd`, `nginx`, and a one-shot backup task.
