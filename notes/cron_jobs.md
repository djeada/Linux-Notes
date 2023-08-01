## Cron
Cron is a tool for scheduling tasks on Linux systems. It lets you run scripts and commands regularly to automate tasks and keep your system working well.

Cron daemon is a background process that always runs, checking special files called crontabs for scripts or commands to run. There are two kinds of crontabs: system crontabs in `/etc/crontab` file, usually set up by root user or daemons, and user crontabs, managed by individual users.

```
+------------------+
| User sets up cron|
| job with specific|
| timing and script|
+------------------+
           |
           |
           v
+------------------+
| The cron daemon  |
| reads the job    |
| from crontab     |
+------------------+
           |
           |
           v
+------------------+
| Cron daemon      |
| launches the     |
| script/job at the|
| specified time   |
+------------------+
           |
           |
           v
+------------------+
| Script/job executes|
| as per the user's |
| instructions      |
+------------------+
```

## Cron directories

These directories on a Linux machine hold scripts to run at regular times:

* `/etc/cron.hourly`: scripts here run every hour.
* `/etc/cron.daily`: scripts here run every day.
* `/etc/cron.weekly`: scripts here run every week.
* `/etc/cron.monthly`: scripts here run every month.

## Custom schedule

For custom schedules, make a crontab file in `/etc/cron.d` directory. Cron daemon reads each file here and schedules using five fields: minutes, hours, day of the month, month, and day of the week.

Use this syntax for schedules:

* Minutes: 0 to 59 or `*` for every minute.
* Hours: 0 to 23 (24 hour clock) or `*` for every hour.
* Day of the month: 1 to 31 or `*` for every day.
* Month: 1 to 12 or `*` for every month.
* Day of the week: 0 to 7 (0 or 7 for Sunday) or `*` for every day of the week.

To make a crontab file, use `crontab -e` to edit current crontab, or `crontab -l` to list current cron jobs. To delete current crontab, use `crontab -r`.

Examples of cron schedules:

* `0 2 * * *`: this job runs daily at 2:00 AM.
* `0 13 * * 2-4`: this job runs every Tuesday, Wednesday, and Thursday at 1:00 PM.

For a script that adds "15 minutes have elapsed" to a log file every 15 minutes, use this crontab entry:

```
*/15 * * * * echo "15 minutes have elapsed" >> /your timer.log
```

For more about cron, see the crontab man page or https://crontab.guru/, a tool for trying different cron schedules.

## Challenges

1. Use `ls` to find any system files in `/etc/cron.d` directory.
2. Use `ls` to list scripts in `/etc/cron.monthly` directory and look at their contents for any scheduling.
3. For cron job schedule `0 2 * * *`, find out when the task runs.
4. For cron job schedule `0 13 * * 2-4`, find out when the task runs.
5. Make a script that adds "15 minutes have elapsed" to a log file at `~/your_timer.log` every 15 minutes. Use `crontab -e` to schedule the script for the right interval.

