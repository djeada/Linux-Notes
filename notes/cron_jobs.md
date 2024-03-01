## Cron

Cron is a utility that automates the execution of scripts or commands. This automation can be scheduled to occur at fixed times, dates, or intervals. The utility is commonly used for system maintenance tasks such as log rotation, backups, and system updates. 

Cron operates through a daemon, which is a background process that is always running. The cron daemon periodically checks for scheduled tasks in special files called crontabs. 

There are two types of crontabs:

- System crontabs: These are located in the `/etc/crontab` file and are typically managed by the system administrator or root user. They can also be used by system daemons to schedule routine tasks.
- User crontabs: These are individual crontab files for each user. They allow users to schedule their own scripts and commands without requiring administrative privileges.

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

## Cron Directories

Several directories are dedicated to cron jobs, each designed to execute scripts at different regular intervals:
* `/etc/cron.hourly`: Contains scripts that are run every hour.
* `/etc/cron.daily`: Contains scripts that are run daily.
* `/etc/cron.weekly`: Contains scripts that are run weekly.
* `/etc/cron.monthly`: Contains scripts that are run monthly.

These directories provide a convenient way to schedule scripts or commands at these standard intervals.

## Custom Schedules

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

* Minutes: Specify values from 0 to 59, or use `*` for every minute.
* Hours: Specify values from 0 to 23 (24-hour clock), or use `*` for every hour.
* Day of the month: Specify values from 1 to 31, or use `*` for every day.
* Month: Specify values from 1 to 12, or use `*` for every month.
* Day of the week: Specify values from 0 to 7 (both 0 and 7 represent Sunday), or use `*` for every day of the week.

Here are some examples of cron schedules:

* `0 2 * * *`: This job runs daily at 2:00 AM.
* `0 13 * * 2-4`: This job runs every Tuesday, Wednesday, and Thursday at 1:00 PM.

Let's say you want a script that adds "15 minutes have elapsed" to a log file every 15 minutes. You would use this crontab entry:

```shell
*/15 * * * * echo "15 minutes have elapsed" >> /path/to/your/timer.log
```

For more detailed information on cron and to experiment with different cron schedules, refer to the crontab manual page via the `man crontab` command in your terminal, or visit [Crontab Guru](https://crontab.guru/), a handy online tool for testing cron schedules.

## Challenges

1. Use the `ls` command to list any system files in the `/etc/cron.d` directory. Explore the contents of a few of these files using the `cat` command to see how they are structured.
2. Use the `ls` command to list scripts in the `/etc/cron.monthly` directory. Pick a few scripts and look at their contents using the `cat` command to understand what tasks they perform and how they are scheduled.
3. For a cron job with the schedule `0 2 * * *`, find out what time and how often this task runs. Explain how you arrived at your conclusion.
4. For a cron job with the schedule `0 13 * * 2-4`, find out what days and at what time this task runs. Explain how you arrived at your conclusion.
5. Write a shell script that appends the string "15 minutes have elapsed" to a log file at `~/your_timer.log` every 15 minutes. Use `crontab -e` to schedule this script to run at the correct interval. Make sure to give your script the correct permissions using `chmod` so it can be executed. After you have set up the cron job, wait for it to run at least once and then check `~/your_timer.log` to verify that your script is running as expected.
6. Use `crontab -l` to view your currently scheduled cron jobs. Identify the job you created in the previous challenge. Then use `crontab -r` to remove all your cron jobs. Use `crontab -l` again to confirm they have been removed. Note: `crontab -r` will remove all your cron jobs, not just the one you created in the previous challenge.
7. Modify your script from challenge 5 to include error handling. If your script fails to write to the log file (e.g., due to permissions issues), it should write an error message to a separate log file at `~/your_timer_error.log`.
8. Research how to use special characters like `*`, `,`, `-`, and `/` to create more complex cron schedules. Then create a cron job that runs at a non-standard interval (e.g., every 5 minutes during the first 15 minutes of every hour).
