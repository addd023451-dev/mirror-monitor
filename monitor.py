import requests
import time
import json
from datetime import datetime

# لیست Mirror های فرضی برای PyPI
MIRRORS = {
    "Official PyPI": "https://pypi.org/simple/",
    "Mirror 1": "https://mirror-1.pypi.local/simple/", # لینک‌های فرضی (می‌توانید با میرورهای واقعی جایگزین کنید)
    "Mirror 2": "https://mirror-2.pypi.local/simple/"
}

TIMEOUT = 5 # Maximum wait time in seconds

def test_mirror(name, url):
    """
    تست سرعت و در دسترس بودن یک میرور.
    یک درخواست HTTP GET ارسال می‌کند و زمان پاسخ را اندازه می‌گیرد.
    """
    start_time = time.time()
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            latency = (time.time() - start_time) * 1000 # Convert to milliseconds
            return {"status": "Online", "latency_ms": round(latency, 2)}
        else:
            return {"status": f"Error {response.status_code}", "latency_ms": None}
    except requests.exceptions.RequestException:
        return {"status": "Offline/Timeout", "latency_ms": None}

def main():
    """
    تابع اصلی برنامه: تمام میرورها را بررسی کرده و گزارش تولید می‌کند.
    """
    results = {}
    best_mirror = None
    min_latency = float('inf')

    print(f"Starting mirror benchmark at {datetime.now()}...")

    for name, url in MIRRORS.items():
        print(f"Testing {name}...")
        result = test_mirror(name, url)
        results[name] = result

        if result["status"] == "Online" and result["latency_ms"] < min_latency:
            min_latency = result["latency_ms"]
            best_mirror = name

    report = {
        "timestamp": str(datetime.now()),
        "best_mirror": best_mirror,
        "lowest_latency_ms": min_latency if best_mirror else None,
        "details": results
    }

    # ذخیره گزارش در فایل JSON
    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\nBenchmark Complete!")
    print(f"Best Mirror: {best_mirror} ({min_latency} ms)")
    print("Full report saved to report.json")

if __name__ == "__main__":
    main()
