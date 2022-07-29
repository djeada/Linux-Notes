## Cron jobs
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


## Cron directories

Put your script in the correct directory.

* /etc/cron.hourly <- those scripts run once per hour
* /etc/cron.daily <- those scripts run once per day
* /etc/cron.weekly <- those scripts run once per week
* /etc/cron.monthly <- those scripts run once per month

## What if your desired schedule is different?

You create a cron tab file in <code>/etc/cron.d</code>.

You have 5 fields: minutes, hour, day of the month, month, day of the week.

* Hours: 24 hour clock.
* Days of the week: number with minus, e.g. 1-5.

When creating a cron config in <code>/etc/cron.d/</code> or <code>/etc/crontab</code>, you must provide the username under whom the command should be performed. For example, to run a following command <code>tar -cvpzf archve.tar.gz --exclude=/mnt</code> every day at 1:00 AM under root, use:

```bash
0 1 * * * root tar -cvpzf archve.tar.gz --exclude=/mnt
```

There is also a very useful website for playing with cron times: https://crontab.guru/.

## Challenges

1. When would this system cron job run its task? <code>0 2 \* \* \*</code>
2. When would this system cron job run its task? <code>0 13 * * 2-4</code>
