
class Progress_data():

    def __init__(self):
    
        self.data ={}
        self.last_refresh_time = None
        self.min_refresh_period = 0.5 # sec
    
    @staticmethod
    def sec_to_hms(seconds):
        return datetime.fromtimestamp(seconds, UTC).strftime('%H:%M:%S') #.%f')[:-3]
    @staticmethod
    def sec_to_hmsms(seconds):
        return datetime.fromtimestamp(seconds, UTC).strftime('%H:%M:%S.%f')[:-3]
        
    @staticmethod
    def get_caller_loop_lenght(self):
        # too difficult todo
        pass
        

pr_d = Progress_data()

def nobar(pr_name, i_max = -1, print_init = False, delete = False, i_start = 1):
    ### init call needed if i_start have default 0 val
    
    # delete
    if delete:
        del pr_d.data[pr_name]
        return

    current_time = time()
    
    # new
    if pr_name not in pr_d.data:
        i_current = i_start
        pr_d.last_refresh_time = current_time
        pr_d.data[pr_name] = {'time_start':current_time, 'time_last':current_time, 'i_current':i_current, 'i_max':i_max}
        # print init
        if i_max > 0 and print_init:
            print(f'{pr_name}  started at {pr_d.sec_to_hms(current_time)}')
            return
        
    # update
    else:
        i_current = pr_d.data[pr_name]['i_current']
        pr_d.data[pr_name]['i_current'] = i_current + 1
        time_last               = pr_d.data[pr_name]['time_last']
        pr_d.data[pr_name]['time_last'] = current_time
        
        # i_max can by updated dynamicaly, but only with larger value
        if i_max > pr_d.data[pr_name]['i_max']:
            pr_d.data[pr_name]['i_max'] = i_max

        pr_i_max = pr_d.data[pr_name]['i_max']
        
        # delete
        if i_current > pr_i_max and pr_i_max > 0:
            del pr_d.data[pr_name]
            return
        
        # skipping too fast print out
        if current_time - pr_d.last_refresh_time < pr_d.min_refresh_period:
            return
            
        # print progress
        pr_d.last_refresh_time = current_time
        time_passed = current_time - pr_d.data[pr_name]['time_start']
        if pr_i_max == -1:
            time_left_str   = 'n/a'
            pr_i_max_str    = 'n/a'
        else:
            time_left       = time_passed / i_current * pr_i_max
            time_left_str   = pr_d.sec_to_hms(time_left)
            pr_i_max_str = str(pr_i_max)
        avg = time_passed / i_current
        print(f' {pr_name}  {i_current} of  {pr_i_max_str}    passed : {pr_d.sec_to_hms(time_passed)}    left: {time_left_str}    avg: {pr_d.sec_to_hmsms(avg)}', end='\r', flush=True if i_current < pr_i_max else False )
    
