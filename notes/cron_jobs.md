## Cron jobs

* If you wish to execute some scripts on a regular basis, use cron jobs.
* Cron daemon starts running when the system boots up. 
* It runs in the background continuously and examines special files known as cron tabs every minute to see whether there is a script that should be running right now.
* The file `/etc/crontab` contains the system crontabs.Those tasks are typically configured exclusively by the root user or daemons.

You can configure cron to run to different types of jobs:
1. System jobs.
2. User jobs.

## Cron directories

These are pre-created directories that are present on every Linux machine.
If you place your script in one of those directories, it will run at the given intervals. 

* */etc/cron.hourly* - those scripts run once per hour.
* */etc/cron.daily* - those scripts run once per day.
* */etc/cron.weekly* - those scripts run once per week.
* */etc/cron.monthly* - those scripts run once per month.

## What if your desired schedule is different?

You create a cron tab file in `/etc/cron.d`. Every file in that directory is read by a *cron deamon*.

To specify the scheduling, you must fill out five fields: minutes, hour, day of the month, month, and day of the week.

* Hours: 24 hour clock.
* Days of the week: number with minus, e.g. 1-5.
* \* means every (like every minute or every hour).
* \*/n means every n'th (like every n'th minute).

Additionally when creating a cron config in `/etc/cron.d/` or `/etc/crontab`, you must provide the username under whom the command should be performed. For example, to run a following command `tar -cvpzf archve.tar.gz --exclude=/mnt` every day at 1:00 AM as a *root* user, use:

```bash
0 1 * * * root tar -cvpzf archve.tar.gz --exclude=/mnt
```

To add a crontab trough a command, use:

```bash
crontab -e
```

To list all your cron jobs, use:

```bash
crontab -l
```

To delete the current cron jobs, use:

```bash
crontab -r
```

## Additional resources

There is also an excellent website for experimenting with cron times: https://crontab.guru/.

## Challenges

1. Are there any system files located at `/etc/cron.d`?
2. Is there any scheduling mentioned in the scripts located at `/etc/cron.monthly`? 
3. When would this system cron job run its task? `0 2 \* \* \*`
4. When would this system cron job run its task? `0 13 * * 2-4`
5. Create a script that will append the string "15 minutes have elapsed" to the log file located at `/your timer.log` every 15 minutes. 
