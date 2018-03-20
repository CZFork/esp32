import time
import traceback
import urequests

class Logfile():
    filename = "log.txt"
    
    def __init__(self):
        self.file = open(Logfile.filename, "a")
        
    def log(self, text):
        self.file.write(str(time.strftime("%Y-%m-%d %H:%M:%S"))+" "+ str("[INFO]") +" "+ str(text) + "\n")
    
    def log_err(self, err):
        trace = traceback.format_exc()
        mes = str(time.strftime("%Y-%m-%d %H:%M:%S"))+" "+ str("[ERROR]") +" "+ str(err) + "\n"
        self.file.write(mes)
        self.post_message(mes)
        
        trace_split = trace.split('\n')
        for trace in trace_split:
            if trace!='':
                mes = str(time.strftime("%Y-%m-%d %H:%M:%S"))+" "+ str("[TRACEBACK]") +" "+ str(trace) + "\n"
                self.file.write(mes)
                self.post_message(mes)
    
    def end(self):
        self.file.close()
        
    def post_message(self, message):
        try:
            URL = 'https://api.telegram.org/bot' 
            TOKEN = '399910911:AAEh2Wv3YWKe1XSOW0hXeBmaJfbp1O4VBlk'
            data = {'offset': 1, 'limit': 0, 'timeout': 0}
            message_data = {
                    'chat_id': 24504089, 
                    'text': message,
                    'parse_mode': 'HTML'
                }

            request = urequests.post(URL+TOKEN +'/sendMessage', data=message_data) 
            
        except Exception as err:
            trace=traceback.format_exc()
            self.log_err(err, trace)