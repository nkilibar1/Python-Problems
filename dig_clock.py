# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 09:34:29 2015

@author: nik
"""

from graphics import *
# create the graphics window

new_win = GraphWin("Digital Clock", 270, 110)


class DigitalClock():
    
    def __init__(self, hours, minutes, seconds):
       
        self.seconds_time = hours*3600 + minutes*60 + seconds
        
        self.time2 = converter().convert_toclock(self.seconds_time)
        self.display = converter().ampmformat(self.time2)
        self.pos = Text(Point(132,25), self.display)
        
    def draw(self, win):
        self.pos.draw(win)
        
    def setSize(self, size):
        self.pos.setSize(size)
        
    def animate(self, win):
                 
            
        self.secs4 = converter().convert_toseconds(self.time2)
        self.secs4 += 1
        self.time2 = converter().convert_toclock(self.secs4)
        self.display = converter().ampmformat(self.time2)
        self.pos.setText(self.display)
        win.after(1000, self.animate, win)
    
        
class converter():
    
    def __init__(self):
        pass
        
    def convert_toclock(self, seconds_time):
        
        self.current_hour, self.seconds_remain = divmod(seconds_time, 3600)
        self.current_minute, self.current_second = divmod(self.seconds_remain, 60)
        self.holder = self.current_hour
       
        return "%d:%02d:%02d" % (self.current_hour, self.current_minute, self.current_second)
        
      
    def convert_toseconds(self, time):
        
         self.split_list = time.split(":")         
         self.secs = self.split_list[2].split(" ")
         
         return int(self.split_list[0]) * 3600 + int(self.split_list[1]) * 60 + int(self.secs[0])
         

    def ampmformat (self, hhmmss):
        
        self.ampm = hhmmss.split (":")
        if (len(self.ampm) == 0) or (len(self.ampm) > 3):
            return hhmmss

        self.hour = int(self.ampm[0]) % 24
        self.isam = (self.hour >= 0) and (self.hour < 12)

        if self.isam:
            self.ampm[0] = ('12' if (self.hour == 0) else "%02d" % (self.hour))
        else:
            self.ampm[0] = ('12' if (self.hour == 12) else "%02d" % (self.hour-12))

        return ':'.join (self.ampm) + (' AM' if self.isam else ' PM')
        
       
           
    
        
    
        
clock = DigitalClock(23, 59, 53)
clock.setSize(35)
clock.draw(new_win)
clock.animate(new_win)

new_win.mainloop()
