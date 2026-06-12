import time
import requests
from typing import List, Dict, Any

class MirrorMonitor:
    """
    مسئولیت مدیریت و سنجش کارایی میرورهای مختلف را بر عهده دارد.
    """
    def __init__(self, manager_name: str, mirrors: List[str]):
        self.manager_name = manager_name
        self.mirrors = mirrors

    def ping_mirror(self, url: str, timeout: int = 5) -> Dict[str, Any]:
        """
        یک درخواست به میرور ارسال کرده و زمان پاسخ‌دهی و وضعیت آن را می‌سنجد.
        """
        start_time = time.time()
        try:
            # ارسال یک درخواست هدد (HEAD) یا گت کوچک برای بررسی وضعیت
            response = requests.head(url, timeout=timeout)
            latency = (time.time() - start_time) * 1000  # تبدیل به میلی‌ثانیه
            
            if response.status_code < 400:
                return {"url": url, "status": "Online", "latency_ms": round(latency, 2)}
            else:
                return {"url": url, "status": f"Error ({response.status_code})", "latency_ms": float('inf')}
        except requests.RequestException:
            return {"url": url, "status": "Offline", "latency_ms": float('inf')}

    def evaluate_all(self) -> List[Dict[str, Any]]:
        """
        تمام میرورها را بررسی کرده و لیست را بر اساس کمترین تأخیر (سریع‌ترین) مرتب می‌کند.
        """
        results = []
        for mirror in self.mirrors:
            metrics = self.ping_mirror(mirror)
            results.append(metrics)
        
        # مرتب‌سازی صعودی بر اساس Latency (آن‌هایی که خطا دارند آخر می‌روند)
        results.sort(key=lambda x: x["latency_ms"])
        return results
