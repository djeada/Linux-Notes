# Cron

Cron is a powerful utility in Unix-like operating systems that automates the execution of scripts or commands at specified times, dates, or intervals. It's an essential tool for system administrators and users alike, facilitating tasks such as system maintenance, backups, updates, and more.

## How Cron Works

Cron operates through a background process called the **cron daemon** (`crond`), which continuously runs and checks for scheduled tasks in crontab files. When the current time matches a scheduled time in the crontab, the cron daemon executes the associated command or script.

### Workflow Diagram

```
+---------------------------------------------------+
|                                                   |
|             Cron Workflow Overview                |
|                                                   |
+---------------------------------------------------+

User/System Schedules Tasks
          │
          ▼
+----------------+      +-------------------+
|                |      |                   |
|  Cron Daemon   |----->|  Crontab Files    |
|   (crond)      |      |                   |
|                |      +-------------------+
|  (Runs Every   |               │
|   Minute)      |               ▼
|                |      +-------------------+
+----------------+      |                   |
                        |  Executes Tasks   |
                        |  at Scheduled     |
                        |  Times            |
                        |                   |
                        +-------------------+
```

1. **Task Scheduling**: Users or the system define tasks in crontab files.
2. **Cron Daemon**: The cron daemon wakes up every minute and checks the crontab files.
3. **Task Execution**: If the current time matches a scheduled task, cron executes the command or script.

## Types of Crontab Files

Cron uses two main types of crontab files to schedule tasks:

### System Crontabs

- **Location**: `/etc/crontab`
- **Purpose**: Managed by the system administrator (`root` user) for system-wide tasks.
- **Usage**: Schedule routine maintenance tasks, system updates, and other automated processes.
- **Example Entry**:

  ```
  # m h dom mon dow user  command
    0 * * * *   root  /usr/bin/apt update
  ```

  - Runs `apt update` every hour as the `root` user.

### User Crontabs

- **Location**: Stored in `/var/spool/cron/crontabs/` (location may vary).
- **Purpose**: Individual files for each user to schedule personal tasks.
- **Usage**: Allows users to automate tasks without administrative permissions.
- **Access Commands**:
  - **Edit Crontab**: `crontab -e`
  - **List Crontab**: `crontab -l`
  - **Remove Crontab**: `crontab -r`

## Understanding Crontab Syntax

A crontab file consists of lines with six fields: five time fields and a command field.

### Crontab Field Structure

```
┌───────────── Minute (0 - 59)
│ ┌───────────── Hour (0 - 23)
│ │ ┌───────────── Day of Month (1 - 31)
│ │ │ ┌───────────── Month (1 - 12 or Jan-Dec)
│ │ │ │ ┌───────────── Day of Week (0 - 7 or Sun-Sat)
│ │ │ │ │
* * * * * command_to_execute
```

### Field Descriptions

- **Minute**: `0` to `59`
- **Hour**: `0` to `23`
- **Day of Month**: `1` to `31`
- **Month**: `1` to `12` or abbreviated month names (`Jan`, `Feb`, etc.)
- **Day of Week**: `0` to `7` (both `0` and `7` are Sunday) or abbreviated day names (`Sun`, `Mon`, etc.)

### Special Characters

- **Asterisk (`*`)**: Represents all possible values for a field.
- **Comma (`,`)**: Separates multiple values.
- **Hyphen (`-`)**: Defines a range.
- **Slash (`/`)**: Specifies step values.

### Examples

1. **Run a command every day at 2:00 AM**:

   ```
   0 2 * * * /path/to/command
   ```

2. **Run a script at 1:00 PM on Tuesdays, Wednesdays, and Thursdays**:

   ```
   0 13 * * 2-4 /path/to/script.sh
   ```

3. **Execute a backup at 7:30 AM from Monday to Friday**:

   ```
   30 7 * * 1-5 /path/to/backup.sh
   ```

4. **Run a task at 10:15 PM on the 1st of every month**:

   ```
   15 22 1 * * /path/to/monthly_task.sh
   ```

5. **Execute a script at midnight on January 1st every year**:

   ```
   0 0 1 1 * /path/to/new_year_script.sh
   ```

6. **Run a command every 5 minutes**:

   ```
   */5 * * * * /path/to/command
   ```

### Visualizing Time Fields

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

## Cron Directories for Regular Intervals

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

- **`/etc/cron.hourly/`**: Place scripts here to run every hour.
- **`/etc/cron.daily/`**: Scripts run once daily.
- **`/etc/cron.weekly/`**: Scripts execute once a week.
- **`/etc/cron.monthly/`**: Scripts run once a month.

### How These Directories Work

- The system crontab (`/etc/crontab`) includes entries that trigger the execution of scripts in these directories.
- Example entry from `/etc/crontab`:

  ```
  # Run hourly jobs
  01 * * * * root run-parts /etc/cron.hourly
  ```

- **`run-parts`**: A utility that executes all scripts in the specified directory.

## Creating Custom Schedules with Crontab

To schedule tasks at specific times, you can create custom crontab entries.

### Editing the Crontab File

- Open the crontab editor:

  ```
  crontab -e
  ```

- Add your scheduled tasks using the crontab syntax.

### Example: Append a Message Every 15 Minutes

To add "15 minutes have elapsed" to a log file every 15 minutes:

```crontab
*/15 * * * * echo "15 minutes have elapsed" >> /path/to/your/timer.log
```

### Using Environment Variables

You can set environment variables in your crontab:

```crontab
PATH=/usr/local/bin:/usr/bin:/bin
```

## Advanced Scheduling Techniques

### Using Step Values

- **Every N Units**: Use `*/N` to run a task every N units of time.
- **Example**: Run a script every 3 hours:

  ```
  0 */3 * * * /path/to/script.sh
  ```

### Specific Days and Times

- **Multiple Days**: Use commas to separate days.
  - Run a task on Mondays, Wednesdays, and Fridays:

    ```
    0 9 * * 1,3,5 /path/to/task.sh
    ```

- **Ranges and Steps**: Combine ranges and steps.
  - Run a command every 2 hours between 8 AM and 4 PM:

    ```
    0 8-16/2 * * * /path/to/command
    ```

### Special Strings

Cron allows the use of special strings instead of the five time fields:

- **`@reboot`**: Run once at startup.
- **`@yearly`** or **`@annually`**: Run once a year (`0 0 1 1 *`).
- **`@monthly`**: Run once a month (`0 0 1 * *`).
- **`@weekly`**: Run once a week (`0 0 * * 0`).
- **`@daily`** or **`@midnight`**: Run once a day (`0 0 * * *`).
- **`@hourly`**: Run once an hour (`0 * * * *`).

**Example**:

```crontab
@weekly /path/to/weekly_task.sh
```

## Managing Cron Allow and Deny

- **`/etc/cron.allow`**: Specifies users allowed to use cron.
- **`/etc/cron.deny`**: Specifies users denied from using cron.
- If neither file exists, only the superuser can use cron.

## Editing System-Wide Crontab

- System-wide crontab entries can be added to files in `/etc/cron.d/`.
- These files have an additional field to specify the user.

**Example** (`/etc/cron.d/system_backup`):

```crontab
# m h dom mon dow user  command
30 2 * * * root /usr/local/bin/system_backup.sh
```


## Example Scenarios

### Scenario 1: Database Backup

- **Task**: Backup a database every night at 11:30 PM.
- **Crontab Entry**:

  ```crontab
  30 23 * * * /usr/local/bin/backup_database.sh >> /var/log/db_backup.log 2>&1
  ```

### Scenario 2: Clear Cache Weekly

- **Task**: Clear application cache every Sunday at 3:00 AM.
- **Crontab Entry**:

  ```crontab
  0 3 * * 0 /usr/bin/php /var/www/html/app/clear_cache.php
  ```

### Scenario 3: System Update

- **Task**: Run system updates on the 1st and 15th of every month at 4:00 AM.
- **Crontab Entry**:

  ```crontab
  0 4 1,15 * * /usr/bin/apt update && /usr/bin/apt upgrade -y
  ```

## Best Practices

### Use Absolute Paths

Always specify the full path to commands and scripts.

```crontab
0 2 * * * /usr/bin/python3 /home/user/scripts/backup.py
```

### Redirect Output

- **Standard Output**: Use `>` to overwrite or `>>` to append.
- **Standard Error**: Redirect errors using `2>` or `2>>`.
- **Example**:

  ```crontab
  0 2 * * * /path/to/command >> /var/log/command.log 2>&1
  ```

### Environment Variables

Cron runs with a minimal environment. If your command depends on certain variables, define them in the crontab or within your script.

**Example**:

```crontab
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

0 5 * * * /path/to/script.sh
```

### Test Your Commands

Before adding them to the crontab, test your commands in the terminal to ensure they work as expected.

### Monitoring and Logging

- Check cron logs to verify task execution.
- Logs are typically found at `/var/log/cron`, `/var/log/syslog`, or `/var/log/messages`.

### Avoid Overlapping Jobs

For tasks that may take longer than the scheduling interval, prevent overlapping executions.

**Example Using a Lock File**:

```bash
#!/bin/bash
(
  flock -n 9 || exit 1
  # Your script commands go here
) 9>/var/lock/.myscript.exclusive
```

## Common Pitfalls

- **Incorrect Time Zones**: Cron uses the system's time zone. Ensure it's set correctly.
- **Permissions**: Ensure scripts have execute permissions (`chmod +x script.sh`).
- **No Newline at EOF**: Always end your crontab file with a newline character.
- **Relative Paths**: Avoid using relative paths; cron's working directory is not guaranteed.

For further exploration and to test cron expressions, consider using online tools like [Crontab Guru](https://crontab.guru/). Always refer to the man pages (`man cron`, `man crontab`) for comprehensive documentation.

1. Use the `ls` command to list any system files in the `/etc/cron.d` directory. Explore the contents of a few of these files using the `cat` command to see how they are structured.
2. Use the `ls` command to list scripts in the `/etc/cron.monthly` directory. Pick a few scripts and look at their contents using the `cat` command to understand what tasks they perform and how they are scheduled.
3. For a cron job with the schedule `0 2 * * *`, find out what time and how often this task runs. Explain how you arrived at your conclusion.
4. For a cron job with the schedule `0 13 * * 2-4`, find out what days and at what time this task runs. Explain how you arrived at your conclusion.
5. Write a shell script that appends the string "15 minutes have elapsed" to a log file at `~/your_timer.log` every 15 minutes. Use `crontab -e` to schedule this script to run at the correct interval. Make sure to give your script the correct permissions using `chmod` so it can be executed. After you have set up the cron job, wait for it to run at least once and then check `~/your_timer.log` to verify that your script is running as expected.
6. Use `crontab -l` to view your currently scheduled cron jobs. Identify the job you created in the previous challenge. Then use `crontab -r` to remove all your cron jobs. Use `crontab -l` again to confirm they have been removed. Note: `crontab -r` will remove all your cron jobs, not just the one you created in the previous challenge.
7. Modify your script from challenge 5 to include error handling. If your script fails to write to the log file (e.g., due to permissions issues), it should write an error message to a separate log file at `~/your_timer_error.log`.
8. Research how to use special characters like `*`, `,`, `-`, and `/` to create more complex cron schedules. Then create a cron job that runs at a non-standard interval (e.g., every 5 minutes during the first 15 minutes of every hour).
