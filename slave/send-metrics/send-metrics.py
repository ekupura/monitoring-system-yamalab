from influxdb import InfluxDBClient
import psutil

#init
db_name = 'testdb'
client = InfluxDBClient('ekupura.com', 8086, 'root', 'root', db_name)

dbs = client.get_list_database()
sample_db = {'name' : db_name}
if sample_db not in dbs:
    client.create_database(db_name)

# get_status
cpu = psutil.cpu_percent(interval=1)
cpus = psutil.cpu_percent(interval=1, percpu=True)
memory = psutil.virtual_memory().percent

json_body = [
{
  "fields" : {
    "cpu" : cpu,
    "memory" : memory,
  },
  "tags" : {
    "machine" : "grape"
  },
  "measurement" : "metrics"
}
]

for i,v in enumerate(cpus):
    json_body[0]["fields"]["cpu{}".format(i)] = v

client.write_points(json_body)
result = client.query('select cpu0 from metrics;')
print("Result: {0}".format(result))

