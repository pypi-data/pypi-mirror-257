#!/usr/bin/env python3
import os
import subprocess
import requests
from zipfile import ZipFile

hosting = None  # Inisialisasi hosting sebagai variabel global

def fetch_hosting_info():
    global hosting
    hosting = requests.get('https://raw.githubusercontent.com/Azigaming404/Autoscript-by-azi/main/domain').text.strip()

def check_permission(my_ip):
    izin = subprocess.getoutput(f'curl -sS http://{hosting}/Autoscript-by-azi-main/izin | awk \'{{print $4}}\' | grep {my_ip}')
    return my_ip == izin

def install_dependencies():
    os.system('apt update && apt upgrade -y')
    os.system('apt install python3 python3-pip -y')
    os.system('apt install sqlite3 -y')
    os.makedirs('/media/.private/', exist_ok=True)
    os.chdir('/media/.private/')
    os.system(f'wget http://{hosting}/Autoscript-by-azi-main/botssh/defencybervpn.zip')
    with ZipFile('defencybervpn.zip', 'r') as zip_ref:
        zip_ref.extractall('cybervpn')
    os.chdir('cybervpn')
    os.system('pip3 install -r requirements.txt')
    os.system('pip install pillow')
    os.system('pip install speedtest-cli')
    os.system('pip3 install aiohttp')
    os.system('pip3 install paramiko')

def input_data():
    azi = open('/root/nsdomain').read().strip()
    domain = open('/etc/xray/domain').read().strip()
    admin = input("[*] Input Your Id Telegram: ")
    token = input("[*] Input Your bot Telegram: ")
    user = input("[*] Input username Telegram: ")
    with open('/media/.private/cybervpn/var.txt', 'w') as f:
        f.write(f'ADMIN="{admin}"\nBOT_TOKEN="{token}"\nDOMAIN="{domain}"\nDNS="{azi}"\nPUB="7fbd1f8aa0abfe15a7903e837f78aba39cf61d36f183bd604daa2fe4ef3b7b59"\nOWN="{user}"\nSALDO="100000"')

def display_completion_message(token, admin, domain):
    os.system('clear')
    print("Done")
    print("Your Data Bot")
    print("===============================")
    print(f"Api Token     : {token}")
    print(f"ID            : {admin}")
    print(f"DOMAIN        : {domain}")
    print("===============================")
    print("Setting done")

def create_nenen_script():
    with open('/usr/bin/nenen', 'w') as f:
        f.write('#!/usr/bin/env python3\n\ncd /media/.private\npython3 -m cybervpn')
    os.system('chmod +x /usr/bin/nenen')

def download_assets_and_setup_services():
    os.system('wget -q -O /usr/bin/enc "https://raw.githubusercontent.com/cyVPN/Azerd/ABSTRAK/enc/encrypt" ; chmod +x /usr/bin/enc')
    os.system('enc /usr/bin/nenen')
    os.system('rm -f /usr/bin/nenen~')
    os.system('rm -f /media/cybervpn.session')
    os.system('systemctl restart cybervpn')
    os.system('chmod 777 /usr/bin/nenen')

def write_cybervpn_service_file():
    cybervpn_service_content = '''[Unit]
Description=Simple CyberVPN - @CyberVPN
After=network.target

[Service]
WorkingDirectory=/root
ExecStart=/usr/bin/nenen
Restart=always

[Install]
WantedBy=multi-user.target
'''
    with open('/etc/systemd/system/cybervpn.service', 'w') as f:
        f.write(cybervpn_service_content)

def reload_and_start_cybervpn_service():
    os.system('systemctl daemon-reload')
    os.system('systemctl start cybervpn')
    os.system('systemctl enable cybervpn')

def download_additional_assets():
    os.system('wget -q -O /usr/bin/panelbot "http://{}/Autoscript-by-azi-main/botssh/panelbot.sh" && chmod +x /usr/bin/panelbot'.format(hosting))
    os.system('wget -q -O /usr/bin/addnoobz "http://cybervpn.serv00.net/Autoscript-by-azi-main/botssh/addnoobz.sh" && chmod +x /usr/bin/addnoobz')
    os.system('wget -q -O /media/.private/log-install.txt "http://cybervpn.serv00.net/Autoscript-by-azi-main/botssh/log-install.txt"')

    download_scripts = [
        'add-vless', 'addtr', 'addws', 'addss', 'cek-ssh', 'cek-ss', 'cek-tr', 'cek-vless', 'cek-ws',
        'del-vless', 'cek-noobz', 'deltr', 'delws', 'delss', 'renew-ss', 'renewtr', 'renewvless', 'renewws',
        'cek-mws', 'cek-mvs', 'cek-mss', 'cek-mts'
    ]

    for script in download_scripts:
        os.system(f'wget -q -O /usr/bin/{script} "http://{hosting}/Autoscript-by-azi-main/botssh/{script}.sh" && chmod +x /usr/bin/{script}')

def main():
    global hosting
    fetch_hosting_info()

    my_ip = get_public_ip()

    if check_permission(my_ip):
        print("IZIN DI TERIMA!!")
    else:
        os.system('clear')
        os.system('figlet "Akses di tolak!! Benget sia hurung!!" | lolcat')
        exit(0)

    install_dependencies()
    input_data()
    display_completion_message(admin, token, domain)
    create_nenen_script()
    download_assets_and_setup_services()
    write_cybervpn_service_file()
    reload_and_start_cybervpn_service()
    download_additional_assets()

    print("Installations complete, type /menu on your bot")

    # Cleanup
    os.system('rm /media/.private/cybervpn.zip')

if __name__ == "__main__":
    main()

