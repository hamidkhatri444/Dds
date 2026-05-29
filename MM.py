import subprocess
import time
import sys
from datetime import datetime

def run_with_delay(cmd, delay, label):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {label}: waiting {delay}s...")
    time.sleep(delay)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {label}: starting {' '.join(cmd)}")
    start = datetime.now()
    proc = subprocess.Popen(cmd)
    return proc, start, label

def main():
    if len(sys.argv) != 4:
        print("Usage: python run_three.py <IP> <port> <duration_sec>")
        sys.exit(1)

    ip, port, duration = sys.argv[1], sys.argv[2], sys.argv[3]

    # Three handlers – all in the same folder
    handlers = {
        "A": ["python", "A.py", ip, port, duration],
        "B": ["python", "B.py", ip, port, duration],
        "C": ["python", "C.py", ip, port, duration],
    }

    delays = [0, 20, 40]   # start gaps

    processes = []
    for (name, cmd), delay in zip(handlers.items(), delays):
        proc, start, label = run_with_delay(cmd, delay, f"Handler-{name}")
        processes.append((proc, start, label))

    print("\nAll handlers launched. Waiting for them to finish...\n")
    for proc, start, label in processes:
        ret = proc.wait()
        end = datetime.now()
        elapsed = (end - start).total_seconds()
        print(f"[{end.strftime('%H:%M:%S')}] {label}: finished after {elapsed:.1f}s (exit {ret})")

if __name__ == "__main__":
    main()