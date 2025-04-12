import traceback

def log_exception(e: Exception):
    print("❌ Lỗi:", str(e))
    print("📋 Traceback:")
    for line in traceback.format_exc().splitlines():
        if "site-packages" not in line:
            print(line)
