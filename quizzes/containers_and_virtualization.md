# Containers and Virtual Machines Quiz

Notes: [Containers and Docker](../notes/containers_and_docker.md), [Virtual Machines](../notes/virtual_machines.md)

Check your understanding of container isolation, Docker images, Dockerfiles, volumes, networking and `docker run`, and of hypervisors, KVM, QEMU and libvirt.

#### Q. On a Linux host running Docker Engine with kernel `6.17.0-20-generic`, what does this command print?

```bash
docker run --rm ubuntu:24.04 uname -r
```

* [ ] The default kernel version of Ubuntu 24.04, which ships inside the image
* [ ] An error, because a container has no kernel of its own to report
* [x] `6.17.0-20-generic`, the host's kernel version
* [ ] The kernel version of a small VM that Docker Engine starts for containers

> **Explanation:** A container is a group of host processes; the image supplies only userspace files, never a kernel. Every container sees the host kernel. (Docker Desktop on macOS or Windows differs: there the containers share the kernel of a Linux VM.)

#### Q. Which kernel mechanism enforces the limits set by `docker run --memory 64m --cpus 1.5`?

* [x] Control groups (cgroups)
* [ ] Namespaces
* [ ] Seccomp filters
* [ ] Linux capabilities

> **Explanation:** cgroups limit and account for resources. Inside such a container on cgroup v2, `/sys/fs/cgroup/memory.max` reads `67108864` and `cpu.max` reads `150000 100000`. Namespaces control what a process can see, not how much it may use.

#### Q. What does the `PID` column show for the `ps` process in the output of this command?

```bash
docker run --rm alpine ps
```

* [x] `1`, because `ps` is the first process in a new PID namespace
* [ ] The same PID that the host's `ps` would show for it
* [ ] `0`, because PID 0 is reserved for the container's init
* [ ] Nothing, because `ps` cannot read `/proc` inside a container

> **Explanation:** Docker starts each container in a new PID namespace, so its first process is PID 1 there and sees no host processes. On the host, the same process has an ordinary, different PID.

#### Q. Which namespace lets a container have its own hostname, separate from the host's?

* [x] `uts`
* [ ] `ipc`
* [ ] `mnt`
* [ ] `user`

> **Explanation:** The UTS namespace isolates the hostname and NIS domain name. Docker sets it to the short container ID by default (`docker run --rm alpine hostname` prints something like `87891a48e4d9`), or to the value of `--hostname`.

#### Q. You must test a kernel module against a kernel version different from the one your server runs. Which environment fits?

* [ ] A Docker container built from an image of the target distribution
* [x] A virtual machine that boots the target kernel
* [ ] A Podman container in rootless mode
* [ ] A container started with `--network none` for isolation

> **Explanation:** Containers always run on the host kernel, so no image or flag can give them another kernel, and loading a module from one affects the host. A VM boots its own guest kernel, so you can choose any version.

#### Q. Why is a virtual machine usually considered a stronger security boundary than a container?

* [ ] Containers cannot use cgroups, so one container can exhaust host memory
* [ ] VM disk images are encrypted, but container images are stored in plain text
* [ ] Containers always run as root, but VM processes never do
* [x] Each VM has its own kernel, while all containers share the host kernel

> **Explanation:** A kernel bug reachable from inside a container can compromise the whole host, because every container calls into the same kernel. A VM attacker must also escape the hypervisor. This is why many platforms run containers inside VMs.

#### Q. What is the relationship between a Docker image and a container?

* [x] An image is a read-only stack of layers; a container adds a writable layer and runtime state
* [ ] An image is a running container that has been paused and saved
* [ ] A container is a compressed copy of an image that is unpacked when it starts
* [ ] An image holds the kernel, while a container holds the application files

> **Explanation:** Many containers can run from one image at once. Each gets its own thin writable layer on top of the shared read-only image layers, plus its own processes, namespaces and network settings.

#### Q. You run the commands below. What does the second command print?

```bash
docker run --name w alpine sh -c 'echo data > /keep.txt'
docker run --rm alpine cat /keep.txt
```

* [ ] `data`
* [ ] An empty line
* [x] `cat: can't open '/keep.txt': No such file or directory`
* [ ] An error saying the name `w` is already in use

> **Explanation:** The file was written to the writable layer of container `w` only. A new container starts from the unchanged image. The data is still in `w` (`docker cp w:/keep.txt -` or `docker start w` would find it) until `w` is removed.

#### Q. In `docker diff` output, what do the letters `A`, `C` and `D` mean?

* [ ] Archived, Cached and Detached files in the image
* [x] Added, Changed and Deleted paths in the container's writable layer
* [ ] Paths from the Application, Config and Data volumes
* [ ] Files that are Accessible, Corrupted or Dangling

> **Explanation:** `docker diff` compares a container's filesystem with its image. After `rm /etc/motd` and creating `/keep.txt` it shows `C /etc`, `D /etc/motd` and `A /keep.txt`. Volume contents are not included.

#### Q. You build this Dockerfile. Which instructions add a filesystem layer on top of the `alpine` base layers?

```dockerfile
FROM alpine:latest
ENV MODE=prod
COPY app.txt /app/
RUN apk add --no-cache curl
EXPOSE 8080
CMD ["cat", "/app/app.txt"]
```

* [ ] All six instructions
* [ ] Only `RUN`
* [ ] `FROM`, `ENV` and `CMD`
* [x] `COPY` and `RUN`

> **Explanation:** Instructions that change files (`RUN`, `COPY`, `ADD`) create layers. `ENV`, `EXPOSE` and `CMD` only change image metadata and appear as `0B` entries in `docker history`. Here the image has one base layer plus two new ones.

#### Q. A Dockerfile has `RUN head -c 50000000 /dev/urandom > /big.bin` followed by `RUN rm /big.bin`. How big is the resulting image compared with the base?

* [x] About 50 MB larger, because the first layer still contains the file
* [ ] About the same, because the second step deletes the file
* [ ] About 100 MB larger, because the delete step copies the file again
* [ ] The build fails, because a later step cannot delete a file from an earlier one

> **Explanation:** Layers are immutable. The `rm` only adds a whiteout marker in a new layer, so the 50 MB stays in the earlier layer. To keep an image small, create and delete temporary files in the same `RUN` instruction.

#### Q. With this Dockerfile, you edit only `app.py` and rebuild. Which steps run again instead of coming from the cache?

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

* [ ] Every step, because the build context changed
* [ ] Only `RUN pip install`, because it is the slowest step
* [x] `COPY . .` and the steps after it
* [ ] No steps, because `CMD` is the only one that uses `app.py`

> **Explanation:** Docker reuses each cached step until one has different inputs; that step and all later ones are rebuilt. Copying `requirements.txt` on its own first means the dependency install is reused until the requirements file itself changes.

#### Q. Why do Dockerfile best practices say to write `RUN apt-get update && apt-get install -y curl` as one instruction rather than two?

* [ ] Two `RUN` instructions in a row are a syntax error
* [ ] `apt-get install` cannot run unless it is chained with `&&`
* [ ] A single instruction makes `apt-get` download packages in parallel
* [x] A cached `apt-get update` layer could be reused with an edited install line, giving stale package lists

> **Explanation:** If `RUN apt-get update` is its own step, its cached layer is reused for months, and a later edit to the install line runs against old package indexes. Combining them, and deleting `/var/lib/apt/lists/*` in the same step, avoids this and saves a layer.

#### Q. An image has the instructions below. What does `docker run --rm img there` print?

```dockerfile
ENTRYPOINT ["echo", "hi"]
CMD ["world"]
```

* [x] `hi there`
* [ ] `hi world`
* [ ] `hi world there`
* [ ] `there`

> **Explanation:** In exec form, `CMD` supplies default arguments to `ENTRYPOINT`. Arguments after the image name replace `CMD`, so `echo hi there` runs. With no arguments it prints `hi world`. To replace the entrypoint itself, use `--entrypoint`.

#### Q. An image uses the shell form `ENTRYPOINT echo hi` together with `CMD ["world"]`. What does `docker run --rm img there` print?

* [ ] `hi there`
* [ ] `hi world`
* [x] `hi`
* [ ] An error, because shell form and exec form cannot be mixed

> **Explanation:** A shell-form `ENTRYPOINT` runs as `/bin/sh -c 'echo hi'`, and both `CMD` and command-line arguments are ignored. Use the exec form (a JSON array) when the entrypoint should accept arguments.

#### Q. The build context contains `arch.tar.gz`. What ends up in the image after these two instructions?

```dockerfile
ADD arch.tar.gz /added/
COPY arch.tar.gz /copied/
```

* [ ] Both directories contain the unpacked files from the archive
* [ ] Both directories contain the file `arch.tar.gz`
* [ ] `/added/` contains `arch.tar.gz` and `/copied/` contains the unpacked files
* [x] `/added/` contains the unpacked files and `/copied/` contains `arch.tar.gz`

> **Explanation:** `ADD` auto-extracts local tar archives (and can fetch URLs, which it does not unpack). `COPY` copies files as they are. Prefer `COPY` unless you need `ADD`'s extra behaviour, because it is more predictable.

#### Q. What is the main benefit of the multi-stage build below?

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /src
COPY . .
RUN go build -o /server .

FROM alpine:3.18
COPY --from=builder /server /usr/local/bin/server
CMD ["server"]
```

* [x] The final image contains the binary but not the Go toolchain or the source code
* [ ] The two stages are built in parallel on two different hosts
* [ ] The final image runs the Go compiler at start-up to rebuild the binary
* [ ] The `builder` stage becomes a shared base layer of the final image

> **Explanation:** Only what `COPY --from=builder` copies reaches the last stage; the stage named `builder` is discarded. A Go toolchain image is hundreds of megabytes, while the final Alpine-based image can be under 20 MB.

#### Q. A project has a `.dockerignore` file containing `.env`, and the Dockerfile uses `COPY . /src/`. What happens to `.env`?

* [ ] It is copied but made read-only
* [x] It is not sent to the build context, so it never reaches the image
* [ ] It is copied, and only `docker push` leaves it out
* [ ] The build fails because an ignored file is matched by `COPY`

> **Explanation:** `.dockerignore` filters what the client sends to the builder. Ignored files cannot be copied by any instruction, which keeps secrets and bulky folders such as `.git` or `node_modules` out of images and speeds up builds.

#### Q. `/etc/apk` in the `alpine` image contains files. What do the two commands list?

```bash
docker volume create v
docker run --rm -v v:/etc/apk alpine ls /etc/apk
docker run --rm -v "$PWD/emptydir":/etc/apk alpine ls /etc/apk
```

* [ ] Both list nothing, because a mount hides the image's directory
* [ ] Both list the image's files, because mounts are layered under the image
* [ ] The first lists nothing; the second lists the image's files
* [x] The first lists the image's files; the second lists nothing

> **Explanation:** When an empty named volume is first mounted, Docker copies the image's contents at that path into it. A bind mount always shows the host directory as it is, hiding whatever the image had there.

#### Q. You run `docker run -v /srv/missing:/data alpine true` and `/srv/missing` does not exist on the host. What happens?

* [ ] Docker refuses to start the container because the source is missing
* [ ] Docker creates a named volume called `missing`
* [x] Docker creates `/srv/missing` on the host, owned by root, and mounts it
* [ ] The mount is skipped and `/data` is an ordinary directory in the container

> **Explanation:** The `-v` syntax creates a missing bind-mount source as a root-owned directory. The `--mount type=bind,...` syntax does not, and fails with `bind source path does not exist`, which catches typos in paths.

#### Q. A PostgreSQL container was started with `-v pgdata:/var/lib/postgresql/data`. You run `docker rm -f` on it and start a new container with the same `-v` option. What happens to the database files?

* [ ] They are lost, because removing a container deletes its volumes
* [x] They are still there, because named volumes outlive containers
* [ ] They are restored from the image's original data directory
* [ ] They survive only if the container was stopped before removal

> **Explanation:** A named volume lives under `/var/lib/docker/volumes/` until you delete it with `docker volume rm`, `docker volume prune` or `docker compose down -v`. Only the container's writable layer is deleted with the container.

#### Q. What happens when a process in a container tries to write to a mount created with `-v pgdata:/data:ro`?

* [ ] The write succeeds, but it goes to the container's writable layer
* [ ] The write succeeds, and Docker discards the change when the container stops
* [ ] The container is stopped with exit code 137
* [x] The write fails with `Read-only file system`

> **Explanation:** The `:ro` option makes that mount read-only inside the container; other paths are not affected. Use it when the container only needs to read, such as served web pages or configuration files.

#### Q. You start `docker run -d -p 8080:80 nginx`. How do you reach the web server from the host?

* [ ] `http://localhost:80`, because `-p` maps the container port onto the same host port
* [x] `http://localhost:8080`, because the format is `HOST_PORT:CONTAINER_PORT`
* [ ] `http://localhost:8080`, but only from inside another container
* [ ] Only at the container's private IP address on port 8080

> **Explanation:** `-p 8080:80` publishes container port 80 on host port 8080 on all host addresses. Add an address to restrict it, as in `-p 127.0.0.1:8080:80`. Repeat `-p` to publish several ports.

#### Q. An image's Dockerfile has `EXPOSE 8000`. You start it with `docker run -d --name web img`. What does `docker port web` print?

* [x] Nothing, because `EXPOSE` alone does not publish a port
* [ ] `8000/tcp -> 0.0.0.0:8000`
* [ ] `8000/tcp -> 0.0.0.0:32768`
* [ ] An error, because exposed ports must be published

> **Explanation:** `EXPOSE` only documents the port in the image metadata. Publish it with `-p`, or use `-P` to publish all exposed ports on random high host ports (for example `8000/tcp -> 0.0.0.0:32768`).

#### Q. A container is started with `-p 127.0.0.1:18080:8000`. Who can connect to host port 18080?

* [ ] Any machine on the network, because Docker ignores the address
* [ ] Only other containers on the default bridge
* [x] Only clients on the host itself, through the loopback address
* [ ] Nobody, because a published port must be 1024 or higher on both sides

> **Explanation:** The optional address before the host port chooses the host interface to listen on. Binding to `127.0.0.1` keeps a development database or admin panel off the network while still letting `curl http://127.0.0.1:18080/` work on the host.

#### Q. Two containers, `app` and `db`, are started on the default bridge network. Inside `app`, `ping db` fails with `bad address 'db'`. What fixes it?

* [ ] Publish a port on `db` with `-p`
* [x] Run both containers on a user-defined network created with `docker network create`
* [ ] Start `app` with `--network none`
* [ ] Add `EXPOSE` to the `db` image

> **Explanation:** Docker's embedded DNS resolves container names only on user-defined networks, not on the default `bridge`. After `docker network create appnet` and `--network appnet` on both containers, `app` can reach `db` by name.

#### Q. What does Docker do with `-p 8080:80` when the container also uses `--network host`?

* [ ] It maps port 80 to 8080 using NAT, as usual
* [ ] It fails to start the container
* [ ] It assigns a random port, as with `-P`
* [x] It discards the published port and prints a warning

> **Explanation:** With `--network host` the container uses the host's network namespace, so a service listening on port 80 is directly on host port 80. Docker prints `WARNING: Published ports are discarded when using host network mode`.

#### Q. What network interfaces does a container started with `--network none` have?

* [ ] None at all, not even loopback
* [x] Only the loopback interface `lo`
* [ ] `lo` and an `eth0` with no default route
* [ ] The same interfaces as the host

> **Explanation:** `--network none` gives the container its own network namespace with only `lo`. `ip -o link` inside it lists just `lo`. Use it for batch jobs that must not reach the network.

#### Q. What is the difference between `docker run` and `docker exec`?

* [ ] `docker run` attaches to a running container; `docker exec` creates a new one
* [ ] `docker exec` restarts a stopped container; `docker run` only works on images
* [ ] They are aliases; `exec` is kept for backward compatibility
* [x] `docker run` creates a new container from an image; `docker exec` runs an extra command in a running container

> **Explanation:** `docker exec -it web sh` opens a shell next to the main process of the running container `web`. It fails if the container is stopped. `docker run -it --rm alpine sh` starts a fresh container and removes it when the shell exits.

#### Q. A container started with `--memory 32m --memory-swap 32m` tries to allocate 200 MB. What do `docker inspect -f '{{.State.ExitCode}} {{.State.OOMKilled}}'` and the exit status show?

* [ ] `1 false`, because `malloc` returns an error
* [x] `137 true`, because the kernel OOM killer sent `SIGKILL`
* [ ] `143 true`, because Docker sent `SIGTERM`
* [ ] `0 false`, because the excess memory goes to swap

> **Explanation:** When a cgroup exceeds its memory limit, the kernel kills a process in it. Exit code 137 is 128 + 9 (`SIGKILL`), and `OOMKilled` is `true`. Setting `--memory-swap` equal to `--memory` gives the container no swap.

#### Q. `docker stop web` takes ten seconds and the container exits with code 137. The main process is a Python server running as PID 1. Why?

* [x] PID 1 in a PID namespace ignores `SIGTERM` unless it installs a handler, so Docker sends `SIGKILL` after the 10 s timeout
* [ ] Python flushes its buffers for 10 s before it exits
* [ ] `docker stop` always waits 10 s and then sends `SIGKILL`
* [ ] The container's cgroup blocks all signals until the timeout ends

> **Explanation:** The kernel does not apply default signal actions to a namespace's init process. Running with `--init` puts a small init (`tini`) at PID 1 that forwards signals; then `docker stop` returns at once and the exit code is 143 (`SIGTERM`).

#### Q. What does the last line print?

```bash
docker run --rm alpine sh -c 'exit 3'
echo $?
```

* [ ] `0`, because the container was created and removed successfully
* [ ] `1`, because any failure inside a container becomes 1
* [x] `3`, because `docker run` returns the container's exit status
* [ ] `125`, because the container command failed

> **Explanation:** `docker run` in the foreground exits with the main process's status, which makes containers usable in scripts and CI. Docker itself uses 125 when the daemon fails to run the container, 126 when the command cannot be invoked and 127 when it is not found.

#### Q. Which hypervisor is a Type 2 (hosted) hypervisor?

* [ ] VMware ESXi
* [ ] Microsoft Hyper-V
* [ ] Xen
* [x] Oracle VirtualBox

> **Explanation:** A Type 2 hypervisor is an application on a host operating system, like VirtualBox or VMware Workstation. Type 1 (bare-metal) hypervisors such as ESXi, Hyper-V and Xen run directly on the hardware, with no general-purpose OS beneath them.

#### Q. What distinguishes paravirtualization from full virtualization?

* [ ] Paravirtualization emulates every hardware device in software
* [x] The guest is modified or uses special drivers to call the hypervisor directly
* [ ] Paravirtualization can only run one guest per host
* [ ] Full virtualization requires a modified guest kernel

> **Explanation:** In full virtualization, an unmodified guest runs as if on real hardware. A paravirtualized guest knows it is virtualized and uses hypercalls or paravirtual devices, such as `virtio` network and disk drivers, which avoid slow device emulation.

#### Q. Which `/proc/cpuinfo` flags show that an x86 CPU has hardware virtualization extensions?

* [ ] `ht` or `lm`
* [ ] `aes` or `avx`
* [x] `vmx` (Intel VT-x) or `svm` (AMD-V)
* [ ] `hypervisor` or `vme`

> **Explanation:** `grep -Ew 'vmx|svm' /proc/cpuinfo` checks for VT-x or AMD-V, and `lscpu` prints a `Virtualization:` line. The `hypervisor` flag means the reverse: you are already inside a VM. `vme` is an old virtual-8086 feature.

#### Q. How do KVM and QEMU divide the work of running a VM on Linux?

* [ ] KVM is a user-space emulator; QEMU is the kernel module that runs guest code
* [ ] KVM and QEMU are two names for the same program
* [x] KVM kernel modules use the CPU's virtualization extensions via `/dev/kvm`; QEMU in user space emulates the devices and manages the VM
* [ ] QEMU runs Linux guests and KVM runs Windows guests

> **Explanation:** `lsmod` shows `kvm` plus `kvm_intel` or `kvm_amd`, which expose `/dev/kvm`. QEMU uses it to run guest code natively on the CPU and provides the virtual disks, NICs and firmware. libvirt manages QEMU/KVM VMs on top.

#### Q. What happens if you start a QEMU x86-64 VM on a host where KVM is unavailable (for example, no `/dev/kvm`)?

* [ ] QEMU refuses to run any x86 guest
* [ ] The VM runs at the same speed through paravirtualization
* [ ] QEMU switches to running the guest as a container
* [x] QEMU can fall back to TCG software emulation, which works but is much slower

> **Explanation:** `qemu-system-x86_64 -accel help` lists `tcg` and `kvm`. TCG translates guest instructions in software, which is how QEMU also emulates other architectures. With `-accel kvm` (or `-enable-kvm`) guest code runs directly on the CPU.

#### Q. `virsh list` shows no VMs, but you know a VM called `web` exists. What is the likely reason?

* [x] `virsh list` shows only running domains; `web` is shut off, so use `virsh list --all`
* [ ] `web` was deleted when it was shut down
* [ ] `virsh list` shows only VMs created in the current shell session
* [ ] The VM is listed only by `virsh dominfo --all`

> **Explanation:** By default `virsh list` prints running domains; `--all` adds inactive ones and `--inactive` shows only those. Also check the connection: `qemu:///system` and the per-user `qemu:///session` have separate sets of VMs.

#### Q. What is the difference between `virsh shutdown web` and `virsh destroy web`?

* [ ] `shutdown` deletes the VM; `destroy` only stops it
* [ ] `destroy` deletes the VM's disk images; `shutdown` keeps them
* [x] `shutdown` asks the guest OS to shut down cleanly; `destroy` stops it at once, like pulling the power cord
* [ ] They are identical, but `destroy` needs root

> **Explanation:** `virsh destroy` terminates the domain immediately without deleting its definition or storage, so it can be started again. `virsh shutdown` depends on the guest reacting (ACPI or guest agent) and may take time or fail if the guest ignores it.

#### Q. What does `virsh undefine web` do to a shut-off VM?

* [ ] Shuts the VM down and keeps it registered
* [x] Removes the VM's libvirt definition but, by default, leaves its disk images in place
* [ ] Deletes the VM's definition and all its disk images
* [ ] Resets the VM's configuration to its defaults

> **Explanation:** `undefine` removes the domain's XML configuration from libvirt. Disk images are deleted only with options such as `--remove-all-storage` or `--storage`. To create a domain from XML use `virsh define`, and to change one use `virsh edit`.

#### Q. You run `virsh setmem web 4G --config` while `web` is running. When does the change take effect?

* [ ] Immediately, without changing the stored configuration
* [ ] Immediately, and it is also saved for the next boot
* [x] At the next boot of the VM, because `--config` changes the persistent configuration
* [ ] Never, because memory can only be changed with `virsh edit`

> **Explanation:** In virsh, `--config` changes the persistent definition used at the next start, `--live` changes the running domain, and both can be given together. `setmem` cannot exceed the domain's maximum memory, which `virsh setmaxmem` changes.

#### Q. A VM uses NAT networking. It can browse the internet, but a laptop on the LAN cannot connect to the VM's web server. What is the usual fix?

* [ ] Switch the VM to host-only networking
* [ ] Switch the VM to internal networking
* [ ] Give the VM a second NAT adapter
* [x] Add a port-forwarding rule on the host, or use bridged networking

> **Explanation:** With NAT, the VM shares the host's address, and outside machines cannot start connections to it unless a port is forwarded. In bridged mode the VM gets its own LAN address. Host-only and internal networks cut off the LAN entirely.

#### Q. Inside a VM, `top` shows a high `st` value. What does it mean?

* [x] The VM's virtual CPUs were ready to run but the hypervisor was running something else
* [ ] The VM's disks are stalled waiting for storage
* [ ] The kernel is starting processes faster than they can be scheduled
* [ ] Processes in the VM are stopped with `SIGSTOP`

> **Explanation:** Steal time (`st`, `%steal` in `iostat`) is time a virtual CPU wanted to run but the hypervisor gave the physical CPU to another VM or task. High steal points to an overloaded host, not to a problem inside the guest.

#### Q. What is a key difference between Podman and Docker?

* [ ] Podman uses its own image format that Docker cannot run
* [x] Podman runs without a central daemon and supports rootless containers
* [ ] Podman can only run on Fedora and RHEL
* [ ] Podman containers run in lightweight VMs instead of namespaces

> **Explanation:** Docker's CLI talks to the `dockerd` daemon, which normally runs as root. Podman forks containers directly from the CLI and is designed for rootless use. Both use OCI images, and most `docker` commands work with `podman`.
