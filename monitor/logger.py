import sqlite3
from pathlib import Path
import json

DB_PATH = Path("monitor.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS system_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_total REAL,
                cpu_per_core TEXT,
                memory_used INTEGER,
                memory_total INTEGER,
                disk_used INTEGER,
                disk_total INTEGER,
                net_sent INTEGER,
                net_recv INTEGER,
                top_processes TEXT
            );
        """)
        conn.commit()


def log_stats(data):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO system_stats (
                timestamp,
                cpu_total,
                cpu_per_core,
                memory_used,
                memory_total,
                disk_used,
                disk_total,
                net_sent,
                net_recv,
                top_processes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['timestamp'],
            data['cpu']['total'],
            json.dumps(data['cpu']['per_core']),
            data['memory']['used'],
            data['memory']['total'],
            data['disk']['used'],
            data['disk']['total'],
            data['network']['bytes_sent'],
            data['network']['bytes_recv'],
            json.dumps(data['top_processes']),
        ))
        conn.commit()
