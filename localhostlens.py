
import platform
import socket
import subprocess


def run_command(command):
    """Run a system command and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return None

        return result.stdout

    except (OSError, subprocess.SubprocessError):
        return None


def get_computer_name():
    """Get the computer's hostname."""
    try:
        return socket.gethostname()
    except OSError:
        return None


def get_ip_address():
    """Get the computer's local IP address."""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    except (socket.gaierror, OSError):
        return None


def get_windows_gateway():
    """Get the default gateway on Windows."""
    output = run_command(["ipconfig"])

    if not output:
        return None

    for line in output.splitlines():
        if "Default Gateway" in line:
            gateway = line.split(":", 1)[1].strip()

            if gateway:
                return gateway

    return None


def get_macos_gateway():
    """Get the default gateway on macOS."""
    output = run_command(["route", "-n", "get", "default"])

    if not output:
        return None

    for line in output.splitlines():
        if "gateway:" in line:
            gateway = line.split(":", 1)[1].strip()

            if gateway:
                return gateway

    return None


def get_windows_dns():
    """Get DNS servers on Windows."""
    output = run_command(["ipconfig", "/all"])

    if not output:
        return None

    dns_servers = []

    for line in output.splitlines():
        if "DNS Servers" in line:
            dns = line.split(":", 1)[1].strip()

            if dns:
                dns_servers.append(dns)

    if dns_servers:
        return ", ".join(dns_servers)

    return None


def get_macos_dns():
    """Get DNS servers on macOS."""
    output = run_command(["scutil", "--dns"])

    if not output:
        return None

    dns_servers = []

    for line in output.splitlines():
        if "nameserver[" in line:
            dns = line.split(":", 1)[1].strip()

            if dns and dns not in dns_servers:
                dns_servers.append(dns)

    if dns_servers:
        return ", ".join(dns_servers)

    return None


def get_gateway():
    """Get the default gateway for the current operating system."""
    operating_system = platform.system()

    if operating_system == "Windows":
        return get_windows_gateway()

    elif operating_system == "Darwin":
        return get_macos_gateway()

    return None


def get_dns_server():
    """Get the DNS server for the current operating system."""
    operating_system = platform.system()

    if operating_system == "Windows":
        return get_windows_dns()

    elif operating_system == "Darwin":
        return get_macos_dns()

    return None


def check_internet_connection():
    """Check whether the computer can reach the internet."""
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=3):
            return True

    except (socket.timeout, OSError):
        return False


print()
print("======================================================================================")
print("Your Local Host Lens is a lightweight network information tool built with Python")
print("======================================================================================")
#print()

name = input("Enter your name(any name): ")
print()

print(f"Hey {name}, here is your computer's information:")
#print("==================================================")
print()


operating_system = platform.system()

if operating_system == "Windows":
    operating_system_name = "Windows"

elif operating_system == "Darwin":
    operating_system_name = "macOS"

else:
    operating_system_name = operating_system

print(f"Operating System: {operating_system_name}")



pc = get_computer_name()

if pc:
    print(f"Your Computer: {pc}")
else:
    print("Your Computer: Unable to determine computer name")



ip = get_ip_address()

if ip:
    print(f"IP Address: {ip}")
else:
    print("IP Address: Unable to determine IP address")



gateway = get_gateway()

if gateway:
    print(f"Default Gateway: {gateway}")
else:
    print("Default Gateway: Not found")



dns = get_dns_server()

if dns:
    print(f"DNS Server: {dns}")
else:
    print("DNS Server: Not found")


print()



if check_internet_connection():
    print("Internet: Connected")
else:
    print("Internet: No Connection")


print()

print("========================================")
print("Follow my journey:")
print()

print("LinkedIn: https://www.linkedin.com/in/eghogho-binitie-647888260/")
print("GitHub: https://github.com/eghoghobinitie/")
print("========================================")
print()

input("\nPress Enter to exit...")