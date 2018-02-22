class Pwm():
    
    def __init__(self, pin_mode, time_mode, freq_mode, energy):
        self.pin_mode = pin_mode
        self.freq_mode = freq_mode #частота
        self.energy = int(energy) # from 0 to 1023
        self.obj = machine.PWM(machine.Pin(self.pin_mode), freq=self.freq_mode)
        
    def pulse(self):
        self.obj.duty(int(self.energy))
            