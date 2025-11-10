from TimeRecorder.RecorderGUI import RecorderGUI
import json
import os
import datetime
import time

class Recorder:
    def __init__(self, file_name):        
        self.gui = RecorderGUI(self)
        self.root_dir = os.getcwd()
        self.config_file_name = file_name
        
        self.current_weeknumber = datetime.datetime.today().isocalendar()[1]
        self.current_date_f = datetime.datetime.now().strftime("%Y-%m-%d")
        self.current_year = self.current_date_f.split("-")[0]
        self.current_week_dir = ""
        
        self.cached_project_id = None
        self.cached_project_t_start = None
        self.cached_text = None
        
        self.pick_session_file()        
        self.load()
        
    
    # ----------------------------------------------------------    
    def load(self):
        config_file_path = os.path.join(self.root_dir, self.config_file_name)
        
        with open(config_file_path, "r") as file:
            data = json.load(file)
            for project_id, spec in data["projects"].items():
                self.gui.project_buttons[project_id] = spec
    
    # ----------------------------------------------------------                
    def run_gui(self):
        self.gui.run()
    
    # ----------------------------------------------------------                
    def get_session_week_name(self):
        name = f"{self.current_year}_cw{self.current_weeknumber}"
        return name
    
    # ----------------------------------------------------------                
    def get_session_file_name(self):
        return "session" + datetime.datetime.now().strftime("%Y-%m-%d") + ".json"
    
    # ----------------------------------------------------------                
    def ensure_week_dir(self):
        path = os.path.join(self.root_dir, "sessions")
        name = self.get_session_week_name()
        
        self.current_week_dir = os.path.join(path, name)
        
        try:
            os.mkdir(self.current_week_dir)
            return
            
        except FileExistsError as e:
            print(f"Warning: Week dir {name} already exists.")
            return 
        
    # ----------------------------------------------------------                
    def pick_session_file(self):
        # ensure folder is in place 
        self.ensure_week_dir()
        
        # full session file path
        self.session_file = os.path.join(self.current_week_dir, self.get_session_file_name())
        
        try:
            # if it does
            # pick the name of that session file
            # check last block, if it is closed
                # if not, ask user, when it ended
                # fill the timestamp
            # end
            
            file_old = open(self.session_file, "r")
            data_old = json.load(file_old)   
            file_old.close()
                
            print("Continuing previous session from today")
            
            if data_old["blocks"][-1]["t_end"] == None:
                # resume previous session
                self.cached_project_id = data_old["blocks"][-1]["projectId"]
                self.cached_project_t_start = data_old["blocks"][-1]["t_start"]
                self.cached_text = data_old["blocks"][-1]["text"]
                
                #  or ask user when it ended
                # .
                # .
                # .
                
                pass
                
            
        
        except (FileNotFoundError, IndexError) as e:
            # if todays session does not exist
                # go the way the temporary approach is running
                
            file = open(self.session_file, "w")
            file.write("{\"blocks\": []}")
            file.close()
            
            
            
        
        
        #----
        # temporary approach
        # self.session_file = "session" + datetime.datetime.now().strftime("%Y-%m-%d") + ".json"
        # file = open(self.session_file, "w")
        # file.write("{\"blocks\": []}")
        # file.close()
        return
    
    # ----------------------------------------------------------        
    def write_change(self, project_id, file_name="", stop=False):
        print("RECORDER::write_change")
        if not file_name:
            file_name = self.session_file
        
        # print(f"FILENAME: {file_name}")
        # actual timestamp
        timestamp = int(time.time())
        
        # read previous version of file        
        with open(file_name, "r") as file_old:
            data_old = json.load(file_old)   
            file_old.close()
        
        if len(data_old["blocks"]) > 0 and data_old["blocks"][-1]["t_end"] == None:
            data_old["blocks"][-1]["t_end"] = timestamp
            data_old["blocks"][-1]["text"] = self.gui.text_block.get("1.0",'end-1c')
        
        data = {"blocks": data_old["blocks"]}
        
        if not stop:            
            new_block = {
                "t_start": timestamp,
                "t_end": None,
                "projectId": project_id,
                "text": ""
            }    
            data["blocks"].append(new_block)
         
        with open(file_name, "w") as file:
            json.dump(data, file)
            file.close() 
    
    # ----------------------------------------------------------        
    def save_to_last_block(self, value_name, value, write_character):
        
        # read previous version of file        
        with open(self.session_file, "r") as file_old:
            data_old = json.load(file_old)   
            file_old.close()
        
        if len(data_old["blocks"]) > 0 and data_old["blocks"][-1]["t_end"] == None:
            if write_character == "append":
                t_old = data_old["blocks"][-1]["text"]
                data_old["blocks"][-1]["text"] = t_old + str(value)
                
            elif write_character == "write":
                data_old["blocks"][-1]["text"] = str(value)
                
            else:
                print("RECORDER::save_to_last_block - Unknown type of write operation")
                
        with open(self.session_file, "w") as file:
            json.dump(data_old, file)
            file.close()  