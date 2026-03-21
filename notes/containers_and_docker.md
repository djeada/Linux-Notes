## Containers and Docker

Containers have fundamentally changed the way software is built, shipped, and run. If you've spent time administering Linux systems—managing packages, configuring services, and troubleshooting dependency conflicts—you already understand the pain that containers were designed to solve. A container packages an application together with all of its dependencies, libraries, and configuration files into a single, portable unit that runs consistently on any Linux system.

Unlike traditional approaches where you install software directly onto a host and hope that library versions don't clash, containers provide **process-level isolation** using features built right into the Linux kernel. Technologies like **namespaces** (which isolate what a process can see) and **cgroups** (which limit what resources a process can consume) make containers lightweight and fast. There is no separate operating system to boot—containers share the host kernel and start in milliseconds.

Docker popularized containers by providing a simple CLI and a standardized image format. Today, containers are at the heart of DevOps workflows, continuous integration pipelines, and orchestration platforms like Kubernetes. Whether you're deploying a single web application or managing hundreds of microservices, understanding containers is an essential skill for any Linux administrator moving into DevOps.

### Containers vs Virtual Machines

One of the first questions people ask is: "How are containers different from virtual machines?" Both provide isolation, but they do it at very different levels.

A **virtual machine** runs an entire guest operating system on top of a hypervisor. Each VM includes its own kernel, init system, and full set of system libraries. This is powerful but heavy—VMs can take minutes to boot and consume gigabytes of RAM just for the OS overhead.

A **container**, on the other hand, shares the host's Linux kernel. It only packages the application and its userspace dependencies. This makes containers dramatically lighter—a typical container image might be 50–200 MB compared to several gigabytes for a VM image, and containers start in under a second.

```
+---------------------------------------------------+
|                  Virtual Machines                  |
+---------------------------------------------------+
|  +-------------+  +-------------+  +-------------+|
|  |    App A    |  |    App B    |  |    App C    ||
|  +-------------+  +-------------+  +-------------+|
|  |   Bins/Libs |  |   Bins/Libs |  |   Bins/Libs ||
|  +-------------+  +-------------+  +-------------+|
|  | Guest OS    |  | Guest OS    |  | Guest OS    ||
|  +-------------+  +-------------+  +-------------+|
|  +-----------------------------------------------+|
|  |              Hypervisor (KVM, Xen)            ||
|  +-----------------------------------------------+|
|  |              Host Operating System            ||
|  +-----------------------------------------------+|
|  |                  Hardware                     ||
|  +-----------------------------------------------+|
+---------------------------------------------------+

+---------------------------------------------------+
|                    Containers                      |
+---------------------------------------------------+
|  +-------------+  +-------------+  +-------------+|
|  |    App A    |  |    App B    |  |    App C    ||
|  +-------------+  +-------------+  +-------------+|
|  |   Bins/Libs |  |   Bins/Libs |  |   Bins/Libs ||
|  +-------------+  +-------------+  +-------------+|
|  +-----------------------------------------------+|
|  |         Container Runtime (Docker)            ||
|  +-----------------------------------------------+|
|  |     Host Operating System (Shared Kernel)     ||
|  +-----------------------------------------------+|
|  |                  Hardware                     ||
|  +-----------------------------------------------+|
+---------------------------------------------------+
```

Notice the key difference: containers eliminate the guest OS layer entirely. This is why you can run dozens of containers on a machine that might only support a handful of VMs.

| Feature | Virtual Machines | Containers |
| --- | --- | --- |
| Isolation level | Hardware-level (hypervisor) | OS-level (namespaces, cgroups) |
| Boot time | Minutes | Seconds or less |
| Image size | Gigabytes | Megabytes |
| Resource overhead | High (full OS per VM) | Low (shared kernel) |
| Portability | Requires compatible hypervisor | Runs on any Linux host with container runtime |
| Density | Tens per host | Hundreds per host |
| Security boundary | Strong (separate kernels) | Moderate (shared kernel) |
| Use case | Full OS environments, mixed OS | Microservices, CI/CD, app packaging |

In practice, VMs and containers are complementary. Many production environments run containers *inside* VMs to combine the strong isolation of a hypervisor with the lightweight packaging of containers.

### Docker Architecture

Docker uses a client-server architecture. The **Docker client** (`docker` CLI) sends commands to the **Docker daemon** (`dockerd`), which builds images, runs containers, and manages networks and volumes. They communicate over a Unix socket or network interface.

```
+----------------------------------------------------------+
|                      Docker Host                         |
|                                                          |
|  +-------------------+       +------------------------+  |
|  |   Docker Client   | <---> |    Docker Daemon       |  |
|  |   (docker CLI)    |  REST |    (dockerd)           |  |
|  +-------------------+  API  |                        |  |
|                              |  +-------+ +-------+   |  |
|                              |  | Image | | Image |   |  |
|                              |  +-------+ +-------+   |  |
|                              |                        |  |
|                              |  +----------+ +------+ |  |
|                              |  |Container | |Contai| |  |
|                              |  |   A      | |ner B | |  |
|                              |  +----------+ +------+ |  |
|                              +------------------------+  |
|                                       |                  |
+---------------------------------------|------------------+
                                        |
                                        v
                             +---------------------+
                             |   Docker Registry   |
                             |   (Docker Hub /     |
                             |    Private)         |
                             +---------------------+
```

The key components are:

- **Images**: Read-only templates used to create containers. Built in layers—each Dockerfile instruction creates a new layer, and layers are cached and shared.
- **Containers**: Running instances of images. A container adds a writable layer on top of the image layers.
- **Registry**: A storage and distribution system for images. Docker Hub is the default public registry.
- **Dockerfile**: A text file with instructions for building an image.

### Installing Docker

Docker is available for all major Linux distributions. The recommended approach is to use Docker's official repository rather than your distro's default repos (which are often outdated).

#### On Ubuntu / Debian

```bash
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### On CentOS / RHEL / Fedora

```bash
sudo yum remove docker docker-client docker-common docker-engine
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Post-Installation Steps

By default, Docker commands require `sudo`. To run Docker as a non-root user:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Verify the installation:

```bash
docker --version
```

```
Docker version 24.0.7, build afdd53b
```

```bash
docker run hello-world
```

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Working with Docker Images

Images are the building blocks of containers. You pull images from a registry, and each image is identified by a **repository name** and a **tag**. If you don't specify a tag, Docker defaults to `latest`.

#### Pulling Images

```bash
docker pull nginx
docker pull nginx:1.25-alpine
docker pull ghcr.io/owner/my-app:v2.1
```

```
1.25-alpine: Pulling from library/nginx
c926b61bad3b: Pull complete
eb2b50a703e2: Pull complete
Digest: sha256:a5127daff3d6...
Status: Downloaded newer image for nginx:1.25-alpine
```

#### Listing and Inspecting Images

```bash
docker images
```

```
REPOSITORY   TAG           IMAGE ID       CREATED        SIZE
nginx        latest        a6bd71f48f68   2 days ago     187MB
nginx        1.25-alpine   2bc7edbc3cf2   2 days ago     43.2MB
ubuntu       22.04         3b418d7b466a   3 weeks ago    77.8MB
```

The `alpine` variant is worth noting—Alpine-based images are dramatically smaller because they use musl libc and BusyBox instead of the full GNU toolchain.

#### Removing Images

```bash
docker rmi nginx:1.25-alpine                 # remove a specific image
docker image prune                           # remove dangling images
docker image prune -a                        # remove ALL unused images
```

### Running Containers

The `docker run` command creates and starts a container from an image.

#### Basic Container Operations

```bash
# Run a container in the foreground
docker run ubuntu:22.04 echo "Hello from a container"
```

```
Hello from a container
```

```bash
# Run in detached mode (background)
docker run -d --name my-nginx nginx
```

```
a3f8b2c9d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1
```

```bash
# List running containers
docker ps
```

```
CONTAINER ID   IMAGE   COMMAND                  CREATED         STATUS         PORTS     NAMES
a3f8b2c9d7e6   nginx   "/docker-entrypoint.…"   5 seconds ago   Up 4 seconds   80/tcp    my-nginx
```

```bash
# List all containers (including stopped)
docker ps -a

# Stop and remove a container
docker stop my-nginx
docker rm my-nginx

# Stop and remove in one step
docker rm -f my-nginx
```

#### Port Mapping

Containers have their own network namespace. To expose a service to the host, map ports with `-p`:

```bash
docker run -d --name web -p 8080:80 nginx
```

Now you can access nginx at `http://localhost:8080`. The format is `-p HOST_PORT:CONTAINER_PORT`.

```bash
docker run -d -p 8080:80 -p 8443:443 nginx          # multiple ports
docker run -d -p 127.0.0.1:8080:80 nginx             # bind to specific interface
```

#### Volume Mounting

To persist data or share files between the host and a container:

```bash
# Bind mount: map a host directory into the container
docker run -d --name web \
  -p 8080:80 \
  -v /home/user/website:/usr/share/nginx/html:ro \
  nginx
```

The `:ro` suffix makes the mount read-only inside the container—a good security practice when the container only needs to read files.

#### Running Interactive Containers

```bash
docker run -it ubuntu:22.04 /bin/bash               # interactive shell in new container
docker exec -it my-nginx /bin/sh                     # exec into a running container
docker logs my-nginx                                 # view container logs
docker logs -f my-nginx                              # follow logs (like tail -f)
```

### Building Custom Images with Dockerfiles

A **Dockerfile** is a text file containing instructions for assembling a Docker image. Each instruction creates a layer.

#### Dockerfile Syntax

| Instruction | Purpose |
| --- | --- |
| `FROM` | Sets the base image (required as the first instruction) |
| `RUN` | Executes a command during the build (installs packages, etc.) |
| `COPY` | Copies files from the build context into the image |
| `ADD` | Like `COPY` but also handles URLs and tar extraction |
| `WORKDIR` | Sets the working directory for subsequent instructions |
| `ENV` | Sets environment variables |
| `EXPOSE` | Documents which ports the container listens on |
| `CMD` | Default command to run when the container starts |
| `ENTRYPOINT` | Configures the container to run as an executable |
| `ARG` | Defines build-time variables |
| `VOLUME` | Creates a mount point for external storage |
| `USER` | Sets the user for subsequent instructions and the running container |

#### Example: Building a Python Web Application Image

```bash
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

```bash
docker build -t my-flask-app:1.0 .
```

```
[+] Building 12.3s (10/10) FINISHED
 => [1/5] FROM python:3.11-slim                              3.2s
 => [2/5] WORKDIR /app                                       0.0s
 => [3/5] COPY requirements.txt .                            0.0s
 => [4/5] RUN pip install --no-cache-dir -r requirements...  7.8s
 => [5/5] COPY . .                                           0.1s
 => exporting to image                                       1.0s
```

Notice the order: we copy `requirements.txt` and install dependencies *before* copying application code. This exploits Docker's layer caching—if dependencies don't change, Docker reuses the cached layer.

```bash
# Run the newly built image
docker run -d -p 5000:5000 --name flask-app my-flask-app:1.0
```

#### Multi-Stage Builds

Multi-stage builds let you use one image for building and a smaller image for running:

```bash
# Dockerfile for a Go application
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server .

FROM alpine:3.18
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/server /usr/local/bin/server
EXPOSE 8080
CMD ["server"]
```

The final image contains only the compiled binary and a minimal Alpine base—no Go toolchain, no source code. A Go build image might be 800 MB, but the production image could be under 20 MB.

### Docker Networking

Docker creates isolated networks for containers. Understanding the network drivers helps you control how containers communicate.

```
+---------------------------------------------------------------+
|                        Docker Host                            |
|                                                               |
|  +------------------+    +------------------+                 |
|  |   Container A    |    |   Container B    |                 |
|  |  172.17.0.2      |    |  172.17.0.3      |                 |
|  +--------+---------+    +--------+---------+                 |
|           |                       |                           |
|  +--------+-----------------------+---------+                 |
|  |              docker0 bridge              |                 |
|  |              172.17.0.1                  |                 |
|  +---------------------+-------------------+                 |
|                        | NAT (iptables)                       |
+------------------------|--------------------------------------+
                         |
                    eth0 (Host) 192.168.1.100
```

#### Network Drivers

| Driver | Description |
| --- | --- |
| `bridge` | Default. Containers on the same bridge can communicate. Isolated from host network. |
| `host` | Container shares the host's network namespace. No isolation, but no NAT overhead. |
| `none` | No networking. Container is completely isolated. |
| `overlay` | Spans multiple Docker hosts. Used in Docker Swarm and orchestration. |
| `macvlan` | Assigns a MAC address to the container, making it appear as a physical device on the network. |

#### Managing Networks

```bash
# List networks
docker network ls
```

```
NETWORK ID     NAME      DRIVER    SCOPE
a1b2c3d4e5f6   bridge    bridge    local
f6e5d4c3b2a1   host      host      local
1a2b3c4d5e6f   none      null      local
```

```bash
docker network create my-app-network

docker run -d --name db --network my-app-network postgres:16
docker run -d --name app --network my-app-network my-flask-app:1.0

# Containers on the same custom network can reach each other by name
docker exec app ping db
```

Custom bridge networks provide **automatic DNS resolution** between containers—you can reference other containers by name instead of IP address.

```bash
docker network connect my-app-network existing-container   # add network to container
docker network inspect my-app-network                      # inspect a network
docker network rm my-app-network                           # remove a network
```

### Docker Volumes and Data Persistence

Containers are **ephemeral** by design—when you remove a container, its writable layer is deleted. For data that must persist, Docker provides volumes.

```
+---------------------------------------------------+
|                  Docker Host                      |
|                                                   |
|  +-----------+   +-----------------------------+  |
|  | Container |   |  /var/lib/docker/volumes/   |  |
|  | /app/data +-->|  my-data/_data/             |  |
|  +-----------+   |  (Named volume)             |  |
|                  +-----------------------------+  |
|  +-----------+   +-----------------------------+  |
|  | Container |   |  /home/user/project/        |  |
|  | /app/code +-->|  (Bind mount)               |  |
|  +-----------+   +-----------------------------+  |
+---------------------------------------------------+
```

#### Named Volumes vs Bind Mounts

| Feature | Named Volumes | Bind Mounts |
| --- | --- | --- |
| Managed by | Docker | You (the host filesystem) |
| Location | `/var/lib/docker/volumes/` | Anywhere on the host |
| Created with | `docker volume create` or at run time | `-v /host/path:/container/path` |
| Portability | Easy to backup and migrate | Tied to host directory structure |
| Best for | Database storage, persistent app data | Development (live code reload), config files |

#### Working with Volumes

```bash
docker volume create pgdata

docker run -d --name postgres \
  -e POSTGRES_PASSWORD=mysecretpw \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

docker volume ls
```

```
DRIVER    VOLUME NAME
local     pgdata
```

```bash
docker volume inspect pgdata
```

```json
[
    {
        "Driver": "local",
        "Mountpoint": "/var/lib/docker/volumes/pgdata/_data",
        "Name": "pgdata",
        "Scope": "local"
    }
]
```

```bash
docker volume rm pgdata        # remove a specific volume
docker volume prune            # remove all unused volumes
```

### Docker Compose

Real-world applications rarely consist of a single container. A web application might need a web server, a backend, a database, and a cache. **Docker Compose** lets you define multi-container applications using a single YAML file.

#### Example: A Web Application Stack

Create a `docker-compose.yml`:

```yaml
version: "3.8"

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
    networks:
      - frontend
  app:
    build: ./app
    environment:
      - DATABASE_URL=postgresql://appuser:apppass@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    networks:
      - frontend
      - backend
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD=apppass
      - POSTGRES_DB=myapp
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - backend
  cache:
    image: redis:7-alpine
    networks:
      - backend

volumes:
  pgdata:

networks:
  frontend:
  backend:
```

#### Docker Compose Commands

```bash
docker compose up -d
```

```
[+] Running 5/5
 ✔ Network myapp_frontend  Created
 ✔ Network myapp_backend   Created
 ✔ Container myapp-cache-1 Started
 ✔ Container myapp-db-1    Started
 ✔ Container myapp-app-1   Started
 ✔ Container myapp-web-1   Started
```

```bash
docker compose ps                        # view running services
docker compose logs -f app               # follow logs for a service
docker compose down                      # stop all services
docker compose down -v                   # stop and remove volumes (destroys data)
docker compose up -d --build             # rebuild images and restart
```

### Podman as an Alternative

**Podman** is a container engine developed by Red Hat that serves as a drop-in replacement for Docker. The key difference is that Podman runs **daemonless** and supports **rootless mode**, meaning containers run without requiring root privileges.

```bash
podman pull nginx:alpine
podman run -d -p 8080:80 --name web nginx:alpine
podman ps
podman stop web && podman rm web
```

| Feature | Docker | Podman |
| --- | --- | --- |
| Architecture | Client-daemon (`dockerd`) | Daemonless (fork-exec) |
| Root required | Yes (daemon runs as root) | No (rootless by default) |
| Systemd integration | Via service file for daemon | Native with `podman generate systemd` |
| Docker Compose | Native | Via `podman-compose` or compatibility mode |
| Image format | OCI-compatible | OCI-compatible |
| Docker CLI compatible | Yes | Yes (alias `docker=podman`) |

Many organizations choose Podman for its security posture—running containers without a root daemon reduces the attack surface. On RHEL 8+, Podman is the default container tool.

```bash
# Create a systemd service from a Podman container
podman generate systemd --name web --files --new
sudo mv container-web.service /etc/systemd/system/
sudo systemctl enable --now container-web.service
```

### Container Best Practices

As you move containers into production, keep these guidelines in mind.

#### Keep Images Small

Start from minimal base images like `alpine` or `*-slim` variants. Combine `RUN` instructions to reduce layers:

```bash
# Bad: creates three layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good: single layer, cleans up in the same step
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

#### Security

- **Don't run as root** inside the container. Use the `USER` instruction:

```bash
FROM node:20-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```

- **Don't store secrets in images.** Use environment variables, Docker secrets, or mounted files instead.
- **Scan images for vulnerabilities** with tools like `trivy` or `docker scout`:

```bash
docker scout cves my-flask-app:1.0
```

- **Pin image versions.** Use `nginx:1.25-alpine` instead of `nginx:latest` so builds are reproducible.

#### Use `.dockerignore`

Just as `.gitignore` keeps files out of your repository, `.dockerignore` prevents files from being sent to the build context:

```
.git
node_modules
*.md
docker-compose*.yml
.env
```

This speeds up builds and keeps sensitive files out of images.

#### Health Checks

Define a `HEALTHCHECK` so Docker can monitor whether your application is working:

```bash
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

```bash
docker ps
```

```
CONTAINER ID   IMAGE     STATUS                   NAMES
b7c3a1d9e4f2   nginx     Up 5 min (healthy)       web
```

### Challenges

1. Install Docker on your Linux system using the official Docker repository (not your distro's default package). Verify the installation by running `docker run hello-world` and explain what happens behind the scenes when you run that command for the first time.
2. Pull three different variants of the `nginx` image (`nginx:latest`, `nginx:alpine`, and `nginx:1.25-bookworm`) and compare their sizes using `docker images`. Discuss why Alpine-based images are significantly smaller and what trade-offs might come with using them.
3. Run an `nginx` container in detached mode with port `8080` mapped to port `80`, then use `curl http://localhost:8080` to verify it is serving the default page. Practice stopping, removing, and restarting the container using `docker stop`, `docker rm`, and `docker run`.
4. Write a `Dockerfile` for a simple application (such as a static HTML site served by nginx or a Python script). Build the image, tag it with a version number, and run a container from it. Explain how Docker's layer caching works and why instruction order in a Dockerfile matters.
5. Create a custom bridge network called `app-net`. Run two containers on this network—one running `nginx` and one running `alpine`—and demonstrate that the `alpine` container can reach the `nginx` container by its container name using `ping` or `wget`. Explain the DNS resolution behavior of custom networks.
6. Create a named Docker volume, attach it to a PostgreSQL container, insert some data, then remove and recreate the container using the same volume. Verify that your data persists across container removal. Discuss the difference between named volumes and bind mounts.
7. Write a `docker-compose.yml` file that defines at least three services (for example, a web server, an application backend, and a database). Start the stack with `docker compose up -d`, verify all services are running, and demonstrate that the services can communicate with each other by service name.
8. Build a multi-stage `Dockerfile` for a compiled application (use any language you are comfortable with, or find a sample Go or C program). Compare the final image size to a single-stage build that includes the full compiler toolchain. Explain why multi-stage builds are important for production images.
9. Install Podman on your system and run the same container image you used with Docker. Compare the Podman and Docker CLI commands and test running a container in rootless mode. Discuss the security benefits of a daemonless, rootless container engine.
10. Audit one of your container images for security best practices: ensure it runs as a non-root user, has no unnecessary packages, pins its base image to a specific version, and includes a `HEALTHCHECK` instruction. Use `docker scout` or `trivy` to scan for known vulnerabilities and fix or document any findings.
