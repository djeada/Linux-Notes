## Cron

Cron is a powerful utility in Unix-like operating systems that automates the execution of scripts or commands at specified times, dates, or intervals. It is used for tasks such as system maintenance, backups, updates, and more.

### How Cron Works

Cron operates through a background process called the **cron daemon** (`crond`), which continuously runs and checks for scheduled tasks in crontab files. When the current time matches a scheduled time in the crontab, the cron daemon executes the associated command or script.

```
+------------------------------------------------------------------+
|                       Cron Workflow Overview                     |
+------------------------------------------------------------------+
         │
         ▼
+--------------------------------------+       +----------------------------------+
|       User/System Schedules          |       |         Crontab Files            |
|       Tasks/Commands                 |       |  (Contains timing & task details)|
| (Via command line or configuration)  |       |                                  |
+--------------------------------------+       +----------------------------------+
         │                                                      │
         │       (Updates/reads scheduled tasks)                │
         --------------------------------------------------------
                                       |
                                       ▼
                         +-------------------------------+
                         |         Cron Daemon (crond)   |
                         |       (Executes every minute) |
                         +-------------------------------+
                                       │
                                       │ Monitors timing schedules and
                                       │ triggers corresponding tasks
                                       ▼
                         +---------------------------------+
                         |      Executes Scheduled Tasks   |
                         | (Runs user/system-defined jobs) |
                         +---------------------------------+
```

- Task scheduling occurs when users or the system **define** specific tasks and their execution times within crontab files.
- The **cron** daemon is responsible for waking up every minute to review the crontab files and check for any tasks that need to be executed.
- Task **execution** happens when the current time matches a scheduled task, prompting cron to run the corresponding command or script.
- Crontab files allow for **precise** scheduling, enabling users to automate repetitive tasks based on minute, hour, day, month, or weekday configurations.
- The **cron** daemon operates continuously in the background, ensuring tasks are run at their defined intervals without manual intervention.
- If a match is found between the system time and a scheduled task, the **cron** daemon triggers the execution of the predefined script or command.

### Types of Crontab Files

Cron uses two main types of crontab files to schedule tasks:

#### System Crontabs

- **Located** at `/etc/crontab`
- Managed by the system administrator (`root` user) for system-wide tasks.
- Schedule routine maintenance tasks, system updates, and other automated processes.

For example, to schedule the `apt update` command to run as the root user every hour on the hour, use the cron job entry:

```
# m h dom mon dow user  command
0 * * * *   root  /usr/bin/apt update
```

#### User Crontabs

- The location of crontab files is typically stored in `/var/spool/cron/crontabs/`, although this location can *vary* depending on the system configuration.
- The *purpose* of these files is to provide each user with an individual crontab file, enabling them to schedule personal tasks independently.
- Crontabs allow users to *automate* tasks without requiring administrative permissions, making it easier for them to manage recurring processes.
- To *edit* a crontab, users can use the command `crontab -e`, which opens the crontab file for modification.
- Users can *list* their scheduled tasks by executing `crontab -l`, which displays the current contents of their crontab file.
- If necessary, users can *remove* their crontab with the command `crontab -r`, deleting all scheduled tasks at once.
- Crontab files serve as a way for users to *define* automated actions, whether for personal maintenance tasks or regular system checks.

### Understanding Crontab Syntax

A crontab file consists of lines with six fields: five time fields and a command field.

#### Crontab Field Structure

```
┌───────────── Minute (0 - 59)
│ ┌───────────── Hour (0 - 23)
│ │ ┌───────────── Day of Month (1 - 31)
│ │ │ ┌───────────── Month (1 - 12 or Jan-Dec)
│ │ │ │ ┌───────────── Day of Week (0 - 7 or Sun-Sat)
│ │ │ │ │
* * * * * command_to_execute
```

#### Field Descriptions

| Field           | Values                                          |
|-----------------|-------------------------------------------------|
| **Minute**      | `0` to `59`                                     |
| **Hour**        | `0` to `23`                                     |
| **Day of Month**| `1` to `31`                                     |
| **Month**       | `1` to `12` or abbreviated month names (`Jan`, `Feb`, etc.) |
| **Day of Week** | `0` to `7` (both `0` and `7` are Sunday) or abbreviated day names (`Sun`, `Mon`, etc.) | 

#### Special Characters

| Symbol        | Description                                |
|---------------|--------------------------------------------|
| **Asterisk (`*`)** | Represents all possible values for a field. |
| **Comma (`,`)**    | Separates multiple values.                  |
| **Hyphen (`-`)**   | Defines a range.                           |
| **Slash (`/`)**    | Specifies step values.                     |

#### Examples

I. Run a command every day at 2:00 AM:

```
0 2 * * * /path/to/command
```

II. Run a script at 1:00 PM on Tuesdays, Wednesdays, and Thursdays:

```
0 13 * * 2-4 /path/to/script.sh
```

III. Execute a backup at 7:30 AM from Monday to Friday:

```
30 7 * * 1-5 /path/to/backup.sh
```

IV. Run a task at 10:15 PM on the 1st of every month:

```
15 22 1 * * /path/to/monthly_task.sh
```

V. Execute a script at midnight on January 1st every year:

```
0 0 1 1 * /path/to/new_year_script.sh
```

VI. Run a command every 5 minutes:

```
*/5 * * * * /path/to/command
```

#### Visualizing Time Fields

Here's an ASCII table to help visualize how the time fields correspond to scheduling:

```
+-----------+-----------+--------------+--------------+-----------------+
|  Field    |   Value   |    Allowed   |     Step     |      Notes      |
+-----------+-----------+--------------+--------------+-----------------+
| Minute    |     M     |     0-59     |     /n       | * for every min |
| Hour      |     H     |     0-23     |     /n       | * for every hr  |
| Day of    |    DOM    |     1-31     |     /n       | * for every day |
| Month     |     M     |     1-12     |     /n       | * for every mo  |
| Day of    |    DOW    |     0-7      |     /n       | 0 or 7 = Sunday |
+-----------+-----------+--------------+--------------+-----------------+
```

### Cron Directories for Regular Intervals

For tasks that need to run at regular intervals without custom scheduling, cron provides specific directories:

```
/etc/cron.hourly/
├── task1
├── task2
└── ...

/etc/cron.daily/
├── task1
├── task2
└── ...

/etc/cron.weekly/
├── task1
├── task2
└── ...

/etc/cron.monthly/
├── task1
├── task2
└── ...
```

| Directory               | Description                          |
|-------------------------|--------------------------------------|
| **`/etc/cron.hourly/`**  | Place scripts here to run every hour. |
| **`/etc/cron.daily/`**   | Scripts run once daily.              |
| **`/etc/cron.weekly/`**  | Scripts execute once a week.         |
| **`/etc/cron.monthly/`** | Scripts run once a month.            |

#### How These Directories Work

The system crontab (`/etc/crontab`) includes entries that trigger the execution of scripts in these directories.

Example entry from `/etc/crontab`:

```
# Run hourly jobs
01 * * * * root run-parts /etc/cron.hourly
```

`run-parts` is a utility that executes all scripts in the specified directory.

### Creating Custom Schedules with Crontab

To schedule tasks at specific times, you can create custom crontab entries.

#### Editing the Crontab File

Open the crontab editor:

```
crontab -e
```

Add your scheduled tasks using the crontab syntax.

#### Example: Append a Message Every 15 Minutes

To add "15 minutes have elapsed" to a log file every 15 minutes:

```crontab
*/15 * * * * echo "15 minutes have elapsed" >> /path/to/your/timer.log
```

#### Using Environment Variables

You can set environment variables in your crontab:

```crontab
PATH=/usr/local/bin:/usr/bin:/bin
```

### Advanced Scheduling Techniques

#### Using Step Values

Use `*/N` to run a task every N units of time.

Run a script every 3 hours:

```
0 */3 * * * /path/to/script.sh
```

#### Specific Days and Times

I. Use commas to separate days.

Run a task on Mondays, Wednesdays, and Fridays:

```
0 9 * * 1,3,5 /path/to/task.sh
```

II. Combine ranges and steps.

Run a command every 2 hours between 8 AM and 4 PM:

```
0 8-16/2 * * * /path/to/command
```

#### Special Strings

Cron allows the use of special strings instead of the five time fields:

| Schedule               | Description                                        |
|------------------------|----------------------------------------------------|
| **`@reboot`**          | Run once at startup.                               |
| **`@yearly`** or **`@annually`** | Run once a year (`0 0 1 1 *`).               |
| **`@monthly`**         | Run once a month (`0 0 1 * *`).                    |
| **`@weekly`**          | Run once a week (`0 0 * * 0`).                     |
| **`@daily`** or **`@midnight`** | Run once a day (`0 0 * * *`).                |
| **`@hourly`**          | Run once an hour (`0 * * * *`).                    |

For example, to schedule the script `weekly_task.sh` to run every week, use the cron job entry:

```crontab
@weekly /path/to/weekly_task.sh
```

#### Managing Cron Allow and Deny

- The `/etc/cron.allow` file is used to specify which users are allowed to access and use the cron service for scheduling tasks.
- Conversely, the `/etc/cron.deny` file lists users who are explicitly denied permission to use cron for task automation.
- If **neither** of these files exists on the system, only the superuser is permitted to use cron, restricting access to regular users.

#### Editing System-Wide Crontab

- System-wide crontab entries can be added to files in `/etc/cron.d/`.
- These files have an additional field to specify the user.

For example, to run the `system_backup.sh` script as the root user every day at 2:30 AM, use the cron job entry:

```crontab
# m h dom mon dow user  command
30 2 * * * root /usr/local/bin/system_backup.sh
```

### Example Scenarios

#### Scenario 1: Database Backup

Backup a database every night at 11:30 PM.

```crontab
30 23 * * * /usr/local/bin/backup_database.sh >> /var/log/db_backup.log 2>&1
```

#### Scenario 2: Clear Cache Weekly

Clear application cache every Sunday at 3:00 AM.

```crontab
0 3 * * 0 /usr/bin/php /var/www/html/app/clear_cache.php
```

#### Scenario 3: System Update

Run system updates on the 1st and 15th of every month at 4:00 AM.

```crontab
0 4 1,15 * * /usr/bin/apt update && /usr/bin/apt upgrade -y
```

### Best Practices

#### Use Absolute Paths

Always specify the full path to commands and scripts.

```crontab
0 2 * * * /usr/bin/python3 /home/user/scripts/backup.py
```

#### Redirect Output

- For **standard output** redirection, the `>` symbol is used to overwrite the contents of a file, while `>>` is used to append output to an existing file without overwriting it.
- To redirect **standard error**, the `2>` operator is used to overwrite the error output to a file, while `2>>` appends the error output to the file instead of overwriting it.
- 
For example, to execute `/path/to/command` every day at 2:00 AM and direct both standard output and error output to a log file, use the cron job entry:

```crontab
0 2 * * * /path/to/command >> /var/log/command.log 2>&1
```

#### Environment Variables

Cron runs with a minimal environment. If your command depends on certain variables, define them in the crontab or within your script.

For example, to run `script.sh` every day at 5:00 AM using the Bash shell and specifying the PATH environment, set the cron job as follows:

```crontab
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

0 5 * * * /path/to/script.sh
```

#### Test Your Commands

Before adding them to the crontab, test your commands in the terminal to ensure they work as expected.

#### Monitoring and Logging

- Check cron logs to verify task execution.
- Logs are typically found at `/var/log/cron`, `/var/log/syslog`, or `/var/log/messages`.

#### Avoid Overlapping Jobs

For tasks that may take longer than the scheduling interval, prevent overlapping executions.

This script example ensures that only one instance of the script can run at a time by using a file lock. Here’s how it works:

```bash
#!/bin/bash
(
  flock -n 9 || exit 1
  # Your script commands go here
) 9>/var/lock/.myscript.exclusive
```

- `flock -n 9` attempts to acquire an exclusive, non-blocking lock on file descriptor 9. If the lock cannot be acquired because another instance is running, it immediately exits with `exit 1`.
- `9>/var/lock/.myscript.exclusive` specifies the lock file. This file is used to track the lock status; if it’s locked, another instance will not start.
  
### Common Pitfalls

- Cron uses the system's time zone. Ensure it's set correctly.
- Ensure scripts have execute permissions (`chmod +x script.sh`).
- Always end your crontab file with a newline character.
- Avoid using relative paths; cron's working directory is not guaranteed.

For further exploration and to test cron expressions, consider using online tools like [Crontab Guru](https://crontab.guru/). Always refer to the man pages (`man cron`, `man crontab`) for comprehensive documentation.

### Challenges

1. List the contents of the `/etc/cron.d` directory to identify any system-defined cron jobs. Examine the structure and contents of a few files using `cat` or `less` to understand how these jobs are defined. Reflect on the purpose of each file and how it might be used for system maintenance.
2. Explore the scripts located in `/etc/cron.monthly` and choose a few to examine with `cat`. For each script, determine what task it performs and hypothesize why it might be scheduled on a monthly basis. Consider what types of tasks benefit from monthly scheduling as you explore.
3. Given the cron schedule `0 2 * * *`, determine the exact time and frequency this job runs. Write down your interpretation of each field in the cron expression, and explain how you arrived at the conclusion that this job runs at 2:00 AM daily.
4. For the cron schedule `0 13 * * 2-4`, determine the days of the week and the time this job is scheduled to run. Break down each field of the cron expression, then test your understanding by translating it into a human-readable schedule (e.g., "every Tuesday through Thursday at 1:00 PM").
5. Write a shell script that appends the message “15 minutes have elapsed” to a log file located at `~/your_timer.log`. Schedule this script using `crontab -e` to run every 15 minutes. Verify your setup by giving the script executable permissions, waiting for it to run, and then checking the log file to confirm it’s working as intended.
6. Use `crontab -l` to view all your active cron jobs and locate the one created in the previous challenge. Then, remove all cron jobs using `crontab -r` and confirm the deletion with `crontab -l`. Document what happens when you remove all cron jobs and the implications for your scheduled tasks.
7. Modify the script from challenge 5 to include error handling: if the script cannot write to `~/your_timer.log` (e.g., due to permission issues), it should log an error message to `~/your_timer_error.log`. Test the script by temporarily changing permissions to simulate an error, then check both log files to see the results.
8. Investigate the use of special cron characters such as `*`, `,`, `-`, and `/` to build more complex schedules. Create a new cron job that runs every 5 minutes during the first 15 minutes of each hour (e.g., at :00, :05, and :10 of each hour). Use `crontab -l` to confirm the job is correctly defined.
9. Research cron’s ability to send output and error messages to a specific email address. Configure a test cron job that sends an email notification to a chosen address each time it runs. You may need to adjust your cron configuration and ensure a mail utility is set up on your system. Test the setup by checking your email after the job runs.
10. Create a cron job that performs a conditional task based on the system’s uptime. Write a script that checks the uptime, and if it’s greater than 24 hours, appends a message to a log file. Schedule this script to run hourly. Test the job by adjusting the script to simulate various uptime values and checking the log file for accuracy.
