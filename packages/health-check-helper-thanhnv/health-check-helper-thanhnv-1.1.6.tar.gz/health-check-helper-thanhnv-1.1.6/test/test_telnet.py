from telnet.check_multithread import MultiThreadsTelnetJob

work_data = [
    "10.1.44.16,8020"
]
number_thread= 10000

job = MultiThreadsTelnetJob(work_iterable=work_data, max_workers=number_thread)

job.run()
result = job.get_result()
print(result)