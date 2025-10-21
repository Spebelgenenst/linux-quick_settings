import tkinter as tk #pip install tk
from tkinter import messagebox
import subprocess
import webbrowser
import requests #pip install requests
from bs4 import BeautifulSoup #pip install beautifulsoup4
import threading
from time import sleep

#settings
WINDOW_SIZE = "500x350"
ALWAYS_ON_TOP = False
BEFORE_QUIT_QUESTION = True
URL_HELP = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" #temp
URL_MINT_VERSION = "https://linuxmint.com/download.php"
URL_CHECK_WIFI = "https://canstein-berlin.de"

#appliCATions (for linux mint cinnamon)
WIFI_SETTINGS = ["cinnamon-settings","network"]
UPDATE_MANAGER = ["mintupdate"] # can be replaced with ["sudo","apt","update"], ["sudo", "apt", "upgrade"]
MOUSE_SETTINGS = ["cinnamon-settings","mouse"]

#colors
FG_TEXT = "black"
BG_TEXT = "pink"
SECOUNDARY_COLOR = "#fc7a84"
BG_WINDOW = "white"
SIZE_TEXT = 18
SIZE_TEXT_SMALL = 12
SIZE_CAT = 10

#text
FONT = "Arial"

TEXT_WINDOW_TITLE = "CAT Menu :3"
TEXT_WIFI_CONNECTION = "Wifi connected to: "
TEXT_LAN_CONNECTION = "Connected to the internet :3"
TEXT_NO_WIFI_CONNECTION = "No wifi connection :c"
TEXT_REFRESH = "refresh"
TEXT_MOUSE_SETTINGS = "mouse/touchpad settings"
TEXT_UPDATE_MANAGER = "update manager"
TEXT_QUIT_MESSAGE = "Are you sure you want to quit? :c"
TEXT_QUIT_TITLE = "Quit?"
TEXT_NEW_MINT_VERSION = "New mint version available!"
TEXT_NO_INTERNET = "No internet connection! please connect to the internet first"
TEXT_LOADING = "Loading..."

CAT= \
"Z ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀\n\
⠀⠀z⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⣼⣿⡗⠀⠀⠀⠀\n\
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀\n\
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀\n\
⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦\n\
⠀⠀⢱⡀⠀⠛⠛⠀⠀⠀⠀⠛⠛⠀⢠⡟⠀⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋\n\
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀\n\
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⢃⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\
⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"

class main_window:
    
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(bg=BG_WINDOW)
        self.window.geometry(WINDOW_SIZE)
        self.window.title(TEXT_WINDOW_TITLE)

        #always on top
        if ALWAYS_ON_TOP:
            self.window.wm_attributes("-topmost", True)

        #help button
        self.help = tk.Button(self.window, text="?", font=(FONT, SIZE_TEXT), fg=FG_TEXT, bg=BG_TEXT, command=self.help)
        self.help.place(width=30,height=30, relx=1.0, rely=0.0, anchor="ne")

        #1. button (temp)
        self.WIFI_SETTINGS = tk.Button(self.window, text=TEXT_LOADING, font=(FONT, SIZE_TEXT), command=self.run_WIFI_SETTINGS, fg=FG_TEXT, bg=BG_TEXT)
        self.WIFI_SETTINGS.pack(pady=10)

        #3. button
        self.UPDATE_MANAGER = tk.Button(self.window, text=TEXT_LOADING, font=(FONT, SIZE_TEXT), command=self.run_UPDATE_MANAGER, fg=FG_TEXT, bg=BG_TEXT)
        self.UPDATE_MANAGER.pack(pady=10)

        #2. button
        self.MOUSE_SETTINGS = tk.Button(self.window, text=TEXT_MOUSE_SETTINGS, font=(FONT, SIZE_TEXT), command=self.run_MOUSE_SETTINGS, fg=FG_TEXT, bg=BG_TEXT)
        self.MOUSE_SETTINGS.pack(pady=10)

        #CAT
        self.CAT = tk.Label(self.window, text=CAT, font=(FONT, SIZE_CAT), fg=SECOUNDARY_COLOR, bg=BG_WINDOW)
        self.CAT.pack(pady=10, side="bottom")

        #refresh tread
        self.refresh_thread = threading.Thread(target=self.refresh_sleep)
        self.refresh_thread.start()

        #start
        self.window.protocol("WM_DELETE_WINDOW", self.before_quit)
        self.window.mainloop()

    def wifi_access_refresh(self):
        try:
            response = requests.get(URL_CHECK_WIFI, timeout=5)
            self.wifi_access = response.status_code == 200

        except:
            self.wifi_access = False

    #get wifi name
    def get_wifi_name(self):
        try:
            result = subprocess.run(["nmcli", "-t", "-f", "active,ssid", "device", "wifi"], capture_output=True, text=True, check=True)
            wifi_name = [line.split(":")[-1] for line in result.stdout.strip().splitlines() if line.startswith("yes")]
        except Exception as e:
            messagebox.showerror(title="ERROR x_x", message=f"ERROR while getting wifi status\n{e}")

        return wifi_name

    def WIFI_SETTINGS_display(self):
        wifi_name = self.get_wifi_name()
        if self.wifi_access:
            if wifi_name:
                self.wifi_access = True
                self.WIFI_SETTINGS_display_text = TEXT_WIFI_CONNECTION + wifi_name[0]
                self.WIFI_SETTINGS_display_color = BG_TEXT
            else:
                self.wifi_access = True
                self.WIFI_SETTINGS_display_text = TEXT_LAN_CONNECTION
                self.WIFI_SETTINGS_display_color = BG_TEXT
            return

        self.wifi_access = False
        self.WIFI_SETTINGS_display_text = TEXT_NO_WIFI_CONNECTION
        self.WIFI_SETTINGS_display_color = SECOUNDARY_COLOR
    
    #mint version
    def get_latest_mint_version(self):
        try:
            response = requests.get(URL_MINT_VERSION)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            latest_version = None
            for title in soup.find_all("title"):
                if "Download Linux Mint" in title.text:  # Anpassungen können nötig sein
                    latest_version = title.text.strip()[20:-13]  # Nächsten Text nach strong abrufen
                    break
        
            return latest_version
        
        except Exception as e:
            messagebox.showerror(title="ERROR x_x", message=f"ERROR while retrieveing Latest mint version\n{e}")

    def get_local_mint_version(self):
        try:
            with open("/etc/lsb-release") as f:
                for line in f:
                    if line.startswith("DISTRIB_RELEASE"):
                        return line.split("=")[1].strip()
                    
        except Exception as e:
            messagebox.showerror(title="ERROR x_x", message=f"ERROR while retrieveing local mint version\n{e}")

    def UPDATE_MANAGER_display(self):
        if self.wifi_access:
            self.mint_update_checked = True

            self.latest_mint_version = self.get_latest_mint_version()
            self.local_mint_version = self.get_local_mint_version()

            if self.latest_mint_version != self.local_mint_version:
                self.UPDATE_MANAGER_display_text = TEXT_NEW_MINT_VERSION + self.latest_mint_version
                self.UPDATE_MANAGER_display_color = SECOUNDARY_COLOR
                return

        else:
            self.mint_update_checked = False

        self.UPDATE_MANAGER_display_text = TEXT_UPDATE_MANAGER
        self.UPDATE_MANAGER_display_color = BG_TEXT
        


    #run appliCATions
    def run_WIFI_SETTINGS(self):
        subprocess.run(WIFI_SETTINGS)
        self.sleep_time = 1

    def run_UPDATE_MANAGER(self):
        subprocess.run(UPDATE_MANAGER)

    def run_MOUSE_SETTINGS(self):
        subprocess.run(MOUSE_SETTINGS)

    #help
    def help(self):
        self.wifi_access_refresh()

        if self.wifi_access:
            webbrowser.open(URL_HELP)
        else:
            messagebox.showinfo(title="Info", message=TEXT_NO_INTERNET)

    def before_quit(self):
        if BEFORE_QUIT_QUESTION:
            reply = messagebox.askyesno(title=TEXT_QUIT_TITLE, message=TEXT_QUIT_MESSAGE)
            if reply:
                self.do_refresh = False
                self.window.destroy()
                exit()


    def refresh_sleep(self):
        self.mint_update_checked = False
        self.do_refresh = True
        self.sleep_time = 1
        while self.do_refresh:
            self.refresh()
            sleep(self.sleep_time)
            self.sleep_time *= 1.5

    def refresh(self):
        self.wifi_access_refresh()

        self.WIFI_SETTINGS_display()
        self.WIFI_SETTINGS.config(text=self.WIFI_SETTINGS_display_text, bg=self.WIFI_SETTINGS_display_color)

        if not self.mint_update_checked and self.wifi_access:
            self.UPDATE_MANAGER_display()
            self.UPDATE_MANAGER.config(text=self.UPDATE_MANAGER_display_text,bg=self.UPDATE_MANAGER_display_color)

if __name__ == "__main__":
    main_window()
