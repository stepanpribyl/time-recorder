from tkinter import Tk, Text, INSERT, N, W, E, S, Frame, Button, Label
import time
import datetime
from TimeRecorder.DynamicTableResults import *

####################################
# GUI support functions 
####################################

def validate_int(_input):
    if _input == "":
        return True
    try:
        if 16 > int(_input) > 0:
            return True
        else:
            return False
    except ValueError:
        return False
        
def make_counter():
    count = -1
    def inner():
        nonlocal count
        count += 1
        return count
        
    return inner


####################################
# GUI 
####################################

class RecorderGUI():
    def __init__(self, recorder):
        self.version = "0.2.4"
        
        self.recorder = recorder
        self.root = Tk()
        self.root.title(f"TIME RECORDER {self.version}")
        self.root.resizable(0,0)
        
        self.project_buttons = {}
        self.function_buttons = {}
        
        # important elements
        self.current_project_id = None
        
        # colors
        self.color_btn_f = "grey"
        self.default_bg = "white"
        self.root.tk_setPalette(background=self.default_bg, foreground='black')
        
        # top frames
        self.frame = Frame(self.root)
        
        self.frame_left = Frame(self.frame)
        self.frame_right = Frame(self.frame)
        self.frame_btns_f = Frame(self.frame)
        self.frame_footer = Frame(self.frame)
        
        # children
        self.project_buttons["general"] = {
            "label": "General",
            "color": "white",
            "font-color": "black",
            "projectId": "general",
            "button": Button(self.frame_left, text="GENERAL", bg=self.color_btn_f, fg="black", width=10, font=("Sans", 10, "bold"))
        }
        self.function_buttons["break"] = {
            "button": Button(self.frame_btns_f, text="STOP", bg=self.color_btn_f, width=10, font=("Sans", 10, "bold"))
            }
        self.function_buttons["saveText"] = {
            "button": Button(self.frame_btns_f, text="SAVE TEXT", bg=self.color_btn_f, width=10, font=("Sans", 10, "bold"))
        }
        self.function_buttons["results"] = {
            "button": Button(self.frame_btns_f, text="RESULTS", bg=self.color_btn_f, width=10, font=("Sans", 10, "bold"))
        }
        
        self.frame_footer.rowconfigure(0, weight=1)
        self.frame_footer.columnconfigure(0, weight=1)
        self.frame_footer.columnconfigure(1, weight=1)
        self.version_label = Label(self.frame_footer, text=f"v{self.version}  |  CW {self.recorder.current_weeknumber}")
        self.timer_today_label = Label(self.frame_footer, text=f"Time Today: 0:00:00")
        
        # only adding the READY label here, the text field goes with the project buttons
        self.current_project_label = Label(self.frame_right, text="Ready.", font=("Sans", 15, "bold"))
        self.timer_today_value = 0 # timer of the day
        self.timer_t_start = None
        self.timer_running = False
        self.timer_label = Label(self.frame_right, text="0:00:00", font=("Sans", 10))
        
        
        
        
        
       
    # ----------------------------------------------------------    
    def build_grid(self):
        # layout
        self.frame.grid(row=0, column=0)
        self.frame_left.grid(row=0, column=0, pady=2)
        self.frame_right.grid(row=0, column=1, sticky=N, rowspan=len(self.project_buttons.keys()))
        self.frame_btns_f.grid(row=1, column=0, columnspan=2, pady=5)
        self.frame_footer.grid(row=2, column=0, columnspan=2, sticky=W+E)
        
        self.current_project_label.grid(row=0, column=0, sticky=N+W)
        self.timer_label.grid(row=1, column=0, sticky=W)
        self.text_block.grid(row=2, column=0, sticky=N, columnspan=10)
        
        self.version_label.grid(row=0, column=0, sticky=W)
        self.timer_today_label.grid(row=0, column=1, sticky=E, ipadx=10)
        
        i = make_counter()
        for project_id in self.project_buttons.keys():
            self.project_buttons[project_id].get("button").grid(row=i(), column=0, ipadx=5, padx=2)
        
        i = make_counter()
        for function_id in self.function_buttons.keys():
            self.function_buttons[function_id].get("button").grid(row=0, column=i(), ipadx=5, padx=2)
        
        return  
    
    # ----------------------------------------------------------    
    def add_buttons_project(self):
        for project_id, spec in self.project_buttons.items():
            if spec.get("button") == None:
                # print(spec)
                bg = spec["color"]
                fg = spec["font-color"]
                label = spec["label"]
                self.project_buttons[project_id]["button"] = Button(self.frame_left, text=label, width=10, bg=bg, fg=fg, font=("Sans", 10, "bold"))
        
        # overengineered height of text field
        h = int((len(self.project_buttons.keys())-1.5)*1.7)
        self.text_block = Text(self.frame_right, height=h, width = 25)
        self.text_block.insert(INSERT, ">>")
        
        return
    
    # ----------------------------------------------------------    
    def reset_text(self, init_text=None):
        print()
        self.text_block.delete("1.0", 'end-1c')
        if init_text == None:
            self.text_block.insert(INSERT, ">>")
        else:
            self.text_block.insert(INSERT, init_text)
        return
    
    # ----------------------------------------------------------    
    def update_timer_today(self, delta=0):
        formatted_time = datetime.timedelta(seconds=self.timer_today_value+delta)
        self.timer_today_label.configure(text=f"Time Today: {formatted_time}")
        return
    
    # ----------------------------------------------------------    
    def update_timer(self):
        if self.timer_running:
            delta = int(time.time())-self.timer_t_start
            # self.timer_today_value += delta
            
            self.update_timer_today(delta)
            
            formatted_time = datetime.timedelta(seconds=delta)
            self.timer_label.config(text=formatted_time)
            
            self.root.after(1000, self.update_timer)
            
        return
    
    # ----------------------------------------------------------    
    def run_timer(self, t_start=None):
        if not self.timer_running:
            self.timer_running = True
            if t_start == None:
                self.timer_t_start = int(time.time())
            else:
                self.timer_t_start = t_start
            
            self.update_timer()
        
        # self.timer_today_value = 0
        # self.timer_label.configure(text="0:00:00")
        return
    
    # ----------------------------------------------------------    
    def stop_timer(self):
        # if there already is some value in the timer, add it to th overall counter
        if self.timer_t_start != None and self.timer_running:
            self.timer_today_value += int(time.time()) - self.timer_t_start 
            print(f"Adding {int(time.time()) - self.timer_t_start} seconds to overall time")
        
        self.timer_running = False
        
    
    # ----------------------------------------------------------    
    def reset_timer(self):
        self.timer_label.configure(text="0:00:00")
        return
        
    # ----------------------------------------------------------    
    def enable_all_buttons(self):
        for project_id in self.project_buttons.keys():
            self.project_buttons[project_id]["button"].configure(state="normal")
        return
    
    # ----------------------------------------------------------        
    def disable_button(self, project_id):
        self.project_buttons[project_id]["button"].configure(state="disabled")
        return
    
    # ----------------------------------------------------------        
    def change_colors(self, bg_color, fg_color):
        self.frame_left.configure(bg=bg_color)
        self.frame_right.configure(bg=bg_color)
        self.frame_btns_f.configure(bg=bg_color)
        self.frame.configure(bg=bg_color)
        self.current_project_label.configure(bg=bg_color, fg=fg_color)
        self.timer_label.configure(bg=bg_color, fg=fg_color)
        self.text_block.configure(bg=bg_color, fg=fg_color)
        return
        
    # ----------------------------------------------------------    
    def config_buttons(self):
        self.function_buttons["break"]["button"].configure(command=self.c_button_break)
        self.function_buttons["saveText"]["button"].configure(command=self.c_button_save_text)
        self.function_buttons["results"]["button"].configure(command=self.c_button_results)
            
        for project_id in self.project_buttons.keys():
            self.project_buttons[project_id]["button"].configure(command= lambda p_id=project_id: self.c_button_project(p_id))
            pass
    
        return
    
    # ----------------------------------------------------------    
    def dump_cache(self):
        self.recorder.cached_project_id = None
        self.recorder.cached_project_t_start = None
        self.recorder.cached_text = None
    
    # ----------------------------------------------------------    
    def c_button_break(self):
        self.change_colors(self.default_bg, "black")
        self.current_project_label.configure(text="Ready.")
        
        self.enable_all_buttons()
        self.recorder.write_change(None, stop=True)
        
        self.stop_timer()
        self.reset_timer()
        self.reset_text()
        return
        
    # ----------------------------------------------------------    
    def c_button_save_text(self):
        self.recorder.save_to_last_block("text", self.text_block.get("1.0",'end-1c'), "write")
        return
        
    # ----------------------------------------------------------        
    def c_button_results(self):
        headers = self.recorder.get_week_dirs()
        
        app = DynamicTableApp(headers, self.recorder.sessions_dir)
        app.mainloop()
        
        return
    
    # ----------------------------------------------------------        
    def c_button_project(self, project_id, t_start=None, init_text=None):
        print(f"GUI: c_button_project {project_id}")
        if project_id == None:
            return
        
        # enable all buttons
        self.enable_all_buttons()
        
        # disable project_id button
        self.disable_button(project_id)
        
        # overwrite label
        self.current_project_label.configure(text=self.project_buttons[project_id]["label"])
        
        #
        if self.project_buttons.get(project_id) == None:
            # stop button
            self.change_colors(self.default_bg, "black")
        else:
            bg_color = self.project_buttons.get(project_id)["color"]
            fg_color = self.project_buttons.get(project_id)["font-color"]
            self.change_colors(bg_color, fg_color)
            
            # only write the change if the block is changed right now by user
            if t_start == None:
                self.recorder.write_change(project_id)
                
        # restart timer
        self.stop_timer()
        self.reset_timer()
        self.run_timer(t_start)
        
        # delete text in text field
        self.reset_text(init_text)
        self.dump_cache()
        
        return
        
    # ----------------------------------------------------------     
    def run(self):
        reg_validate = self.root.register(validate_int)
        
        if len(self.project_buttons.keys()) < 2:
            print("run > ERROR: No projects found in config")
            return 0
            
        self.add_buttons_project()
        self.build_grid()
        self.config_buttons()
        
        self.c_button_project(self.recorder.cached_project_id, self.recorder.cached_project_t_start, self.recorder.cached_text)
        
        self.update_timer_today()
        self.root.mainloop()
        return
        
