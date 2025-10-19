import tkinter as tk #pip install tk
import subprocess
from tkinter import messagebox
import webbrowser
import requests #pip install requests
from bs4 import BeautifulSoup #pip install beautifulsoup4

#settings
window_size = "500x350"
always_on_top = False
before_quit_question = True
help_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" #temp
mint_version_url = "https://linuxmint.com/download.php"

#applications (for linux mint cinnamon)
wifi_settings = ["cinnamon-settings","network"]
update_manager = ["mintupdate"] # can be replaced with ["sudo","apt","update"], ["sudo", "apt", "upgrade"]
mouse_settings = ["cinnamon-settings","mouse"]

#colors
text_fg = "black"
text_bg = "pink"
secondary_color = "#fc7a84"
window_bg = "white"
text_size = 18
smal_text_size = 12
cat_size = 10

#text
font = "Arial"

text_window_title = "Cat Menu :3"
text_wifi_connection = "Wifi connected to: "
text_no_wifi_connection = "No wifi connection :c"
text_mouse_settings = "mouse/touchpad settings"
text_update_manager = "update manager"
text_quit_message = "Are you sure you want to quit? :c"
text_quit_title = "Quit?"
text_new_mint_version = "New mint version available!"

cat= \
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
        self.window.configure(bg=window_bg)
        self.window.geometry(window_size)
        self.window.title(text_window_title)

        #always on top
        if always_on_top:
            self.window.wm_attributes("-topmost", True)

        #help button
        self.help = tk.Button(self.window, text="?", font=(font, text_size), fg=text_fg, bg=text_bg, command=self.help)
        self.help.place(width=30,height=30, relx=1.0, rely=0.0, anchor="ne")

        #1. button
        self.wifi_settings_display()

        self.wifi_settings = tk.Button(self.window, text=self.wifi_settings_display_text, font=(font, text_size), command=self.run_wifi_settings, fg=text_fg, bg=self.wifi_settings_display_color)
        self.wifi_settings.pack(pady=10)

        #3. button
        self.update_manager_display()
        
        self.update_manager = tk.Button(self.window, text=self.update_manager_display_text, font=(font, text_size), command=self.run_update_manager, fg=text_fg, bg=self.update_manager_display_color)
        self.update_manager.pack(pady=10)

        #2. button
        self.mouse_settings = tk.Button(self.window, text=text_mouse_settings, font=(font, text_size), command=self.run_mouse_settings, fg=text_fg, bg=text_bg)
        self.mouse_settings.pack(pady=10)

        #cat
        self.cat = tk.Label(self.window, text=cat, font=(font, cat_size), fg=secondary_color, bg=window_bg)
        self.cat.pack(pady=10)

        #start
        self.window.protocol("WM_DELETE_WINDOW", self.before_quit)
        self.window.mainloop()


    #get wifi name
    def get_wifi_name(self):
        try:
            result = subprocess.run(["nmcli", "-t", "-f", "active,ssid", "device", "wifi"], capture_output=True, text=True, check=True)
            wifi_name = [line.split(":")[-1] for line in result.stdout.strip().splitlines() if line.startswith("yes")]
        except Exception as e:
            messagebox.showerror(title="ERROR x_x", message=f"ERROR while getting wifi status\n{e}")

        return wifi_name

    def wifi_settings_display(self):
        wifi_name = self.get_wifi_name()
        if wifi_name:
            self.wifi_access = True
            self.wifi_settings_display_text = text_wifi_connection + wifi_name
            self.wifi_settings_display_color = text_bg
        else:
            self.wifi_access = False
            self.wifi_settings_display_text = text_no_wifi_connection
            self.wifi_settings_display_color = secondary_color
    
    #mint version
    def get_latest_mint_version(self):
        try:
            response = requests.get(mint_version_url)
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

    def update_manager_display(self):

        if self.wifi_access:

            self.latest_mint_version = self.get_latest_mint_version()
            self.local_mint_version = self.get_local_mint_version()

            if self.latest_mint_version != self.local_mint_version:
                self.update_manager_display_text = text_new_mint_version + self.latest_mint_version
                self.update_manager_display_color = secondary_color
                return

        self.update_manager_display_text = text_update_manager
        self.update_manager_display_color = text_bg


    #run applications
    def run_wifi_settings(self):
        subprocess.run(wifi_settings)

    def run_update_manager(self):
        subprocess.run(update_manager)

    def run_mouse_settings(self):
        subprocess.run(mouse_settings)

    def help(self):
        webbrowser.open(help_url)

    def before_quit(self):
        if before_quit_question:
            reply = messagebox.askyesno(title=text_quit_title, message=text_quit_message)
            if reply:
                self.window.destroy()



if __name__ == "__main__":
    main_window()
