import psutil
import datetime


def get_cpu_usage():
    return {
        "total": psutil.cpu_percent(interval=0.5),
        "per_core": psutil.cpu_percent(interval=0.5, percpu=True),
    }


def get_memory_usage():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "used": mem.used,
        "available": mem.available,
        "percent": mem.percent,
    }


def get_swap_usage():
    swap = psutil.swap_memory()
    return {
        "total": swap.total,
        "used": swap.used,
        "free": swap.free,
        "percent": swap.percent,
    }


def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
    }


def get_network_io():
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv,
    }


def get_top_processes(n=5):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:n]
    return top


def collect_metrics():
    timestamp = datetime.datetime.now().isoformat()
    return {
        "timestamp": timestamp,
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "swap": get_swap_usage(),
        "disk": get_disk_usage(),
        "network": get_network_io(),
        "top_processes": get_top_processes()
    }
