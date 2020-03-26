#!/usr/bin/env python3
import requests, json

BACULA_CODES_OK="TA"
BACULA_CODES_WAITING="FSmMsjcdtp"
BACULA_CODES_RUNNING="RC"

JOB_KEYS = ['ok', 'running', 'waiting', 'error']

def get_all_jobs():
    endpoint = "jobs/"
    session = requests.Session()
    if option.api_user is not None and option.api_password is not None:
        session.auth = (option.api_user, option.api_password)

    uri = option.api_url + endpoint
    response = session.get(uri)
    if response.status_code != 200:
        raise Exception("{} not accesible with status code {}".format(uri, response.status_code))
    return json.loads(response.content)

def validate_jobs(jobs):
    counter = {"ok": 0, "running": 0, "waiting": 0, "error": 0, "total": len(jobs)}
    ids = {"running": [], "waiting": [], "error": []}
    for job in jobs:
        if job['jobstatus'] in BACULA_CODES_OK:
            counter['ok'] += 1
        elif job['jobstatus'] in BACULA_CODES_WAITING:
            counter['waiting'] += 1
            ids['waiting'].append(job['jobid'])
        elif job['jobstatus'] in BACULA_CODES_RUNNING:
            counter['running'] += 1
            ids['running'].append(job['jobid'])
        else:
            counter['error'] += 1
            ids['error'].append(job['jobid'])
    return (counter, ids)

def print_result(counter, ids):
    result_str="SUM: {}".format(counter['total'])
    for key in JOB_KEYS:
        if counter[key] > 0:
            result_str += "/{}: {}".format(key[:3].upper(), counter[key])
            if option.list_ids and key != 'ok':
                result_str += " " + str(ids[key])
    print(result_str)

def status_code(counter):
    if (counter['ok'] == counter['total']):
        return 0
    status_code = 0
    for key in JOB_KEYS[1:]: 
        if counter[key] >= option.__getattribute__(key+"_critical"):
            return 2
        elif counter[key] >= option.__getattribute__(key+"_warning"):
            status_code = 1
    return status_code
            


if __name__ == '__main__':
    from optparse import OptionParser
    import sys

    parser = OptionParser()
    parser.add_option('-a', '--api', dest="api_url", help="Base api url like https://bacula.benocs.com/api/v1", nargs=1)
    parser.add_option('-u', '--api-user', dest="api_user", help="API Http authentication username")
    parser.add_option('-p', '--api-password', dest="api_password", help="API Http authentication password")
    parser.add_option('-w', dest="waiting_warning", help="Limit for jobs on waiting state to trigger warning status", default=1, type=int)
    parser.add_option('-W', dest="waiting_critical", help="Limit for jobs on waiting state to trigger critical status", default=1, type=int)
    parser.add_option('-r', dest="running_warning", help="Limit for jobs on running state to trigger warning status", default=1, type=int)
    parser.add_option('-R', dest="running_critical", help="Limit for jobs on running state to trigger critical status", default=5, type=int)
    parser.add_option('-e', dest="error_warning", help="Limit for jobs on error state to trigger warning status", default=1, type=int)
    parser.add_option('-E', dest="error_critical", help="Limit for jobs on error state to trigger critical status", default=1, type=int)
    parser.add_option('-l', '--list-ids', dest="list_ids", help="Limit for jobs on error state to trigger critical status", action="store_true", default=False)
    (option, args) = parser.parse_args()
    jobs = get_all_jobs()
    counter, ids = validate_jobs(jobs['output'])
    print_result(counter, ids)
    sys.exit(status_code(counter))

    
