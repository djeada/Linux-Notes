## CI/CD Pipelines

CI/CD stands for Continuous Integration and Continuous Delivery (or Continuous Deployment). It is a set of practices that automate the process of integrating code changes, running tests, and delivering software to production environments. For Linux administrators moving into DevOps, CI/CD pipelines are a natural extension of the automation skills you already use daily—writing shell scripts, managing services with `systemd`, and configuring servers over SSH.

At its core, a CI/CD pipeline is a series of automated steps that take code from a developer's machine all the way to a running production system. Every time someone pushes a commit, the pipeline kicks in: it builds the application, runs tests, and—if everything passes—deploys the result. This removes the error-prone manual process of building and deploying software, and it gives teams the confidence to ship changes frequently.

The DevOps philosophy bridges the gap between development and operations. As a Linux admin, you already handle the "ops" side—managing servers, monitoring logs, and maintaining uptime. CI/CD pipelines give you the tools to automate the handoff between developers writing code and administrators deploying it.

```
+----------------------------------------------------------------------+
|                        CI/CD Pipeline Overview                       |
|                                                                      |
|   Developer        Pipeline Stages            Production             |
|                                                                      |
|   +--------+    +---------+---------+------+---------+  +---------+  |
|   |  Code  | -> | Source  | Build   | Test | Deploy  |->| Running |  |
|   | Change |    | Control | & Pack  |      |         |  | System  |  |
|   +--------+    +---------+---------+------+---------+  +---------+  |
|                                                                      |
|   git push       git repo   compile   unit    ssh/     systemctl     |
|                  webhook    package  integr.  rsync    restart svc   |
|                                                                      |
+----------------------------------------------------------------------+
```

### CI/CD Pipeline Stages

A typical pipeline flows through several stages, each building on the previous one. If any stage fails, the pipeline stops and notifies the team. This fast feedback loop is one of the greatest benefits of CI/CD.

```
+----------+     +----------+     +----------+     +-----------+     +----------+
|          |     |          |     |          |     |           |     |          |
|  Source  | --> |  Build   | --> |   Test   | --> |  Staging  | --> |  Deploy  |
|          |     |          |     |          |     |           |     |          |
+----------+     +----------+     +----------+     +-----------+     +----------+
  |                |                |                |                  |
  | Trigger:       | Compile        | Run unit       | Deploy to       | Push to
  | git push,      | code,          | tests,         | staging env,    | production
  | pull request,  | resolve        | integration    | run smoke       | server(s)
  | schedule       | dependencies   | tests, lint    | tests           |
```

| Stage | Purpose | Typical Tools |
| --- | --- | --- |
| **Source** | Detect code changes and trigger the pipeline. | Git, GitHub, GitLab, Bitbucket |
| **Build** | Compile source code, resolve dependencies, create artifacts. | `make`, `gcc`, `mvn`, `npm`, `docker build` |
| **Test** | Run automated tests to catch bugs before deployment. | `pytest`, `jest`, `go test`, `selenium` |
| **Staging** | Deploy to a pre-production environment for validation. | Ansible, Terraform, Docker Compose |
| **Deploy** | Release the artifact to production systems. | `ssh`, `rsync`, `kubectl`, Ansible |

### Continuous Integration

Continuous Integration (CI) is the practice of merging all developer working copies into a shared mainline frequently—ideally several times a day. Each merge triggers an automated build and test cycle, so problems are detected early rather than discovered days or weeks later during a manual integration phase.

The key principles of CI include:

- Developers commit code to a shared repository frequently.
- Every commit triggers an automated build.
- Automated tests run against each build.
- Failures are reported immediately so the team can fix them.
- The mainline branch stays in a deployable state at all times.

A minimal CI workflow might look like this on a Linux build server:

```bash
#!/bin/bash
# Simple CI script triggered by a webhook

set -e

REPO_DIR="/opt/builds/myapp"
cd "$REPO_DIR"

git pull origin main

echo "Installing dependencies..."
npm install

echo "Running linter..."
npm run lint

echo "Running tests..."
npm test

echo "Build succeeded at $(date)"
```

The `set -e` flag ensures the script exits on the first error—mimicking how a CI pipeline halts when a stage fails.

### Continuous Delivery vs Continuous Deployment

These two terms are often confused, but they differ in one important way: the presence of a manual approval gate before production.

```
+---------------------+         +---------------------+
|  Continuous         |         |  Continuous          |
|  Delivery           |         |  Deployment          |
|                     |         |                      |
|  Code -> Build ->   |         |  Code -> Build ->    |
|  Test -> Staging -> |         |  Test -> Staging ->  |
|  [Manual Approval]  |         |  Production          |
|  -> Production      |         |  (automatic)         |
+---------------------+         +---------------------+
```

| Aspect | Continuous Delivery | Continuous Deployment |
| --- | --- | --- |
| **Definition** | Every change is built, tested, and ready to deploy. | Every change that passes tests is automatically deployed. |
| **Manual Gate** | Yes—a human approves the final release to production. | No—deployment is fully automated. |
| **Risk Level** | Lower—humans review before release. | Higher—requires extremely robust test suites. |
| **Speed** | Slower due to approval wait times. | Fastest possible path to production. |
| **Best For** | Regulated industries, teams building confidence in automation. | Mature teams with comprehensive automated testing. |
| **Rollback** | Can decide not to deploy a specific version. | Must rely on automated rollback mechanisms. |

Most teams start with Continuous Delivery and graduate to Continuous Deployment once their test coverage and monitoring are mature enough to trust full automation.

### Jenkins

Jenkins is one of the oldest and most widely used CI/CD tools. It runs as a Java application on Linux and is managed as a system service—something you already know how to handle from working with `systemd` (see [services.md](./services.md)).

#### Installing Jenkins on Linux

On Debian/Ubuntu systems:

```bash
# Add the Jenkins repository key and source
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins

# Jenkins runs as a systemd service
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

On RHEL/CentOS systems:

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

sudo yum install -y jenkins

sudo systemctl enable jenkins
sudo systemctl start jenkins
```

After installation, Jenkins is accessible at `http://your-server:8080`. Retrieve the initial admin password with:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

#### Jenkinsfile Basics

A `Jenkinsfile` defines your pipeline as code and lives in the root of your repository. Jenkins supports two syntax styles: Declarative and Scripted. Declarative is more structured and recommended for most use cases.

```groovy
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any

    environment {
        APP_NAME = 'myapp'
        DEPLOY_SERVER = 'prod.example.com'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/org/myapp.git'
            }
        }

        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'reports/**/*.xml'
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    rsync -avz --delete dist/ deploy@${DEPLOY_SERVER}:/var/www/${APP_NAME}/
                    ssh deploy@${DEPLOY_SERVER} 'sudo systemctl restart ${APP_NAME}'
                """
            }
        }
    }

    post {
        failure {
            mail to: 'team@example.com',
                 subject: "Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Check the build at ${env.BUILD_URL}"
        }
    }
}
```

Notice how the Deploy stage uses `rsync` over SSH and restarts a `systemd` service on the remote host—skills directly from your Linux admin toolkit.

### GitLab CI/CD

GitLab CI/CD is configured through a `.gitlab-ci.yml` file at the root of your repository. GitLab runners—agents installed on Linux machines—execute the pipeline jobs. If you have managed background services on Linux, setting up a runner will feel familiar.

#### .gitlab-ci.yml Example

```yaml
stages:
  - build
  - test
  - deploy

variables:
  APP_NAME: "myapp"
  DEPLOY_PATH: "/var/www/myapp"

build_job:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

unit_tests:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'
  artifacts:
    reports:
      junit: reports/junit.xml

lint_check:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm run lint

deploy_production:
  stage: deploy
  only:
    - main
  before_script:
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | ssh-add -
    - mkdir -p ~/.ssh
    - echo "$KNOWN_HOSTS" >> ~/.ssh/known_hosts
  script:
    - rsync -avz --delete dist/ deploy@prod.example.com:$DEPLOY_PATH/
    - ssh deploy@prod.example.com "sudo systemctl restart $APP_NAME"
  environment:
    name: production
    url: https://example.com
```

Key concepts in GitLab CI/CD:

- **Stages** define the order in which groups of jobs run.
- **Jobs** are the individual tasks within a stage; jobs in the same stage run in parallel.
- **Artifacts** are files produced by a job and passed to later stages.
- **Runners** are the Linux machines (or containers) that execute jobs.

### GitHub Actions

GitHub Actions uses workflow files stored in `.github/workflows/` within your repository. Each workflow is a YAML file that defines triggers, jobs, and steps.

#### Workflow Example

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  APP_NAME: myapp
  NODE_VERSION: '20'

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Build application
        run: npm run build

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  deploy:
    needs: build-and-test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Deploy to production
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
        run: |
          mkdir -p ~/.ssh
          echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan "$DEPLOY_HOST" >> ~/.ssh/known_hosts
          rsync -avz --delete dist/ deploy@"$DEPLOY_HOST":/var/www/myapp/
          ssh deploy@"$DEPLOY_HOST" 'sudo systemctl restart myapp'
```

Key concepts in GitHub Actions:

- **Triggers** (`on`) define what events start the workflow—pushes, pull requests, schedules, or manual dispatches.
- **Jobs** run on virtual machines called runners; `ubuntu-latest` gives you a full Linux environment.
- **Steps** are individual commands or reusable actions from the GitHub marketplace.
- **Secrets** are encrypted environment variables configured in repository settings, never exposed in logs.
- **Needs** enforces job ordering—the deploy job waits for build-and-test to succeed.

### Common Pipeline Patterns

#### Build Artifacts

Most pipelines produce an artifact in the build stage—a compiled binary, a Docker image, or a bundled archive—that later stages consume. This ensures every stage tests and deploys the same artifact rather than rebuilding from source.

```bash
# Example: building and archiving an artifact
npm run build
tar -czf myapp-$(git rev-parse --short HEAD).tar.gz -C dist .
```

#### Testing Stages

A well-structured pipeline runs tests in layers, from fastest to slowest:

```
+-------------+     +-------------------+     +------------------+
|   Linting   | --> | Unit Tests        | --> | Integration      |
| (seconds)   |     | (seconds/minutes) |     | Tests (minutes)  |
+-------------+     +-------------------+     +------------------+
                                                      |
                                              +------------------+
                                              | End-to-End Tests |
                                              | (minutes/hours)  |
                                              +------------------+
```

Running fast checks first means developers get quick feedback. If linting fails, there is no point running the full integration suite.

#### Deployment Strategies

When deploying to production, several strategies help minimize downtime and risk:

```
+---------------------------------------------------------------+
|                   Deployment Strategies                        |
|                                                               |
|  Blue-Green                                                   |
|  +----------+    +----------+                                 |
|  |  Blue    |    |  Green   |  Traffic switches entirely      |
|  | (active) | -> | (new ver)|  from Blue to Green once        |
|  +----------+    +----------+  Green is verified.             |
|                                                               |
|  Rolling Update                                               |
|  +----+ +----+ +----+ +----+                                  |
|  | v1 | | v2 | | v2 | | v2 |  Instances are updated one      |
|  +----+ +----+ +----+ +----+  at a time until all run v2.    |
|                                                               |
|  Canary                                                       |
|  +----+ +----+ +----+ +----+                                  |
|  | v1 | | v1 | | v1 | | v2 |  A small percentage of traffic  |
|  +----+ +----+ +----+ +----+  goes to v2; expand if healthy. |
|                                                               |
+---------------------------------------------------------------+
```

| Strategy | Downtime | Rollback Speed | Resource Cost |
| --- | --- | --- | --- |
| **Blue-Green** | Zero (instant switch) | Instant (switch back) | High (double infrastructure) |
| **Rolling** | Zero (gradual) | Moderate (roll back instances) | Low (reuses existing infra) |
| **Canary** | Zero (partial traffic) | Fast (redirect traffic) | Low to moderate |
| **Recreate** | Brief (stop old, start new) | Slow (full redeploy) | Low |

### Pipeline Security

A CI/CD pipeline has access to your production servers, credentials, and deployment keys. Treating pipeline security casually is one of the most dangerous mistakes a team can make.

#### Secrets Management

Never hardcode secrets in pipeline configuration files. Every major CI/CD platform provides a secrets store:

| Platform | Secrets Mechanism | How to Reference |
| --- | --- | --- |
| **Jenkins** | Credentials store | `credentials('my-secret-id')` |
| **GitLab** | CI/CD Variables (masked, protected) | `$MY_SECRET` in `.gitlab-ci.yml` |
| **GitHub Actions** | Repository/Environment secrets | `${{ secrets.MY_SECRET }}` |

#### Environment Variables in Pipelines

CI/CD pipelines rely heavily on environment variables (see [environment_variable.md](./environment_variable.md)) for configuration. Best practices include:

- Use the platform's secret store for sensitive values like API keys, SSH keys, and database passwords.
- Define non-sensitive configuration as plain environment variables in the pipeline file.
- Scope variables to specific environments (staging vs. production) when the platform supports it.
- Audit which jobs and stages have access to which secrets.

```yaml
# GitHub Actions: scoping secrets to an environment
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy
        env:
          DB_HOST: ${{ secrets.PROD_DB_HOST }}
          DB_PASS: ${{ secrets.PROD_DB_PASS }}
        run: ./deploy.sh
```

#### Secure Deployment Practices

- Run pipeline agents with the minimum permissions required.
- Use short-lived credentials or tokens instead of long-lived SSH keys where possible.
- Pin action versions (e.g., `actions/checkout@v4`) rather than using `@latest` to prevent supply chain attacks.
- Enable branch protection rules so only reviewed code reaches the deployment pipeline.
- Sign commits and verify signatures in the pipeline to ensure code authenticity.

### Integrating with Linux Systems

As a Linux administrator, the final stages of a CI/CD pipeline often land squarely in your domain. This is where your existing skills—SSH, `systemd`, file permissions, and log management—become essential.

#### SSH Deployment

Deploying over SSH (see [ssh_and_scp.md](./ssh_and_scp.md)) is one of the most common patterns for pushing artifacts to Linux servers:

```bash
#!/bin/bash
# deploy.sh - called by the CI/CD pipeline

set -euo pipefail

DEPLOY_HOST="prod.example.com"
DEPLOY_USER="deploy"
DEPLOY_PATH="/var/www/myapp"
ARTIFACT="dist/"

# Sync the build artifact to the server
rsync -avz --delete "$ARTIFACT" "${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/"

# Restart the application service
ssh "${DEPLOY_USER}@${DEPLOY_HOST}" << 'EOF'
    sudo systemctl restart myapp
    sleep 2
    sudo systemctl is-active --quiet myapp && echo "Service is running" || echo "Service failed to start"
EOF
```

#### Systemd Service Restarts

When your pipeline deploys a new version, it typically needs to restart the application service. A well-designed service unit file (see [services.md](./services.md)) makes this reliable:

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/myapp
ExecStart=/usr/bin/node /var/www/myapp/server.js
Restart=on-failure
RestartSec=5
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

The `Restart=on-failure` directive ensures the service recovers automatically if it crashes after a deployment. The pipeline can verify the restart succeeded:

```bash
ssh deploy@prod.example.com '
    sudo systemctl daemon-reload
    sudo systemctl restart myapp
    sleep 3
    if sudo systemctl is-active --quiet myapp; then
        echo "Deployment successful"
        exit 0
    else
        echo "Deployment failed - rolling back"
        sudo cp -r /var/www/myapp.backup/* /var/www/myapp/
        sudo systemctl restart myapp
        exit 1
    fi
'
```

#### Log Monitoring

After a deployment, checking logs confirms the new version is running correctly. Your pipeline can include a post-deploy verification step:

```bash
# Check application logs after deployment
ssh deploy@prod.example.com '
    sudo journalctl -u myapp --since "2 minutes ago" --no-pager | tail -20
'
```

Using `journalctl` to inspect service logs is a direct application of your Linux administration knowledge. Combining this with monitoring tools like Prometheus or Grafana gives you full visibility into whether a deployment is healthy.

### Challenges

1. Write a simple shell script that simulates a CI pipeline: it should pull the latest code from a Git repository, install dependencies, run a linter, execute tests, and print a success or failure message. Use `set -e` to halt on the first error, and run it manually to verify its behavior.
2. Install Jenkins on a Linux virtual machine using either `apt` or `yum`. Verify it is running with `systemctl status jenkins`, access the web interface, complete the initial setup wizard, and create a freestyle project that executes a basic shell command like `echo "Hello from Jenkins"`.
3. Write a `Jenkinsfile` with Declarative Pipeline syntax that has at least three stages (Build, Test, Deploy). The Deploy stage should only run when the branch is `main`. Test it by creating a pipeline job in Jenkins and pointing it at a Git repository containing your `Jenkinsfile`.
4. Create a `.gitlab-ci.yml` file that defines three stages and uses artifacts to pass a build output from the build stage to the deploy stage. Include a job that runs only on the `main` branch. If you do not have a GitLab instance, use GitLab's free tier or explain each directive in comments.
5. Write a GitHub Actions workflow file that triggers on pushes to `main` and pull requests. It should have two jobs: one for building and testing, and a second for deploying that depends on the first job succeeding. Use repository secrets for any sensitive values and explain how you would configure them in the GitHub UI.
6. Compare Blue-Green, Rolling, and Canary deployment strategies. For each, describe a real-world scenario where it would be the best choice, and explain what Linux infrastructure (load balancers, multiple servers, containers) you would need to implement it.
7. Set up a deployment pipeline that uses `rsync` over SSH to copy build artifacts to a remote Linux server and then restarts a `systemd` service. Verify the deployment by checking `systemctl is-active` on the target host. Document the SSH key setup required for passwordless authentication from the CI server.
8. Create a `systemd` service unit file for a sample application (a simple Node.js or Python HTTP server). Configure it with `Restart=on-failure` and appropriate environment variables. Then write a pipeline script that deploys a new version and includes a rollback mechanism if the service fails to start after the update.
9. Audit the security of a CI/CD pipeline configuration you have written or found online. Identify at least three potential security issues (such as hardcoded secrets, unpinned action versions, or overly broad permissions) and describe how you would fix each one.
10. Design a complete CI/CD pipeline on paper (or in a YAML file) for a team of five developers working on a web application. Include stages for linting, unit testing, integration testing, building a Docker image, pushing it to a container registry, deploying to a staging environment, and promoting to production with a manual approval gate. Explain the Linux infrastructure needed to support each stage.
