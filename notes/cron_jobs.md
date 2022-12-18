## Cron
Cron is a powerful tool for scheduling tasks in Linux systems. It allows you to execute scripts and commands at regular intervals, allowing you to automate tasks and keep your system running smoothly.

The cron daemon is a background process that runs continuously, checking special files known as crontabs for scripts or commands that need to be executed. There are two types of crontabs: system crontabs, which are stored in the `/etc/crontab` file and are typically configured by the root user or daemons, and user crontabs, which are created and managed by individual users.

## Cron directories

There are several directories on a Linux machine where you can place scripts to be run at regular intervals:

* `/etc/cron.hourly`: scripts in this directory are run once per hour.
* `/etc/cron.daily`: scripts in this directory are run once per day.
* `/etc/cron.weekly`: scripts in this directory are run once per week.
* `/etc/cron.monthly`: scripts in this directory are run once per month.

## Custom schedule

If you need to schedule tasks with a more custom schedule, you can create a crontab file in the `/etc/cron.d` directory. Each file in this directory is read by the cron daemon and the scheduling is specified using five fields: minutes, hours, day of the month, month, and day of the week.

To specify a schedule, you can use the following syntax:

* Minutes: a range from 0 to 59, or an asterisk `(*)` to indicate every minute.
* Hours: a range from 0 to 23 (using a 24 hour clock), or an asterisk (`*`) to indicate every hour.
* Day of the month: a range from 1 to 31, or an asterisk (`*`) to indicate every day.
* Month: a range from 1 to 12, or an asterisk (`*`) to indicate every month.
* Day of the week: a range from 0 to 7 (with 0 or 7 representing Sunday), or an asterisk (`*`) to indicate every day of the week.

To create a crontab file, you can use the `crontab -e` command to edit the current crontab, or use the `crontab -l` command to list all the current cron jobs. To delete the current crontab, you can use the `crontab -r` command.

Here are some examples of cron schedules:

* `0 2 * * *`: this cron job will run every day at 2:00 AM.
* `0 13 * * 2-4`: this cron job will run every Tuesday, Wednesday, and Thursday at 1:00 PM.

To create a script that will append the string "15 minutes have elapsed" to a log file every 15 minutes, you can use the following crontab entry:

```
*/15 * * * * echo "15 minutes have elapsed" >> /your timer.log
```

For more information about cron and how to use it, you can check out the crontab man page or visit the https://crontab.guru/ website, which provides a tool for experimenting with different cron schedules.

## Challenges

1. Use the `ls` command to determine if there are any system files located in the `/etc/cron.d` directory.
1. Use the `ls` command to list the scripts in the `/etc/cron.monthly` directory and examine their contents to determine if any scheduling is mentioned in the scripts.
1. Given the cron job schedule `0 2 * * *`, determine when the task would be run.
1. Given the cron job schedule `0 13 * * 2-4`, determine when the task would be run.
1. Create a script that will append the string "15 minutes have elapsed" to a log file located at `~/your_timer.log` every 15 minutes. Use the `crontab -e` command to schedule the script to run at the desired interval.
