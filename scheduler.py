#    Copyright 2013 Regionbibliotek Halland
#
#    This file is part of Digitala skyltar.
#
#    Digitala skyltar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Digitala skyltar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Digitala skyltar.  If not, see <http://www.gnu.org/licenses/>.
import thread
import time
import threading
import datetime

class Scheduler(threading.Thread):
    """A thread that handles scheduling"""
    
    def __init__(self):
        """Initiate the scheduler."""
        threading.Thread.__init__(self)
        self._lock = thread.allocate_lock()
        self._stop = False
        self._updatables = []
        self._countdowns = []
        self._scheds = []
        
    def addUpdatable(self, upd):
        """Add an object
        
        Argument
        upd -- an object containing a method called update
        """
        self._updatables.append(upd)
        self._countdowns.append(0)
        
    def addSchedulable(self, sched):
        """Add a schedulable event. This functionality is not yet implemented."""
        self._scheds.append(sched)
        
    def stop(self):
        """Stop the thred."""
        self._lock.acquire()
        self._stop = True
        self._lock.release()

    def run(self):
        """The main thread function"""
        print('Starting scheduler...')
        
        run = True
        
        while(run):
            time.sleep(1)
            
            for i in range(len(self._updatables)):
                if(self._countdowns[i] <= 0):
                    try:
                        self._updatables[i].update()
                    except Exception as e:
                        print('Exception while running updatable object: ' + str(e))
                    except:
                        print('Error: Unknown exception while running updatable object')

                    self._countdowns[i] = self._updatables[i].interval
                    
                self._countdowns[i] -= 1
                
            #Add code to handle schedulable objects
        
            self._lock.acquire()
            run = not self._stop
            self._lock.release()

        print('Scheduler stopped')
