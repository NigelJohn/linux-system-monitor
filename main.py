# main.py
try:
    from monitor.collector import collect_all
    from monitor.logger import init_db, log_stats
except Exception as e:
    print("Import failed:", e)
    raise
import time

if __name__ == "__main__":
    init_db()  # Ensure DB is set up

    while True:
        stats = collect_all()
        log_stats(stats)
        print("Logged at", stats["timestamp"])
        time.sleep(5) 