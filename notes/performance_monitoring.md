## Performance Monitoring

Performance monitoring is an important aspect of system administration as it allows you to identify any potential bottlenecks or issues that may be affecting the performance of your system. In this article, we will explore some of the tools and techniques available for monitoring performance in Linux.

## The top command

The top command is a real-time system monitoring tool that allows you to view the resource usage of various processes running on your system. It provides a detailed overview of the CPU, memory, and swap usage, as well as the load average and uptime of your system.

You can run it without any flags and arguments:

```
top
```

This will display a list of processes sorted by CPU usage, with the highest usage at the top. You can use the `Shift + m` key combination to sort the processes by memory usage instead.

You can also use the `-p` flag to specify a specific process ID to monitor:

```
top -p 1234
```

## Swap space

Swap space is an area on your hard drive that is used as virtual memory when your system runs out of physical RAM. It allows your system to continue running even when it has exhausted all available RAM, but it can have a negative impact on performance as accessing data from the hard drive is slower than accessing it from RAM.

To view the amount of swap space available on your system, use the free command:

```
free -h
```

This will display the total, used, and free swap space in human-readable format (e.g. in MB or GB).

`Free` will display the total amount of RAM available, as well as the amount of used and free memory. If the used memory is close to the total amount of RAM, it may indicate that you are running out of RAM and may need to add more or optimize your usage.

## The vmstat command

`vmstat` displays information about system memory, swap, and CPU usage. It provides a snapshot of the current state of the system, as well as the average statistics over a period of time.

To view the current state of the system, use `vmstat` without any arguments. To view the average statistics over a period of time, use `vmstat [interval] [count]`, where interval is the time in seconds between each snapshot and count is the number of snapshots to take.

## Challenges

1. What command can you use to view the current CPU, memory, and swap usage in real-time?
1. How can you determine if your machine is running low on available memory?
1. What command can you use to view information about CPU and memory usage over time?
1. How can you identify which process is consuming the most CPU or memory resources on your system?
1. What are some common signs that a machine is reaching its limits in terms of CPU, memory, or disk usage?
