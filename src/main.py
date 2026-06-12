import sys
import time
import argparse
from monitor import MirrorMonitor

# لیست میرورهای پیش‌فرض برای تست (مثلاً میرورهای معروف npm یا PyPI)
DEFAULT_MIRRORS = {
    "npm": [
        "https://registry.npmjs.org/",
        "https://registry.npmmirror.com/",  # میرور چین
        "https://mirror.soft98.ir/npm/",    # نمونه میرور داخلی فرضی
    ],
    "pip": [
        "https://pypi.org/pypi",
        "https://pypi.tuna.tsinghua.edu.cn/simple",
        "https://repo.iut.ac.ir/repo/pypi/" # میرور دانشگاه اصفهان
    ]
}

def display_report(manager: str, results: list):
    """نمایش زیبای گزارش در ترمینال"""
    print(f"\n{'='*50}")
    print(f"   MIRROR MONITORING REPORT FOR: {manager.upper()}")
    print(f"{'='*50}")
    print(f"{'Mirror URL':<40} | {'Status':<10} | {'Latency':<10}")
    print(f"{'-'*40}-+-{'-'*10}-+-{'-'*10}")
    
    for r in results:
        latency_str = f"{r['latency_ms']} ms" if r['latency_ms'] != float('inf') else "N/A"
        print(f"{r['url']:<40} | {r['status']:<10} | {latency_str:<10}")
    
    best = results[0]
    if best['latency_ms'] != float('inf'):
        print(f"\n🚀 fastest Mirror: {best['url']} ({best['latency_ms']} ms)")
    else:
        print("\n❌ All mirrors are offline or unreachable!")

def main():
    parser = argparse.ArgumentParser(description="Package Manager Mirror Performance Monitor")
    parser.add_argument("--manager", choices=["npm", "pip"], default="pip", help="Package manager to benchmark")
    parser.add_argument("--interval", type=int, default=0, help="Periodic execution interval in seconds (0 means run once)")
    
    args = parser.parse_args()
    
    mirrors = DEFAULT_MIRRORS.get(args.manager, [])
    monitor = MirrorMonitor(args.manager, mirrors)
    
    if args.interval > 0:
        print(f"🔄 Starting periodic monitor every {args.interval} seconds. Press Ctrl+C to stop.")
        try:
            while True:
                results = monitor.evaluate_all()
                display_report(args.manager, results)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user.")
    else:
        # اجرای تک‌مرتبه‌ای
        results = monitor.evaluate_all()
        display_report(args.manager, results)

if __name__ == "__main__":
    main()
