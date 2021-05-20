It finds all files larger than 10 MB and long lists them using the ls command.
find / -size +10M -exec ls -l {} ;
