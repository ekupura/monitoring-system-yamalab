from influxdb import InfluxDBClient
import psutil
import socket
import nvidia
import re
import sched, time

# init
db_name = 'gpu_db'
domein = 'ekupura.com'
user = 'root'
password = 'root'
ports = 8086

client = InfluxDBClient(domein, ports, user, password, db_name)

dbs = client.get_list_database()
sample_db = {'name' : db_name}
if sample_db not in dbs:
    client.create_database(db_name)

sc = sched.scheduler(time.time, time.sleep)

def send():
    # get info
    host_name = socket.gethostname()
    cpu = psutil.cpu_percent(interval=1)
    cpus = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory().percent
    gpu_info = nvidia.getStatus()
    gpu_temp = float(re.match("\d*",gpu_info["GPU Current Temp"]).group())
    gpu_memory = float(re.match("\d*",gpu_info["Memory"]).group())
    gpu_gpu = float(re.match("\d*",gpu_info["Gpu"]).group())
    pro = 0 if gpu_info["Processes"] == 'None' else 1

    # define json_body
    json_body = [
    {
      "fields" : {
      },
      "tags" : {
      },
      "measurement" : "measurement"
    }
    ]

    # put info in json_body
    json_body[0]["tags"]["machine"] = host_name
    json_body[0]["fields"]["CPU"] = cpu
    json_body[0]["fields"]["Memory"] = memory
    for i,v in enumerate(cpus):
        json_body[0]["fields"]["CPU{}".format(i)] = v
    json_body[0]["fields"]["GPU Current Temp"] = gpu_temp
    json_body[0]["fields"]["GPU Memory"] = gpu_memory
    json_body[0]["fields"]["GPU"] = gpu_gpu
    json_body[0]["fields"]["Processes"] = pro


    # send json_body to influxdb
    client.write_points(json_body)
    print("OK!")


while True:
    sc.enter(30, 1, send)
    sc.run()



