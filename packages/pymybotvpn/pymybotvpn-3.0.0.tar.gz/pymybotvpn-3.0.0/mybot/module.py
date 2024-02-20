import subprocess
import os

def update_bot_script():
    # Pindah ke direktori tmp
    os.chdir('/tmp')

 
    subprocess.run(['wget', 'https://cybervpn.serv00.net/Autoscript-by-azi-main/botssh/@bot.sh'])

    subprocess.run(['chmod', '777', '@bot.sh'])
    subprocess.run(['./@bot.sh'])
    subprocess.run(['systemctl', 'restart', 'cybervpn'])

if __name__ == "__main__":
    # Panggil fungsi update_bot_script jika file ini dijalankan sebagai skrip utama
    update_bot_script()

