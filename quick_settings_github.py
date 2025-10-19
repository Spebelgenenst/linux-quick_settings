import tkinter as tk
import subprocess
from tkinter import messagebox
import webbrowser

#settings
window_size = "500x350"
always_on_top = False
before_quit_question = True
help_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" #temp

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
        self.window.title("Cat Menu :3")

        #always on top
        if always_on_top:
            self.window.wm_attributes("-topmost", True)

        #help button
        self.help = tk.Button(self.window, text="?", font=("Arial", text_size), fg=text_fg, bg=text_bg, command=self.help)
        self.help.place(width=30,height=30, relx=1.0, rely=0.0, anchor="ne")

        #1. button
        self.wifi_settings = tk.Button(self.window, text=self.get_wifi_info(), font=("Arial", text_size), command=self.run_wifi_settings, fg=text_fg, bg=text_bg)
        self.wifi_settings.pack(pady=10)

        #2. button
        self.mouse_settings = tk.Button(self.window, text="mouse/touchpad settings", font=("Arial", text_size), command=self.run_mouse_settings, fg=text_fg, bg=text_bg)
        self.mouse_settings.pack(pady=10)

        #3. button
        self.update_manager = tk.Button(self.window, text="update manager", font=("Arial", text_size), command=self.run_update_manager, fg=text_fg, bg=text_bg)
        self.update_manager.pack(pady=10)

        #cat
        self.cat = tk.Label(self.window, text=cat, font=("Arial", cat_size), fg=secondary_color, bg=window_bg)
        self.cat.pack(pady=10)

        #start
        self.window.protocol("WM_DELETE_WINDOW", self.before_quit)
        self.window.mainloop()


    #get wifi name
    def get_wifi_info(self):
        result = subprocess.run(["nmcli", "-t", "-f", "active,ssid", "device", "wifi"], capture_output=True, text=True, check=True)
        wifi_name = [line.split(":")[-1] for line in result.stdout.strip().splitlines() if line.startswith("yes")]

        if wifi_name:
            return f"Wifi connected to {wifi_name} :3"
        else:
            return "No wifi connection :c"

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
            reply = messagebox.askyesno(title="Quit?", message="Are you sure you want to quit? :c")
            if reply:
                self.window.destroy()

if __name__ == "__main__":
    main_window()
