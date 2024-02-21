
import os
def install_vim():
    print("Installing Vim...")
    os.system("sudo apt install vim")    
def install_default():
    print("Installing default...")  

def install_hotspot():
    print("Installing hotspot...")
def install_hello():
    os.system("sudo snap install hello")
def install_snapd():
    print("Installing snapd...")
    os.system("sudo mv /etc/apt/preferences.d/nosnap.pref ~/Documents/nosnap.backup")
    os.system("sudo apt update")
    os.system("sudo apt install snapd")
#install google-chrome
def install_google_chrome():
    print("Installing google-chrome...")
    os.system("sudo snap install google-chrome")
#install slack
def install_slack():
    print("Installing slack...")
    os.system("sudo snap install slack --classic")
#install vlc
def install_vlc():
    print("Installing vlc...")
    os.system("sudo apt install vlc")
#install zoom
def install_zoom():
    print("Installing zoom...")
    os.system("sudo snap install zoom-client")
#install vscode
def install_vscode():
    print("Installing vscode...")
    os.system("sudo snap install code --classic")
#install postman
def install_postman():
    print("Installing postman...")
    os.system("sudo snap install postman")
#install discord
def install_discord():
    print("Installing discord...")
    os.system("sudo snap install discord")
#install spotify
def install_spotify():
    print("Installing spotify...")
    os.system("sudo snap install spotify")
#install telegram
def install_telegram():
    print("Installing telegram...")
    os.system("sudo snap install telegram-desktop")
#install obs-studio
def install_obs_studio():
    print("Installing obs-studio...")
    os.system("sudo snap install obs-studio")
def install_freetube():
    print("Installing freetube...")
    os.system("sudo snap install freetube")
def install_signal():
    print("Installing signal...")
    os.system("sudo snap install signal-desktop")
def install_brave():
    print("Installing brave...")
    os.system("sudo snap install brave")
def install_firefox():
    print("Installing firefox...")
    os.system("sudo apt install firefox")
def install_youtube_dl():
    print("Installing youtube-dl...")
    os.system("sudo apt install youtube-dl")
def install_qbittorrent():
    print("Installing qbittorrent...")
    os.system("sudo apt install qbittorrent")
def install_pycharm():
    print("Installing pycharm...")
    os.system("sudo snap install pycharm-community --classic")
def install_intellij():
    print("Installing intellij...")
    os.system("sudo snap install intellij-idea-community --classic")
def install_android_studio():
    print("Installing android-studio...")
    os.system("sudo snap install android-studio --classic")
def install_WifiHotspot():
    print("Installing dependencies for Linux WiFi Hotspot...")
    dependencies = "libgtk-3-dev build-essential gcc g++ pkg-config make hostapd libqrencode-dev libpng-dev"
    os.system(f"sudo apt install -y {dependencies}")
    os.system("git clone https://github.com/lakinduakash/linux-wifi-hotspot")
    os.chdir("linux-wifi-hotspot")
    os.system("make")
    os.system("sudo make install")
    os.chdir("..")
    os.system("rm -rf linux-wifi-hotspot")
    print("Done!")


def install_wireshark():
    print("Installing wireshark...")
    os.system("sudo apt install wireshark")

install_functions = {
    "vim": install_vim,
    "google_chrome": install_google_chrome,
    "slack": install_slack,
    "vlc": install_vlc,
    "zoom": install_zoom,
    "vscode": install_vscode,
    "postman": install_postman,
    "discord": install_discord,
    "spotify": install_spotify,
    "telegram": install_telegram,
    "obs_studio": install_obs_studio,
    "freetube": install_freetube,
    "signal": install_signal,
    "brave": install_brave,
    "firefox": install_firefox,
    "youtube_dl": install_youtube_dl,
    "qbittorrent": install_qbittorrent,
    "pycharm": install_pycharm,
    "intellij": install_intellij,
    "android_studio": install_android_studio,
    "WifiHotspot": install_WifiHotspot,
    "wireshark": install_wireshark,
    # Add more mappings for other apps
}

def install_apps(apps_to_install):
    # Add your installation logic here
    if os.system("snap --version") == 1:
        install_snapd()
    
    print("Installing apps:", apps_to_install)
    for app in apps_to_install:
        install_function = install_functions.get(app, install_default)
        install_function()


