# Services, Boot and Kernel Quiz

Notes: [Services](../notes/services.md), [System Startup](../notes/system_startup.md), [Kernel](../notes/kernel.md), [Hardware](../notes/hardware.md)

Check your understanding of systemd units and `systemctl`, dependencies, targets and timers, the boot sequence, kernel modules and kernel parameters.

#### Q. `nginx.service` is stopped. You run the commands below. What does the last one print?

```bash
sudo systemctl enable nginx.service
systemctl is-active nginx.service
```

* [ ] `active`
* [x] `inactive`
* [ ] `enabled`
* [ ] `activating`

> **Explanation:** `enable` only sets up boot-time activation; it does not start anything. The service stays stopped until you run `systemctl start`, or use `enable --now` to do both in one step.

#### Q. Which command stops `sshd.service` now and also keeps it from starting at the next boot?

* [ ] `sudo systemctl disable sshd.service`
* [ ] `sudo systemctl stop sshd.service`
* [x] `sudo systemctl disable --now sshd.service`
* [ ] `sudo systemctl kill sshd.service`

> **Explanation:** `disable` only removes the boot-time symlinks and leaves a running service running; `stop` (and `kill`) affect only the current state. `--now` makes `disable` stop the unit as well.

#### Q. The unit file has `WantedBy=multi-user.target` in its `[Install]` section. What does `sudo systemctl enable app.service` do on disk?

* [x] Creates a symlink to the unit in `/etc/systemd/system/multi-user.target.wants/`
* [ ] Copies the unit file from `/usr/lib/systemd/system/` to `/etc/systemd/system/`
* [ ] Adds `app.service` to the `DefaultUnits=` list in `/etc/systemd/system.conf`
* [ ] Starts the unit and records its main PID under `/run/systemd/units/`

> **Explanation:** `enable` reads `[Install]` and creates the matching `.wants/` symlink, so `multi-user.target` pulls the unit in at boot. `[Install]` is read only by install commands such as `enable` and `disable`, never when the unit starts.

#### Q. You run the commands below. What happens?

```bash
sudo systemctl mask cups.service
sudo systemctl start cups.service
```

* [ ] cups starts, because masking only affects what happens at boot
* [ ] cups starts with a warning, and is stopped again at the next boot
* [ ] cups starts only if another unit lists it in `Requires=`
* [x] The start fails with `Unit cups.service is masked.`

> **Explanation:** `mask` links the unit name to `/dev/null`, so neither a manual `start` nor a dependency can start it. A disabled unit can still be started by hand; a masked one needs `systemctl unmask` first.

#### Q. A unit file has no `[Install]` section and is started only by another unit that lists it in `Wants=`. What does `systemctl is-enabled` print for it?

* [ ] `disabled`
* [x] `static`
* [ ] `masked`
* [ ] `indirect`

> **Explanation:** `static` means the unit has no install information, so there is nothing for `enable` to do; running `enable` on it prints a notice instead. Such units are started by other units or by socket, timer or D-Bus activation.

#### Q. You change `ExecStart=` in `/etc/systemd/system/app.service` and then run the command below without anything else. What does systemd run?

```bash
sudo systemctl restart app.service
```

* [x] The old `ExecStart=`, with a warning that the unit file changed on disk
* [ ] The new `ExecStart=`, because `restart` always rereads the unit file
* [ ] Nothing; `restart` refuses to run until you reload systemd
* [ ] The new `ExecStart=`, but only after the old process exits by itself

> **Explanation:** systemd works from the unit definitions it has loaded in memory. Until `systemctl daemon-reload`, a restart uses the old command and `systemctl` prints "changed on disk. Run 'systemctl daemon-reload'".

#### Q. You want to change a setting of the packaged `/usr/lib/systemd/system/nginx.service` so that the change survives package upgrades. What is the usual way?

* [ ] Edit `/usr/lib/systemd/system/nginx.service` directly and run `daemon-reload`
* [ ] Put the changed copy in `/run/systemd/system/nginx.service`
* [x] Add a drop-in under `/etc/systemd/system/nginx.service.d/`, for example with `systemctl edit nginx`
* [ ] Add the setting under a `[nginx.service]` section in `/etc/systemd/system.conf`

> **Explanation:** Files under `/etc/systemd/system` take precedence over `/usr/lib/systemd/system`, which upgrades overwrite. `systemctl edit` creates `override.conf` there and reloads systemd. `/run` is lost at reboot.

#### Q. `app.service` has `Type=simple`. You add the drop-in below, run `daemon-reload`, and `systemctl start app` fails with "bad unit file setting". Why?

```ini
# /etc/systemd/system/app.service.d/override.conf
[Service]
ExecStart=/usr/local/bin/app --verbose
```

* [ ] Drop-ins may only contain `[Unit]` settings, so the `[Service]` section is ignored
* [ ] The drop-in must be named `app.service.conf` and live next to the unit file
* [ ] `ExecStart=` paths in a drop-in must be relative to `WorkingDirectory=`
* [x] The drop-in adds a second `ExecStart=`; an empty `ExecStart=` line must clear the original first

> **Explanation:** `ExecStart=` is a list, so a drop-in appends to it. Only `Type=oneshot` may have several; others are refused. Put `ExecStart=` (empty) before the new line to reset the list.

#### Q. `systemctl status backup.service` shows the lines below for a `Type=oneshot` unit. What do they tell you?

```text
     Active: inactive (dead)
    Process: 3600 ExecStart=/usr/local/bin/backup.sh (code=exited, status=0/SUCCESS)
```

* [x] The script ran and finished successfully; inactive is normal after a oneshot completes
* [ ] The script crashed, and systemd gave up after too many restart attempts
* [ ] The unit is disabled, so the script was never started by systemd
* [ ] The script is still running in the background, detached from systemd

> **Explanation:** A oneshot unit is active only while its command runs, then goes back to inactive; `status=0/SUCCESS` shows a clean exit. With `RemainAfterExit=yes` it would stay `active (exited)` instead.

#### Q. `legacyd` forks into the background and its parent process exits at once. Its unit uses `Type=simple`. What happens after `systemctl start legacyd`?

* [ ] systemd follows the fork and adopts the child as the new main PID
* [x] systemd sees the main process exit, marks the unit inactive and kills the forked daemon
* [ ] The daemon keeps running, but `systemctl status` reports it as failed
* [ ] systemd restarts the parent process in an endless loop

> **Explanation:** With `Type=simple` the `ExecStart=` process is the service; when it exits, systemd stops the unit and kills what is left in its cgroup. Use `Type=forking` (with `PIDFile=`) or run the daemon in foreground mode.

#### Q. A unit has `Restart=on-failure`. Its main process exits with status 0. What does systemd do?

* [ ] Restarts it after `RestartSec=` has passed
* [ ] Marks the unit `failed` and restarts it once
* [x] Leaves it stopped, because a clean exit is not a failure
* [ ] Restarts it until `StartLimitBurst=` is reached

> **Explanation:** `on-failure` restarts only after a non-zero exit code, a fatal signal, a timeout or a watchdog failure. `Restart=always` would restart it even after a clean exit.

#### Q. A service with `Restart=always` crashes right after every start. After a few quick restarts, `systemctl status` shows `failed` and "Start request repeated too quickly". Why did systemd stop restarting it?

* [ ] `Restart=always` allows only five restarts over the unit's whole lifetime
* [ ] journald stopped accepting its messages, so systemd killed it
* [ ] `RestartSec=` expired before the service reached the active state
* [x] It hit the start rate limit, `StartLimitBurst=` starts within `StartLimitIntervalSec=`

> **Explanation:** By default a unit may start 5 times in 10 seconds; after that systemd refuses and marks it failed. Fix the crash, then `systemctl reset-failed` clears the counter and the failed state.

#### Q. A shell script must check whether `nginx.service` is running. Which test is reliable?

* [x] `systemctl is-active --quiet nginx`, which exits with status 0 only when the unit is active
* [ ] `systemctl is-enabled --quiet nginx`, which exits with status 0 when the service is running
* [ ] `systemctl status nginx`, which always exits with status 0 if the unit file exists
* [ ] `systemctl cat nginx`, which fails when the main process is not running

> **Explanation:** `is-active` reports the runtime state and returns non-zero (3 for inactive) otherwise; `--quiet` hides the output. `is-enabled` only tells you about boot-time setup, and `cat` just prints the unit file.

#### Q. You fixed a broken unit, but `systemctl --failed` still lists it from the earlier attempt. Which command clears that state?

* [ ] `sudo systemctl daemon-reload`
* [x] `sudo systemctl reset-failed broken.service`
* [ ] `sudo systemctl unmask broken.service`
* [ ] `sudo journalctl --rotate`

> **Explanation:** systemd remembers a unit's failed result until it starts successfully or you run `reset-failed`. `daemon-reload` rereads unit files but keeps unit state, and journal commands only affect logs.

#### Q. What is the difference between `systemctl reload app` and `systemctl restart app`?

* [ ] `reload` rereads the unit file; `restart` rereads the application's config
* [ ] `reload` works only for disabled units; `restart` only for enabled ones
* [ ] They are aliases; both stop and start the process with a new PID
* [x] `reload` asks the running process to reread its config; `restart` stops and starts it

> **Explanation:** `reload` runs the unit's `ExecReload=` (often a `SIGHUP`), so the main PID survives. Not every service supports it; `reload-or-restart` falls back to a restart. Rereading unit files is `daemon-reload`.

#### Q. `app.service` contains only `After=postgresql.service` in `[Unit]`. PostgreSQL is stopped. What happens when you run `systemctl start app`?

* [ ] PostgreSQL is started first, then app
* [x] app starts and PostgreSQL stays stopped
* [ ] app waits until someone starts PostgreSQL
* [ ] app refuses to start because PostgreSQL is inactive

> **Explanation:** `After=` only orders units that are both being started in the same transaction; it never pulls a unit in. Add `Wants=` or `Requires=` to have PostgreSQL started too.

#### Q. `db.service` fails to start. One app unit has `Requires=db.service` and `After=db.service`; another has `Wants=db.service` and `After=db.service`. Which statement is true?

* [x] The `Requires=` app is not started; the `Wants=` app starts anyway
* [ ] Both apps start; `Requires=` only logs a warning about the failure
* [ ] Neither app starts, because both wait for `db.service`
* [ ] The `Wants=` app is not started; the `Requires=` app starts after a retry

> **Explanation:** Both settings pull `db.service` in, but only `Requires=` (with `After=`) makes the start job of the app fail with "A dependency job failed". `Wants=` is the weak form: a failed dependency is ignored.

#### Q. `app.service` has `Requires=db.service` but no `After=` or `Before=`. `db.service` fails to start. What happens when you start `app.service`?

* [ ] app is not started, because `Requires=` always waits for the result
* [ ] systemd delays app until db has been retried
* [x] app starts anyway, because both start jobs run in parallel
* [ ] systemd refuses the transaction as an ordering cycle

> **Explanation:** Without an ordering dependency, systemd starts both at the same time and does not wait for db's result. A failed required unit blocks the requiring unit only when `After=` is also set.

#### Q. `app.service` has `Requires=db.service` and `After=db.service`, and both are running. What happens when you run `systemctl stop db.service`?

* [ ] Only db stops; app keeps running until it is restarted
* [ ] systemd refuses to stop db while app needs it
* [ ] db stops, and app is restarted to reconnect
* [x] app is stopped as well

> **Explanation:** With `Requires=`, explicitly stopping or restarting the required unit also stops or restarts the units that require it. With `Wants=`, app would keep running.

#### Q. A service fails at boot because it starts before the network is fully configured. Which `[Unit]` lines express "start the network-online milestone too, and start me after it"?

* [ ] `Wants=network.target` and `After=network.target`
* [ ] `Requires=network-online.target` and `Before=network-online.target`
* [x] `Wants=network-online.target` and `After=network-online.target`
* [ ] `After=network-online.target` and `WantedBy=network-online.target`

> **Explanation:** `Wants=` pulls the target into the boot and `After=` orders the service after it. `network.target` only means the network stack started, not that addresses are configured. `Before=` reverses the order, and `WantedBy=` belongs in `[Install]`.

#### Q. Which systemd target corresponds to SysV runlevel 3 (multi-user, networking, no GUI)?

* [x] `multi-user.target`
* [ ] `graphical.target`
* [ ] `basic.target`
* [ ] `rescue.target`

> **Explanation:** systemd ships `runlevel3.target` as a symlink to `multi-user.target`. Runlevel 5 maps to `graphical.target`, 1 to `rescue.target`, 0 to `poweroff.target` and 6 to `reboot.target`.

#### Q. You want a server to boot into text mode from now on, without ending the current graphical session. Which command?

* [ ] `sudo systemctl isolate multi-user.target`
* [x] `sudo systemctl set-default multi-user.target`
* [ ] `sudo systemctl enable multi-user.target`
* [ ] `sudo systemctl start multi-user.target`

> **Explanation:** `set-default` repoints the `default.target` symlink, which affects future boots only. `isolate` switches the running system right away and stops units the new target does not need, such as the display manager.

#### Q. What is the main difference between `rescue.target` and `emergency.target`?

* [ ] `emergency.target` mounts all filesystems and starts networking; `rescue.target` mounts none
* [ ] `rescue.target` needs a network connection for remote repair; `emergency.target` does not
* [ ] They are aliases of the same target, kept only for SysV compatibility
* [x] `rescue.target` mounts local filesystems and starts basic services; `emergency.target` starts almost nothing

> **Explanation:** Rescue mode is single-user mode with filesystems mounted. Emergency mode gives a shell with no other mounts or services, which helps when `/etc/fstab` or a filesystem check breaks the boot.

#### Q. In the GRUB menu you press `e` to edit the boot entry. What do you append to the `linux` line to boot once into rescue mode on a systemd system?

* [x] `systemd.unit=rescue.target`
* [ ] `init=rescue.target`
* [ ] `runlevel=rescue`
* [ ] `default.target=rescue`

> **Explanation:** systemd reads `systemd.unit=` from the kernel command line; `single` or `1` work too. Editing in GRUB lasts for one boot. `init=` expects a program path, not a unit name.

#### Q. Which timer setting runs a job every 15 minutes, like the cron schedule `*/15 * * * *`?

* [ ] `OnCalendar=15min`
* [ ] `OnCalendar=*-*-* *:15:00`
* [ ] `OnUnitActiveSec=*:15`
* [x] `OnCalendar=*:0/15`

> **Explanation:** `*:0/15` means any hour, minutes starting at 0 in steps of 15; `systemd-analyze calendar '*:0/15'` shows the next run times. `*:15:00` fires once an hour at minute 15, and `OnUnitActiveSec=` takes a time span.

#### Q. A laptop is often switched off at 03:00, when `backup.timer` (`OnCalendar=*-*-* 03:00:00`) should fire. Which line makes the missed run happen at the next boot?

* [ ] `AccuracySec=1us`
* [ ] `RandomizedDelaySec=1h`
* [ ] `WakeSystem=false`
* [x] `Persistent=true`

> **Explanation:** With `Persistent=true` systemd stores the last trigger time on disk and runs the service at once if a scheduled run was missed while the timer was inactive. It affects only `OnCalendar=` timers.

#### Q. You enable `backup.timer`, which has no `Unit=` line. Which unit does it start when it fires?

* [x] `backup.service`
* [ ] `backup.target`
* [ ] `timers.target`
* [ ] No unit, until you add `Unit=`

> **Explanation:** A timer activates the service with the same name by default; the `ACTIVATES` column of `systemctl list-timers` shows it. `timers.target` is only what timers are usually `WantedBy=`.

#### Q. Which statement describes an advantage of a systemd timer over a cron job?

* [ ] A timer uses the same five-field schedule syntax as `crontab`
* [ ] A timer can run a command without any matching unit file
* [x] Each run is a service unit, so its output and result show up in the journal and `systemctl status`
* [ ] A timer runs its job in the owner's login shell with the crontab environment

> **Explanation:** A timer starts a service unit, so you get journal logs, dependencies, resource limits and status for free. Cron needs its own logging or mail; timers need a `.service` file and their own `OnCalendar=` syntax.

#### Q. Which `[Timer]` settings run a job 10 minutes after boot and then 1 hour after each time it was last activated?

* [x] `OnBootSec=10min` and `OnUnitActiveSec=1h`
* [ ] `OnCalendar=10min` and `Persistent=true`
* [ ] `OnStartupSec=1h` and `OnCalendar=hourly`
* [ ] `OnActiveSec=10min` and `AccuracySec=1h`

> **Explanation:** `OnBootSec=` and `OnUnitActiveSec=` are monotonic timers, measured from boot and from the last activation of the unit. `OnCalendar=` takes calendar expressions such as `hourly`, and `AccuracySec=` only sets how precisely a timer fires.

#### Q. Which order matches a typical Linux boot?

* [ ] Bootloader, firmware POST, initramfs, kernel, PID 1
* [ ] Firmware POST, kernel, bootloader, PID 1, initramfs
* [x] Firmware POST, bootloader, kernel, initramfs, PID 1
* [ ] Firmware POST, initramfs, bootloader, kernel, PID 1

> **Explanation:** Firmware tests hardware and finds a boot target, the bootloader loads the kernel and initramfs, the initramfs prepares and mounts the real root, then `switch_root` runs PID 1 (systemd), which starts services.

#### Q. Which statement correctly contrasts BIOS and UEFI booting?

* [ ] BIOS loads a `.efi` file from a FAT partition; UEFI runs code from the first disk sector
* [x] BIOS runs boot code from the disk's first 512-byte sector; UEFI loads a `.efi` file from the EFI System Partition
* [ ] BIOS reads boot entries from NVRAM; UEFI always boots the first disk in the system
* [ ] Both load the kernel straight from `/boot` without a bootloader

> **Explanation:** The MBR holds 446 bytes of boot code that can only chain to a bigger loader. UEFI reads a boot entry from NVRAM and runs an EFI program such as `shimx64.efi` or `grubx64.efi` from the ESP, usually mounted at `/boot/efi`.

#### Q. On Ubuntu you want to add a kernel parameter to every future boot. What is the usual way?

* [ ] Edit `/boot/grub/grub.cfg` directly, since GRUB reads it at every boot
* [ ] Append the parameter to `/proc/cmdline`, then reboot the machine
* [ ] Add the parameter to `/etc/sysctl.conf` and apply it with `sysctl -p`
* [x] Add it to `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`, then run `sudo update-grub`

> **Explanation:** `grub.cfg` is generated, so manual edits are lost the next time it is rebuilt. Red Hat-style systems use `grub2-mkconfig -o /boot/grub2/grub.cfg` (or `grubby`). `/proc/cmdline` is read-only.

#### Q. Which command shows the parameters the running kernel was booted with?

* [ ] `uname -a`
* [x] `cat /proc/cmdline`
* [ ] `sysctl -a`
* [ ] `grep GRUB_CMDLINE /etc/default/grub`

> **Explanation:** `/proc/cmdline` holds the exact command line the bootloader passed, such as `root=UUID=... ro quiet splash`. `/etc/default/grub` describes future boots and may have changed since; `sysctl -a` lists runtime tunables.

#### Q. The root filesystem is on LVM inside a LUKS-encrypted partition. Why does this system need an initramfs?

* [ ] The kernel can only mount ext4 directly, so all other filesystems need it
* [ ] The initramfs holds the GRUB menu and the kernel parameters
* [ ] systemd refuses to run as PID 1 from an encrypted disk
* [x] The tools and drivers that unlock and assemble the root device must run before that root is available

> **Explanation:** The initramfs is a small filesystem in RAM with storage drivers, `cryptsetup`, LVM tools and scripts. It prepares and mounts the real root, then hands over with `switch_root`.

#### Q. After booting a self-built kernel you see the message below. What is the most likely cause?

```text
Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)
```

* [x] No usable initramfs or built-in driver for the root device, or a wrong `root=` parameter
* [ ] `sshd.service` failed to start, so systemd could not finish the boot
* [ ] The GRUB menu timeout is too short for the kernel to load its drivers
* [ ] `/etc/fstab` has a wrong UUID for the `/home` filesystem

> **Explanation:** The kernel could not find any block device to mount as root. Typical fixes: build the storage and filesystem drivers in, generate an initramfs for the new kernel, or correct `root=`. `/etc/fstab` is read later, by systemd.

#### Q. On Ubuntu you added `blacklist nouveau` under `/etc/modprobe.d/`, but the module still loads early in boot. Which command is usually needed next?

* [ ] `sudo update-grub`
* [x] `sudo update-initramfs -u`
* [ ] `sudo depmod -a`
* [ ] `sudo sysctl --system`

> **Explanation:** The initramfs carries its own copy of the modules and modprobe configuration, so it must be rebuilt to see the change. On RHEL/Fedora the equivalent is `sudo dracut -f`.

#### Q. `ps -p 1 -o comm,args` prints the line below on Ubuntu. Why does the command name differ from the arguments?

```text
COMMAND         COMMAND
systemd         /sbin/init splash
```

* [ ] PID 1 is SysV init, which starts systemd as a child process
* [ ] systemd renames itself after it finishes the boot
* [ ] The kernel always reports PID 1 as `/sbin/init`
* [x] `/sbin/init` is a symlink to systemd, and the kernel started it by that path

> **Explanation:** The kernel runs `/sbin/init` by default (or the `init=` parameter); here it links to `/usr/lib/systemd/systemd`. `comm` is the executable's name, while `args` shows how it was invoked. `splash` came from the kernel command line.

#### Q. What happens if PID 1 exits on a running Linux system?

* [ ] Another process is promoted to PID 1 and the system continues
* [x] The kernel panics, because there must always be an init process
* [ ] systemd restarts itself from the initramfs within a few seconds
* [ ] Only user sessions end; system services keep running

> **Explanation:** PID 1 reaps orphaned processes and manages the system, so the kernel cannot continue without it and panics with "Attempted to kill init!". That is why a crash of the init process is fatal.

#### Q. In a RHEL root password reset you boot with `rd.break` and run the commands below. Why is the last command needed?

```bash
mount -o remount,rw /sysroot
chroot /sysroot
passwd root
touch /.autorelabel
```

* [ ] It tells GRUB to drop `rd.break` from the kernel command line at the next boot
* [ ] It forces `fsck` to check the root filesystem during the next boot
* [x] SELinux relabels files at the next boot, fixing the label of the newly written `/etc/shadow`
* [ ] It makes `/sysroot` writable again after leaving the `chroot`

> **Explanation:** In the initramfs SELinux policy is not loaded, so `passwd` writes `/etc/shadow` without its proper label. Without a relabel, logins can fail. `rd.break` itself lasts only for the edited boot.

#### Q. `systemd-analyze blame` lists `backup-check.service` at the top with 20 s, yet removing it does not shorten the boot. What explains this?

* [ ] `blame` reports time spent in the firmware and loader, not in user space
* [ ] `blame` measures the CPU time used by each unit, not wall-clock time
* [x] Units start in parallel, so a slow unit off the critical path does not delay the target
* [ ] The times are cached and only updated after two more reboots

> **Explanation:** `blame` sorts units by their own start-up time. `systemd-analyze critical-chain` shows the chain of units that actually determined when the default target was reached.

#### Q. After adding a USB backup disk to `/etc/fstab`, the system drops to emergency mode whenever the disk is unplugged. Which mount option lets boot continue without it?

* [x] `nofail`
* [ ] `defaults`
* [ ] `errors=remount-ro`
* [ ] `relatime`

> **Explanation:** With `nofail`, a missing device no longer fails `local-fs.target`, so boot carries on. `errors=remount-ro` only changes what ext4 does on errors after the mount succeeded.

#### Q. `lsmod` prints the lines below. What does `1 ipt_REJECT` in the last column mean?

```text
Module                  Size  Used by
ipt_REJECT             12288  0
nf_reject_ipv4         12288  1 ipt_REJECT
```

* [ ] `nf_reject_ipv4` was loaded once, by the user `ipt_REJECT`
* [x] One module, `ipt_REJECT`, depends on `nf_reject_ipv4`, so it cannot be unloaded first
* [ ] `nf_reject_ipv4` is built into the kernel image of `ipt_REJECT`
* [ ] `ipt_REJECT` is waiting for `nf_reject_ipv4` to finish loading

> **Explanation:** The number is the use count and the list names dependent modules. `modprobe -r nf_reject_ipv4` would fail while `ipt_REJECT` uses it; `lsmod` just formats `/proc/modules`.

#### Q. `sudo insmod ./btrfs.ko` fails with "Unknown symbol in module", while `sudo modprobe btrfs` works. Why?

* [ ] `insmod` cannot load compressed modules
* [ ] `insmod` works only for modules outside `/lib/modules`
* [ ] `modprobe` ignores signature checks that `insmod` enforces
* [x] `insmod` loads only the named file; `modprobe` loads its dependencies first

> **Explanation:** `modprobe` uses `modules.dep` under `/lib/modules/$(uname -r)` to load modules such as `raid6_pq` and `xor` before `btrfs`; `modprobe --show-depends btrfs` lists them. `insmod` does no dependency handling.

#### Q. `/etc/modprobe.d/blacklist-nouveau.conf` contains `blacklist nouveau`. What happens when an admin runs `sudo modprobe nouveau`?

* [ ] modprobe refuses with "module is blacklisted"
* [ ] modprobe loads it only after the next reboot
* [x] The module loads, because `blacklist` only stops loading by alias
* [ ] modprobe removes the blacklist line and loads the module

> **Explanation:** `blacklist` makes modprobe ignore the module's aliases, so hardware detection no longer pulls it in, but loading it by name still works. To block that too, add `install nouveau /bin/false`.

#### Q. You put `net.ipv4.ip_forward = 1` in `/etc/sysctl.d/90-router.conf`. Which command applies it now without a reboot?

* [x] `sudo sysctl --system`
* [ ] `sudo sysctl -p`
* [ ] `sudo systemctl daemon-reload`
* [ ] `sudo sysctl -a`

> **Explanation:** `--system` loads every file in the sysctl configuration directories, including `/etc/sysctl.d/`. Plain `sysctl -p` reads only `/etc/sysctl.conf` unless you name a file. `sysctl -w` changes a value only until reboot.

#### Q. Which command shows the same value as `sysctl vm.swappiness`?

* [ ] `cat /sys/kernel/vm/swappiness`
* [x] `cat /proc/sys/vm/swappiness`
* [ ] `cat /proc/vm/swappiness`
* [ ] `cat /etc/sysctl.d/vm.swappiness`

> **Explanation:** sysctl names are paths under `/proc/sys/` with dots in place of slashes. Writing to the file (as root) has the same effect as `sysctl -w`, and both are lost at reboot.

#### Q. Where can you read the current parameter values of the loaded `kvm` module?

* [ ] `/proc/sys/kvm/`
* [ ] `/lib/modules/$(uname -r)/kvm/`
* [x] `/sys/module/kvm/parameters/`
* [ ] `/etc/modprobe.d/kvm.conf`

> **Explanation:** sysfs (`/sys`) exposes the kernel's device, driver and module model, with one file per module parameter. `/etc/modprobe.d/` holds options for future loads, and `/lib/modules` holds the module files.

#### Q. In `make menuconfig`, what does `<M>` next to a driver mean, compared with `[*]`?

* [ ] `<M>` means mandatory; `[*]` means optional
* [x] `<M>` builds it as a loadable module; `[*]` builds it into the kernel image
* [ ] `<M>` marks a modified option; `[*]` marks the default
* [ ] `<M>` enables it for multiprocessor systems only

> **Explanation:** Built-in code is always present from boot. A module is a separate `.ko` file installed under `/lib/modules/<version>` and loaded on demand. `[ ]` leaves the feature out.

#### Q. A web server fails with "Too many open files" at about 1024 open sockets, although `fs.file-max` is very large. Which limit is it most likely hitting?

* [ ] The listen backlog of the socket, `net.core.somaxconn`
* [ ] The per-user inotify limit, `fs.inotify.max_user_watches`
* [x] The per-process open-file limit, `ulimit -n` or `LimitNOFILE=` in its unit
* [ ] The system-wide process limit, `kernel.pid_max`

> **Explanation:** `fs.file-max` caps file handles for the whole system. Each process also has its own `RLIMIT_NOFILE`, often a soft limit of 1024; for a systemd service raise it with `LimitNOFILE=`.

#### Q. A program calls `read()` on a file. Which statement describes what happens?

* [ ] The C library reads the disk blocks itself and returns them to the program
* [ ] The kernel copies the program into kernel space and runs the read there
* [ ] The disk driver is mapped into the program and runs in user space
* [x] The CPU switches to kernel mode, the kernel does the I/O, and data is copied into the program's buffer

> **Explanation:** User-space code cannot touch hardware or kernel memory. A system call enters the kernel, whose filesystem and driver code performs the request and returns the result to the process.
