import subprocess
import json

DEFAULT_ATTRIBUTES_GPU = (
    'utilization.gpu',
    'utilization.memory',
    'temperature.gpu'
)

DEFAULT_ATTRIBUTES_APPS = (
    'process_name',
)

def stringToValue(dict):
    for k in dict.keys():
        try:
            dict[k] = float(dict[k])
        except:
            pass
    return dict

def getGpuInfo(nvidia_smi_path='nvidia-smi', keys=DEFAULT_ATTRIBUTES_GPU, apps =
        DEFAULT_ATTRIBUTES_APPS, no_units=True):
    nu_opt = '' if not no_units else ',nounits'
    cmd = '%s --query-gpu=%s --format=csv,noheader%s' % (nvidia_smi_path, ','.join(keys), nu_opt)
    output = subprocess.check_output(cmd, shell=True).decode('utf-8') + ', '
    cmd = '%s --query-compute-apps=%s --format=csv%s' % (nvidia_smi_path, ','.join(apps), nu_opt)
    output += subprocess.check_output(cmd, shell=True).decode('utf-8')
    lines = output.replace('\n','').split(', ')
    dict = {k: l for k, l in zip(keys + apps, lines)}
    return stringToValue(dict)
