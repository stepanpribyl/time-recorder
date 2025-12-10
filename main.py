from TimeRecorder.Recorder import Recorder

if __name__ == "__main__":
    rec = Recorder("recorder_config.json")
    rec.run_gui()