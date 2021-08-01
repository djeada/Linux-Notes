<h2>Cron jobs</h2>
If you wish to execute some scripts on a regular basis, use cron jobs.

Cron daemon starts running when the system boots up. 
It runs in the background continuously and examines special files known as cron tabs every minute to see whether there is a script that should be running right now.
You can check those files with:

```bash
cat /etc/crontab
```

You can configure cron to run to different types of jobs:
1. System jobs
2. User jobs


<h2>Cron directories</h2>

Put your script in the correct directory.

* /etc/cron.hourly <- those scripts run once per hour
* /etc/cron.daily <- those scripts run once per day
* /etc/cron.weekly <- those scripts run once per week
* /etc/cron.monthly <- those scripts run once per month

<h2>What if your schedule is different?</h2>

You create a cron tab file in /etc/cron.d

You have 5 fields: minutes, hour, day of the month, month, day of the week.

* Hours: 24 hour clock.
* Days of the week: number with minus, e.g. 1-5.

When creating a cron config in /etc/cron.d/ or /etc/crontab, you must provide the username under whom the command should be performed:

```bash
0 1 * * * root tar -cvpzf archve.tar.gz --exclude=/mnt /
```

When would this system cron job run its task? 
Ans: every day at 1:00 AM.
