## Cron

Cron is a utility that automates the execution of scripts or commands. This automation can be scheduled to occur at fixed times, dates, or intervals. The utility is commonly used for system maintenance tasks such as log rotation, backups, and system updates. 

Cron operates through a daemon, which is a background process that is always running. The cron daemon periodically checks for scheduled tasks in special files called crontabs. 

There are two types of crontabs available in a Unix-like system:

- **System crontabs** are found in the `/etc/crontab` file and are usually managed by the system administrator or root user. These crontabs are also utilized by system daemons to schedule routine maintenance tasks and other automated processes.
- **User crontabs** are individual files for each user, enabling them to schedule their own scripts and commands without the need for administrative permissions. This separation allows users to automate tasks without impacting the system-wide configuration managed by administrators.

The process of scheduling and executing a cron job can be illustrated with the following steps:

```
+------------+      +--------------+      +-------------+
|            |      |              |      |             |
| cron daemon|----->| crontab file |----->| Execute     |
| (crond)    |      |              |      | cron job    |
|            |      |              |      | at scheduled|
+------------+      +--------------+      | time        |
     ^                                 +--|             |
     |                                 |  +-------------+
     |                                 |
     |    +------------------------+   |
     +----| Every minute, check for|<--+
          | scheduled tasks in     |
          | crontab file           |
          +------------------------+
```

### Cron Directories

Several system directories are designated for cron jobs, each corresponding to a specific frequency for executing scripts:

- The `/etc/cron.hourly` directory is intended for scripts that need to run every hour.
- The `/etc/cron.daily` directory holds scripts that are executed once daily.
- The `/etc/cron.weekly` directory is used for scripts scheduled to run once a week.
- The `/etc/cron.monthly` directory contains scripts that are run once a month.

These directories offer a straightforward method for scheduling tasks at these common intervals, allowing administrators to easily manage regular maintenance and automated processes without needing to individually configure each script's timing.

### Custom Schedules

Creating custom schedules with crontab allows users to automate tasks based on specific time criteria. To configure these, place a custom crontab file in `/etc/cron.d`. The cron daemon processes each file in this directory, executing tasks as per the specified schedule, which consists of five time-and-date fields.

To manage crontab entries, several commands are available:

- `crontab -e`: Opens an editor to modify the current crontab, where you can insert your desired cron schedule.
- `crontab -l`: Displays a list of all active cron jobs.
- `crontab -r`: Removes the current crontab, effectively deleting all scheduled jobs.

A crontab entry is structured as follows, where each asterisk can be replaced with a specific time value:

```
+---------------- minute (0 - 59)
|  +------------- hour (0 - 23)
|  |  +---------- day of month (1 - 31)
|  |  |  +------- month (1 - 12)
|  |  |  |  +---- day of week (0 - 7) (Sunday=0 or 7)
|  |  |  |  |
*  *  *  *  *  command to be executed
```

- Minutes are specified with values ranging from 0 to 59, or `*` can be used to indicate every minute.
- Hours are specified using values from 0 to 23 (24-hour clock), with `*` indicating every hour.
- The day of the month can be specified with values from 1 to 31, or `*` can be used for every day.
- The month is indicated by values from 1 to 12, or `*` can be used to denote every month.
- The day of the week can be specified with values from 0 to 7 (where both 0 and 7 represent Sunday), or `*` can be used for every day of the week.

Here are some examples of cron schedules along with explanations:

- The schedule `0 2 * * *` specifies that the job will run daily at 2:00 AM.
- The schedule `0 13 * * 2-4` means the job will execute at 1:00 PM every Tuesday, Wednesday, and Thursday.
- The schedule `30 7 * * 1-5` specifies that the job will run at 7:30 AM from Monday to Friday.
- The schedule `15 22 1 * *` schedules a job to run at 10:15 PM on the 1st day of every month.
- The schedule `0 0 1 1 *` sets a job to execute at midnight on January 1st every year.
- The schedule `*/5 * * * *` runs a job every 5 minutes.

Let's say you want a script that adds "15 minutes have elapsed" to a log file every 15 minutes. You would use this crontab entry:

```shell
*/15 * * * * echo "15 minutes have elapsed" >> /path/to/your/timer.log
```

For more detailed information on cron and to experiment with different cron schedules, refer to the crontab manual page via the `man crontab` command in your terminal, or visit [Crontab Guru](https://crontab.guru/), a handy online tool for testing cron schedules.

### Challenges

1. Use the `ls` command to list any system files in the `/etc/cron.d` directory. Explore the contents of a few of these files using the `cat` command to see how they are structured.
2. Use the `ls` command to list scripts in the `/etc/cron.monthly` directory. Pick a few scripts and look at their contents using the `cat` command to understand what tasks they perform and how they are scheduled.
3. For a cron job with the schedule `0 2 * * *`, find out what time and how often this task runs. Explain how you arrived at your conclusion.
4. For a cron job with the schedule `0 13 * * 2-4`, find out what days and at what time this task runs. Explain how you arrived at your conclusion.
5. Write a shell script that appends the string "15 minutes have elapsed" to a log file at `~/your_timer.log` every 15 minutes. Use `crontab -e` to schedule this script to run at the correct interval. Make sure to give your script the correct permissions using `chmod` so it can be executed. After you have set up the cron job, wait for it to run at least once and then check `~/your_timer.log` to verify that your script is running as expected.
6. Use `crontab -l` to view your currently scheduled cron jobs. Identify the job you created in the previous challenge. Then use `crontab -r` to remove all your cron jobs. Use `crontab -l` again to confirm they have been removed. Note: `crontab -r` will remove all your cron jobs, not just the one you created in the previous challenge.
7. Modify your script from challenge 5 to include error handling. If your script fails to write to the log file (e.g., due to permissions issues), it should write an error message to a separate log file at `~/your_timer_error.log`.
8. Research how to use special characters like `*`, `,`, `-`, and `/` to create more complex cron schedules. Then create a cron job that runs at a non-standard interval (e.g., every 5 minutes during the first 15 minutes of every hour).
