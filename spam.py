import json
import os
import random
import time
import uuid
import ctypes  # Thư viện đổi tên tiêu đề dòng Tab trên Windows
import requests
from colorama import init, Fore, Style

# Khởi tạo thư viện màu sắc Colorama
init(autoreset=True)

URL = "https://acchm.miniworldgame.com:14100/auth/login/web/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
]

# Bộ đếm số lần đã loop đăng nhập thành công/thất bại
total_attempts = 0
success_attempts = 0
fail_attempts = 0

def update_window_title():
    """Hàm cập nhật tiêu đề dòng Tab trên cùng của cửa sổ ứng dụng"""
    global total_attempts, success_attempts, fail_attempts
    title_text = f"Tổng Số Lần Thử: {total_attempts} | Thành Công: {success_attempts} | Thất Bại: {fail_attempts} | Developer By IsSaiPho"
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(title_text)
    except Exception:
        pass

def check_login(uin, passwd):
    random_device = "WEB" + uuid.uuid4().hex[:32]
    
    payload = {
        "attach": {
            "env": "10",
            "device_id": random_device,
            "lang": "tha",
            "session_id": random_device,
            "device_plat": 100,
        },
        "mode": "uin",
        "data": {
            "passwd": str(passwd),
            "uin": str(uin),
        },
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://payment.miniworldgame.com",
    }

    try:
        response = requests.post(
            URL, data=json.dumps(payload), headers=headers, timeout=10
        )
        if response.status_code == 200:
            res_data = response.json()
            server_code = res_data.get("code", -1)

            if server_code == 0:
                return True, f"{Fore.GREEN}[+] ĐĂNG NHẬP THÀNH CÔNG!"
            elif server_code == 7012:
                return False, f"{Fore.RED}[-] ĐĂNG NHẬP THẤT BẠI: Sai tài khoản hoặc mật khẩu."
            else:
                server_msg = res_data.get("msg", "Không rõ nguyên nhân")
                return False, f"{Fore.RED}[-] ĐĂNG NHẬP THẤT BẠI: Mã lỗi {server_code} ({server_msg})"
        else:
            return False, f"{Fore.YELLOW}[-] LỖI KẾT NỐI: Server phản hồi mã HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"{Fore.YELLOW}[-] LỖI MẠNG: Không thể kết nối tới server ({e})"

def print_banner():
    """In banner trang trí lúc khởi động phần mềm"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Fore.CYAN}==================================================================
{Fore.GREEN}              TOOL LOOP LOGIN MINI WORLD SINGLE ACCOUNT
{Fore.LIGHTBLUE_EX}                    DEVELOPER BY ISSAIPHO
{Fore.CYAN}==================================================================
    """
    print(banner)

def main():
    global total_attempts, success_attempts, fail_attempts
    
    update_window_title()
    print_banner()

    # Bước 1: Nhập tài khoản (UIN)
    user = input(f"{Fore.LIGHTWHITE_EX}[?] Nhập tài khoản (UIN): ").strip()
    if not user:
        print(f"{Fore.RED}[-] Tài khoản không được để trống!")
        return
    if not user.isdigit():
        print(f"{Fore.RED}[-] Lỗi: UIN phải là một chuỗi số.")
        return

    # Bước 2: Nhập mật khẩu
    password = input(f"{Fore.LIGHTWHITE_EX}[?] Nhập mật khẩu: ").strip()
    if not password:
        print(f"{Fore.RED}[-] Mật khẩu không được để trống!")
        return

    # Bước 3: Nhập thời gian chờ giữa các lần lặp (Delay)
    try:
        delay_input = input(f"{Fore.LIGHTWHITE_EX}[?] Nhập thời gian delay giữa mỗi lần lặp (số giây): ").strip()
        # Nếu nhấn Enter để trống thì mặc định là 5 giây
        delay_time = float(delay_input) if delay_input else 5.0
        if delay_time < 0:
            print(f"{Fore.RED}[-] Thời gian delay không được là số âm. Tự động đổi về 5 giây.")
            delay_time = 5.0
    except ValueError:
        print(f"{Fore.YELLOW}[-] Nhập sai định dạng số. Tự động đặt delay mặc định là 5 giây.")
        delay_time = 5.0

    print(f"\n{Fore.GREEN}[*] Bắt đầu chế độ lặp. Nhấn tổ hợp phím Ctrl + C nếu muốn dừng tool.")
    print(f"{Fore.CYAN}" + "-" * 60)

    # Vòng lặp vô hạn đăng nhập liên tục
    while True:
        try:
            total_attempts += 1
            print(f"{Fore.BLUE}[Lần {total_attempts}] Đang tiến hành đăng nhập tài khoản: {Fore.LIGHTWHITE_EX}{user}...")
            
            # Gửi request đăng nhập
            success, message = check_login(user, password)
            
            print(f"    -> Kết quả: {message}")
            
            if success:
                success_attempts += 1
            else:
                fail_attempts += 1

            # Cập nhật thông số lên tiêu đề Tab cửa sổ
            update_window_title()
            
            print(f"{Fore.LIGHTBLACK_EX}[*] Chờ {delay_time} giây cho lần lặp tiếp theo...")
            print(f"{Fore.CYAN}" + "-" * 40)
            
            # Tạm dừng theo số giây bạn đã nhập
            time.sleep(delay_time)
            
        except KeyboardInterrupt:
            # Xử lý khi người dùng nhấn Ctrl + C để thoát tool một cách an toàn
            print(f"\n{Fore.YELLOW}[!] Đã nhận lệnh dừng tool từ bàn phím!")
            break

    print("\n" + f"{Fore.CYAN}=" * 60)
    print(f"{Fore.GREEN}[*] ĐÃ DỪNG TIẾN TRÌNH LOOP LOGIN!")
    print(f"{Fore.GREEN}[*] TỔNG SỐ LẦN ĐĂNG NHẬP THÀNH CÔNG: {success_attempts}")
    print(f"{Fore.RED}[*] TỔNG SỐ LẦN ĐĂNG NHẬP THẤT BẠI: {fail_attempts}")
    print(f"{Fore.CYAN}=" * 60)
    
    input(f"\n{Fore.LIGHTWHITE_EX}Nhấn Enter để thoát hẳn phần mềm...")

if __name__ == "__main__":
    main()
