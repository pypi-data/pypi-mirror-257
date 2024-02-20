from time import time
from datetime import datetime, timezone 
UTC = timezone.utc

class Progress_data():

    def __init__(self):
        
        # progresses dict collection
        self.d ={}
        
        self.last_print_time = 0.0
        self.min_print_period = 0.5 # sec
        self.current_time       = None
        
        self.bar_txt = None
        
        # self.fill_min_len = 4
    
    @staticmethod
    def sec_to_hms(seconds):
        return datetime.fromtimestamp(seconds, UTC).strftime('%H:%M:%S')

    @staticmethod
    def sec_to_hmsms(seconds):
        return datetime.fromtimestamp(seconds, UTC).strftime('%H:%M:%S.%f')[:-3]

    @staticmethod
    def time_zero_trim(time_str:str, trim_spaces = False):
        n = 0
        for i in range(len(time_str)):
            if time_str[i] in ('0',':',) and time_str[i+1] != '.':
                n += 1
            else:
                break
        if trim_spaces:
            time_str = time_str[n:]
        else:
            time_str = ' ' * n + time_str[n:]
        return time_str
        
    @staticmethod
    def num_len(int_num):
        return len(str(int_num))
        
    def fill_len(self,i_max):
        return self.num_len(i_max)
        # return max(self.num_len(i_max), self.fill_min_len)
        
    def insert(self, pr_name, current_time, i_start, i_max):
    
        self.d[pr_name] = {'time_start':current_time, 'time_last':current_time,'time_passed_prev':current_time, 'i_current':i_start, 'i_max':i_max}
        
    def update(self, pr_name, i_start, i_max):
        
        i_current = self.d[pr_name]['i_current'] + 1
        
        # i_max was changed
        if i_max != -1:
            if i_max > i_current:
                pr.d[pr_name]['i_max'] = i_max
            else:
                print('unable to set Max i smaller then Current i')
        
        # i_start was changed
        if i_start != 1:
            self.d[pr_name]['i_current'] = i_start
        else:
            self.d[pr_name]['i_current'] = i_current
        
        time_last = self.d[pr_name]['time_last']
        
        # calculate time_start for non inititialized, at the second nobar  call 
        if pr.d[pr_name]['i_max'] == -1 and i_current == 2:
            self.d[pr_name]['time_start'] = self.current_time - 2*(self.current_time - time_last)
        
        self.d[pr_name]['time_passed_prev'] = time_last
        self.d[pr_name]['time_last'] = self.current_time
            
    def delete(self, pr_name):
    
        del self.d[pr_name]
        
    def gen_txt_init(self,pr_name):
    
        i_max = self.d[pr_name]["i_max"]
        fill_len = pr.fill_len(i_max)
        self.bar_txt = f'{pr_name}  {" "*(fill_len-1)}0 / {i_max}  pas 00:00:00   lef --:--:--   tot --:--:--   las --:--:--   avg --:--:--'
    
    def gen_txt_first_noninited(self,pr_name):
    
        i_max = self.d[pr_name]["i_max"]
        fill_len = pr.fill_len(i_max)
        self.bar_txt = f'{pr_name}  {" "*(fill_len-1)}1 / {"-"*fill_len}  pas --:--:--   lef --:--:--   tot --:--:--   las -.---   avg -.---'
    
    def gen_txt_upd(self,pr_name):
    
        p = self.d[pr_name]
        
        i_passed            = p["i_current"]
        i_max               = p['i_max']
        time_passed         = p['time_last'] - p['time_start']
        time_passed_str     = self.sec_to_hms(time_passed)

        time_passed_prev    = p['time_passed_prev']
        

        fill_len    = pr.fill_len(i_max)
        len_i       = self.num_len(i_passed)
        fill_len_i  = fill_len - len_i
        fill_len_m  = fill_len - self.num_len(i_max)
        
        
        
        if i_max == -1:
            time_left_str   = '--:--:--'
            time_total_str  = '--:--:--'
            i_max_str       = '-'* len_i
            t_last_str      = '-.---'
            avg_str         = '-.---'
        else:
            time_total          = time_passed / i_passed * i_max
            time_total_str      = self.sec_to_hms(time_total)
            i_max_str           = str(i_max)
            # i_max_str           = ' '*fill_len_m + str(i_max)
            time_left           = time_total - time_passed
            time_left_str      = self.sec_to_hms(time_left)
        t_last_str              = self.time_zero_trim(self.sec_to_hmsms(p['time_last'] - time_passed_prev), trim_spaces = True)
        avg_str = self.time_zero_trim(self.sec_to_hmsms(time_passed / i_passed), trim_spaces = True)
        self.bar_txt = f'{pr_name}   {" "*(fill_len_i)}{i_passed} / {i_max_str}   pas {time_passed_str}   lef {time_left_str}   tot {time_total_str}   las {t_last_str}   avg {avg_str}' # 
        
    def print_init(self,pr_name):
    
        self.gen_txt_init(pr_name)
        self.print_out()
        
    def print_first_noninited(self,pr_name):
    
        self.gen_txt_first_noninited(pr_name)
        self.print_out()
        
    def print_upd(self, pr_name, force_new_line=False):
    
        self.gen_txt_upd(pr_name)
        self.print_out(is_last =  (self.d[pr_name]['i_current']>=self.d[pr_name]['i_max'] and self.d[pr_name]['i_max'] != -1  or force_new_line) )

    def print_out(self, is_last=False):
    
        self.last_print_time = self.current_time
        print(self.bar_txt, end='\r' if not is_last else None, flush=True if is_last else False)
        
    def print_all(self):
    
        # print all passed
        for pr_name in self.d.keys():
            self.gen_txt_upd(pr_name)
            self.print_upd(pr_name, force_new_line=True)

    # reserved
    def get_caller_loop_lenght(self):
        # too hard todo
        pass

pr = Progress_data()

def nobar(pr_name= '', i_max=-1, delete=False, i_start=1, print_all=False):
    
    pr.current_time = time()
    
    # delete
    if delete:
        if pr_name in pr.d:
            pr.delete(pr_name)
            return
        else:
            print('wrong progress name')
            return
            
    # print_all
    if print_all:
        pr.print_all()
        return

    # data
    if pr_name in pr.d:
        # update
        pr.update(pr_name,i_start,i_max)
        # print
        # skipping by refresh rate, except last iteration
        if pr.current_time - pr.last_print_time < pr.min_print_period and pr.d[pr_name]['i_current'] < pr.d[pr_name]['i_max']:
            return
        pr.print_upd(pr_name)

    else:
        # insert (new one)
        
        if i_max >= 0:
            # initialized
            pr.insert(pr_name, pr.current_time, i_start-1, i_max)
            pr.print_init(pr_name)
        else:
            # noninitialized
            pr.insert(pr_name, pr.current_time, i_start, i_max)
            pr.print_first_noninited(pr_name)
        return
