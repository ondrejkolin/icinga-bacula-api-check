# Icinga Bacula plugin

This is a simple extension, which does over HTTP API check on failed jobs. It differs running jobs, waiting jobs and failed jobs. Limits can be adjusted. Currenty only `http basic auth` is supported

## Usage and example
 
 ```
Usage: icinga_bacula_check.py [options]

Options:
  -h, --help           show this help message and exit
  -w WAITING_WARNING   Limit for jobs on waiting state to trigger warning
                       status
  -W WAITING_CRITICAL  Limit for jobs on waiting state to trigger critical
                       status
  -r RUNNING_WARNING   Limit for jobs on running state to trigger warning
                       status
  -R RUNNING_CRITICAL  Limit for jobs on running state to trigger critical
                       status
  -e ERROR_WARNING     Limit for jobs on error state to trigger warning status
  -E ERROR_CRITICAL    Limit for jobs on error state to trigger critical
                       status
  -l, --list-ids       Limit for jobs on error state to trigger critical
                       status
```
Example:
```
icinga_bacula_check.py -a https://backups.benocs.com/api/ -u icinga -p password
```
