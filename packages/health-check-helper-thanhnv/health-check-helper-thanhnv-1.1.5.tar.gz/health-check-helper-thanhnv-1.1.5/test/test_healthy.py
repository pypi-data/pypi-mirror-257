from heath_check.health_check_job import MultiThreadsHeathCheckJob
from heath_check.model import read_from_json_file

if __name__ == '__main__':
    p = "monitor_source.json"
    list_health_check = read_from_json_file(p)
    job = MultiThreadsHeathCheckJob(list_health_check)
    job.run()
    result = job.get_result()
    print(result)
