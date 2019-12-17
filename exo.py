#############################
# Import required libraries #
#############################

import pyglet, math, sys, os, random, time
from pyglet import window, image, font #get the window, image & font/text manipulation commands
from pyglet.window import key
from pyglet.gl import * #get the commands to manipulate graphics
from pyglet.media import Player #get sound player
random.seed()


#######################
# Important constants #
#######################

font_size = 20 #vary this until it looks right on your monitor
computer = 'tracker'
if computer == 'tracker':
    screen_width = 40 #tracker mac mini
elif computer == 'mike':
    screen_width = 37.0 #mike's laptop
elif computer == 'emac':
    screen_width = 33.5 #emac
elif computer == 'eyelink':
    screen_width = 37.5 #eyelink mac mini
viewing_distance = 75.0 #units can be anything so long as they match those used in screen_width

ITI = 1.000 #specify the inter-trial-interval (sec)
fixation_interval = 1.000
cue_duration = 0.050 #specify the cue duration (sec)
target_duration = 0.200 #specify the cue duration (sec)
response_timeout = 1.500
SOA_list = [0.1, 0.8] #list the cue-target stimulus onset asynchrony intervals (sec)
cue_validity_list = ['valid', 'invalid', 'neutral']
target_location_list = [-1, 1]

target_trials_per_cell = 4
catch_trials_per_cell = 1

# trials_per_block = (target_trials_per_cell + catch_trials_per_cell) * len(cue_validity_list) * len(SOA_list) * len(['right','left'])

number_of_blocks = 8 #specify the number of blocks
number_of_sub_blocks = 2 #when the full combination of IVs yields large numbers of trials per block, this lets you put breaks inside the "block". Best to use a factor of the number of trials per block.
num_trials_in_practice_block = 30

box_offset_in_degrees = 7
box_size_in_degrees = 1.5
box_thickness_proportion = .2
target_size_in_degrees = .5
target_thickness_proportion = .1

text_proportion = .9 #the proportion of the screen to use for text messages
dpi = 72 #use 72 for mac, 96 for PC
text_font = 'Helvetica' #use 'Helvetica' for mac, 'Arial' for PC

data_path = os.path.join('_Data', 'exo')


#########################
# Initialize the window #
#########################

#create a pyglet window class that facilitates keypress detection
class my_win(window.Window):
    
    def __init__(self, *args, **kwargs):
        self.response=False
        self.text=""
        self.text_done=False
        self.mouse_pressed=False
        self.mouse_x = 0
        self.mouse_y = 0
        window.Window.__init__(self, *args, **kwargs)
        
    def on_key_press(self, symbol, modifiers):
        self.response=symbol
        self.abs_rt = time.time()
        if symbol==key.ESCAPE:
            sys.exit()
        elif symbol==key.BACKSPACE:
            if len(self.text) < 2:
                self.text=""
            else:
                self.text=self.text[0:-1]
        elif symbol==key.RETURN:
            self.text_done=True
            
    def on_text(self,text):
        self.text = self.text+text
        
    def on_mouse_press(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        self.mouse_pressed=True


win = my_win(fullscreen=True) #make a fullscreen window (happily, highest native resolution is captured by default and double buffering is a default behavior)
win.x_center = win.width/2 #store the location of the horizontal center for later reference
win.y_center = win.height/2 #store the location of the vertical center for later reference
win.set_exclusive_mouse() #ensures the mouse is invisible
glClearColor(0, 0, 0, 0) #set the 'cleared' background to white
cursor = win.get_system_mouse_cursor(win.CURSOR_CROSSHAIR)
win.set_exclusive_mouse(True)
win.set_mouse_cursor(cursor)

win.dispatch_events() #always do a dispatch soon after creating a new window
image.get_buffer_manager().get_color_buffer().get_image_data #necessary (for some reason) to ensure openGL drawing coordinates are in pixels with (0,0) in lower left corner

# Perform some calculations to convert stimulus measurements in degrees to pixels
screen_width_in_degrees = math.degrees(math.atan((screen_width/2.0)/viewing_distance)*2)
PPD = win.width/screen_width_in_degrees
target_size = target_size_in_degrees*PPD
box_offset = box_offset_in_degrees*PPD
box_size = box_size_in_degrees*PPD
wheel_size = box_size*5
target_size = target_size_in_degrees*PPD
text_width = text_proportion*win.width
glLineWidth(target_size*target_thickness_proportion)

color_wheel_inner_rim = math.sqrt(((wheel_size/2.0)**2)+((wheel_size/2.0)**2))
color_wheel_outer_rim = wheel_size


#############################
# Define graphics functions #
#############################

def draw_plus():
    glLineWidth(target_size*target_thickness_proportion)
    glColor3f(.5,.5,.5)
    glBegin(GL_LINE_STRIP)
    glVertex2f(win.x_center,win.y_center-target_size/2.0)
    glVertex2f(win.x_center,win.y_center+target_size/2.0)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex2f(win.x_center-target_size/2.0,win.y_center)
    glVertex2f(win.x_center+target_size/2.0,win.y_center)
    glEnd()

def draw_cross(target_color,location):
    glLineWidth(target_size*target_thickness_proportion)
    glColor3f(target_color[0],target_color[1],target_color[2])
    glBegin(GL_LINE_STRIP)
    glVertex2f(win.x_center+location*box_offset-target_size/2.0,win.y_center-target_size/2.0)
    glVertex2f(win.x_center+location*box_offset+target_size/2.0,win.y_center+target_size/2.0)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex2f(win.x_center+location*box_offset-target_size/2.0,win.y_center+target_size/2.0)
    glVertex2f(win.x_center+location*box_offset+target_size/2.0,win.y_center-target_size/2.0)
    glEnd()

def draw_box(location,cue=False):
    glColor3f(.2,.2,.2)
    if cue:
        glColor3f(1,1,1)
    glRectf(
        win.x_center  + box_offset*location - box_size/2
        ,win.y_center                       - box_size/2
        ,win.x_center + box_offset*location + box_size/2
        ,win.y_center                       + box_size/2
        )
    glColor3f(0,0,0)
    glRectf(
        win.x_center  + box_offset*location - box_size/2 + box_size*box_thickness_proportion/2
        ,win.y_center                       - box_size/2 + box_size*box_thickness_proportion/2
        ,win.x_center + box_offset*location + box_size/2 - box_size*box_thickness_proportion/2
        ,win.y_center                       + box_size/2 - box_size*box_thickness_proportion/2
        )

def draw_cue(cue_validity,target_location):
    if cue_validity=='valid':
        win.clear()
        draw_box(0)
        draw_plus()
        draw_box(target_location,cue=True)
        draw_box(target_location*-1)
    elif cue_validity=='invalid':
        win.clear()
        draw_box(0)
        draw_plus()
        draw_box(target_location)
        draw_box(target_location*-1,cue=True)
    elif cue_validity=='neutral':
        win.clear()
        draw_box(0,cue=True)
        draw_plus()
        draw_box(target_location)
        draw_box(target_location*-1)

def draw_fixation():
    win.clear()
    draw_box(0)
    draw_plus()
    draw_box(-1)
    draw_box(1)

def draw_target(target,target_color,location):
    win.clear()
    draw_box(0)
    draw_plus()
    draw_box(-1)
    draw_box(1)
    if target:
        draw_cross(target_color,location)


####################
# Helper functions #
####################

def angle_to_color(angle,wheel_rotation):
    angle=float(angle)
    if angle < wheel_rotation:
        angle = angle-wheel_rotation+360
    else:
        angle = angle-wheel_rotation
    if angle<60:
        red=1
        green=angle/60
        blue=0
    elif angle < 120:
        red=1-(angle-60)/60
        green=1
        blue=0
    elif angle < 180:
        red=0
        green=1
        blue=(angle-120)/60
    elif angle < 240:
        red=0
        green=1-(angle-180)/60
        blue=1
    elif angle < 300:
        red=(angle-240)/60
        green=0
        blue=1
    else:
        red=1
        green=0
        blue=1-(angle-300)/60
    return [red,green,blue]


def color_to_angle(color,wheel_rotation):
    if color[0]==1:
        if color[2]==0:
            angle = color[1]*60
        else:
            angle = 300 + (1-color[2])*60
    elif color[1]==1:
        if color[2]==0:
            angle = 60 + (1-color[0])*60
        else:
            angle = 120 + color[2]*60
    else:
        if color[0]==0:
            angle = 180 + (1-color[1])*60
        else:
            angle = 240  + color[0]*60
    if angle<wheel_rotation:
        true_angle = angle-wheel_rotation+360
    else:
        true_angle = angle-wheel_rotation
    return true_angle


def mouse_to_angle():
    this_angle = math.atan2(float(win.mouse_x-win.x_center),float(win.mouse_y-win.y_center))*180/math.pi
    if this_angle<0:
        this_angle=360+this_angle
    return this_angle


def draw_color_wheel(wheel_rotation):
    win.clear()
    for angle in range(360):
        this_color = angle_to_color(angle,wheel_rotation)
        glColor3f(this_color[0],this_color[1],this_color[2])
        glBegin(GL_TRIANGLES)
        glVertex2f(win.x_center , win.y_center)
        glVertex2f(
         win.x_center+ math.sin(angle*math.pi/180) * wheel_size
         ,win.y_center + math.cos(angle*math.pi/180) * wheel_size
        )
        glVertex2f(
         win.x_center + math.sin((angle+1)*math.pi/180) * wheel_size
         ,win.y_center + math.cos((angle+1)*math.pi/180) * wheel_size
        )
        glEnd()
    glColor3f(0,0,0)
    for angle in range(360):
        glBegin(GL_TRIANGLES)
        glVertex2f(win.x_center , win.y_center)
        glVertex2f(
         win.x_center + math.sin(angle*math.pi/180) * math.sqrt(((wheel_size/2.0)**2)+((wheel_size/2.0)**2))
         ,win.y_center + math.cos(angle*math.pi/180) * math.sqrt(((wheel_size/2.0)**2)+((wheel_size/2.0)**2))
        )
        glVertex2f(
         win.x_center + math.sin((angle+1)*math.pi/180) * math.sqrt(((wheel_size/2.0)**2)+((wheel_size/2.0)**2))
         ,win.y_center + math.cos((angle+1)*math.pi/180) * math.sqrt(((wheel_size/2.0)**2)+((wheel_size/2.0)**2))
        )
        glEnd() 


def clicked_within_wheel():
    x=win.mouse_x-win.x_center
    y=win.mouse_y-win.y_center
    h = math.sqrt((x**2)+(y**2))
    return (h<color_wheel_outer_rim) & (h>color_wheel_inner_rim)


#define a function that checks if a file exists
def file_exists(f):
    try:
        file = open(f)
    except IOError:
        exists = 0
    else:
        exists = 1
    return exists


#define a function that waits for a given duration to pass
def wait(duration):
    start = time.time()
    while time.time() <= (start + duration):
        win.dispatch_events()


def wait_for_response():
    win.response = False
    while not win.response:
        win.dispatch_events()
    win.response = False


#define a function that prints a message on the screen while looking for user input to continue. The function returns the total time it waited
def show_message(text):
    wait_start = time.time()
    win.clear()
    win.flip()
    win.clear()
    rendered_text = pyglet.text.Label(
        text, text_font, font_size, multiline=True, width=win.width*text_proportion, x=win.width//2,   
        y=win.height//2, anchor_x='center', anchor_y='center', color=[200,200,200,255]
    )
    rendered_text.draw()
    wait(.5)
    win.flip()
    win.response=False
    done=False
    while not done:
        win.dispatch_events()
        if win.response:
            done=True
    win.response=False
    win.flip()
    win.clear()
    wait(.5)
    return time.time()-wait_start


#define a function that prints a feedback message on the screen for a specified amount of time.
def show_feedback(text):
    win.clear()
    rendered_text = pyglet.text.Label(
        text, text_font, font_size, x=win.width//2, y=win.height//2,
        anchor_x='center', anchor_y='center',  color=[200,200,200,255]
    )
    rendered_text.draw()
    win.flip()
    draw_fixation()
    wait_start = time.time()
    wait_end = wait_start + feedback_duration
    while time.time() < wait_end:
        win.dispatch_events()
    win.flip()
    win.response=False


#define a function that helps get_input (below) render an input request and user input to screen.
def input_message(text,location=0):
    rendered_text = pyglet.text.Label(
        text, text_font, font_size, x=win.width//2, y=win.height//2,
        anchor_x='center', anchor_y='center', color=[200,200,200,255]
    )
    if location != 0:
        rendered_text = pyglet.text.Label(
            text, text_font, font_size, x=win.width//2, y=(win.height//2)-50,
            anchor_x='center', anchor_y='center', color=[200,200,200,255]
        )
    rendered_text.draw()


#define a function that requests user input
def get_input(get_what):
    win.text=''
    win.clear()
    win.flip()
    wait(.5)
    win.text_done=False
    while not win.text_done:
        win.dispatch_events()
        win.clear()
        input_message(get_what)
        input_message(win.text,1)
        win.flip()
    text_to_return = win.text[0:-1]
    win.text = ""
    return text_to_return


#define a function that obtains subject info via user input
def get_sub_info():
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    done = False #set done as false in order to enter the loop
    while not done:
        done = True #set done as true then change if we find an existing file
        id = get_input('ID (\'test\' to demo):')
        if id != 'test':
            existing_files=os.listdir(data_path)
            for this_file in existing_files:
                if id==this_file.rsplit('_')[0]:
                    win.clear()
                    overwrite_id = get_input('Oops! ID already exists! Do you really want to overwrite the existing data? (y or n)')
                    if overwrite_id == 'n':
                        done=False
    if id != 'test':
        age = get_input('Age (2-digit number):')
        gender = get_input('Gender (m or f):')
        handedness = get_input('Handedness (r or l):')
    else:
        age='test'
        gender='test'
        handedness='test'
    year = time.strftime('%Y')
    month = time.strftime('%m')
    day = time.strftime('%d')
    hour = time.strftime('%H')  
    sub_info = [id, age, gender, handedness, year, month, day, hour, computer]
    return sub_info


#define a function that initializes the data file
def initialize_data_file(): 
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    data_file_name = os.path.join(data_path, sub_info[0]+'.txt')
    data_file  = open(data_file_name, 'w')
    header ='\t'.join([
        'id', 'age', 'gender', 'handedness', 'year', 'month', 'day', 'hour', 'computer', 'block',
        'trial', 'cue_validity', 'SOA', 'target', 'target_location', 'rt', 'pre_target_response',
        'wheel_rotation', 'target_angle', 'response_angle'
    ])
    data_file.write(header+'\n')    
    return data_file


#define a function that generates a randomized list of trial-by-trial stimulus information representing a factorial combination of the independent variables.
def get_trials():
    target_list = []
    for i in range(target_trials_per_cell):
        target_list.append(True)
    for i in range(catch_trials_per_cell):
        target_list.append(False)
    trials=[]
    for cue_validity in cue_validity_list:
        for SOA in SOA_list:
            for target_location in target_location_list:
                for target in target_list:
                    wheel_rotation = random.uniform(0,360)
                    target_angle = random.uniform(0,360)
                    trials.append([
                        cue_validity, SOA, target_location,
                        target, wheel_rotation, target_angle
                    ])
    random.shuffle(trials)
    return trials


#define a function that runs a block of trials
def run_block(block):
    if block=='practice':
        trials = get_trials()[0:num_trials_in_practice_block]
        sub_block_split = len(trials)
    else:
        trials = get_trials()
        sub_block_split = len(trials)/number_of_sub_blocks
    trial_num = 1
    win.clear()
    draw_plus()
    win.flip()
    win.clear()
    draw_fixation()
    wait(ITI)
    for trial in trials:
        win.flip()
        trial_start_time = time.time()
        cue_validity = trial[0]
        SOA = trial[1]
        target_location = trial[2]
        target = trial[3]
        wheel_rotation = trial[4]
        target_angle = trial[5]
        target_color = angle_to_color(target_angle, wheel_rotation)
        cue_shown = False
        cue_done = False
        target_shown = False
        target_done = False
        pre_target_response = 'FALSE' #R format logical
        ITI_response = 'FALSE' #R format logical
        trial_done=False
        cue_on_time = trial_start_time + fixation_interval
        cue_off_time = cue_on_time + cue_duration
        target_on_time = cue_on_time + SOA
        target_off_time = target_on_time + target_duration
        response_timeout_time = target_on_time + response_timeout
        draw_cue(cue_validity, target_location) #buffer cue screen
        while not trial_done:
            now = time.time()
            if not cue_shown:
                if now >= cue_on_time:
                    win.flip()
                    cue_shown = True
                    draw_fixation() #buffer fixation
            elif not cue_done:
                if now >= cue_off_time:
                    win.flip() #show fixation
                    cue_done = True
                    draw_target(target,target_color, target_location) #buffer target
            elif not target_shown:
                if now >= target_on_time:
                    win.flip() #show target
                    target_shown = time.time() #record the time that the target is being shown
                    win.clear()
                    draw_fixation() #buffer fixation
            elif not target_done:
                if now >= target_off_time:
                    win.flip() #show fixation
                    target_done = True
            elif now >= response_timeout_time:
                trial_done = True
                rt = 'NA'
            #look for key responses
            win.dispatch_events()
            if win.response:
                if target_shown==False:
                    pre_target_response = 'TRUE'
                else:
                    trial_done=True
                    rt = win.abs_rt-target_shown #get the rt relative to the time at which the target was shown
                win.response = False
        if target:
            draw_color_wheel(wheel_rotation)
            win.flip()
            win.set_exclusive_mouse(False)
            response_done = False
            while not response_done:
                win.dispatch_events()
                if win.mouse_pressed:
                    if clicked_within_wheel():
                        response_done = True
                        response_angle = mouse_to_angle()
                        win.mouse_pressed = False
                        win.response = False
            win.set_exclusive_mouse(True)
            win.clear()
            win.flip()
            wait(.5)
        else:
            response_angle = 'NA'
        win.clear()
        draw_plus()
        win.flip()
        win.clear()
        draw_fixation()
        wait(ITI)
        #define trial info to write to file
        trial_info = '\t'.join(map(str, [
            sub_info_for_file, block, trial_num, cue_validity, SOA, target, target_location,
            rt, pre_target_response, wheel_rotation, target_angle, response_angle
        ]))
        data_file.write(trial_info+'\n')
        if trial_num%sub_block_split ==0:
            if block =='practice':
                show_message('You\'re all done the practice phase of this experiment.\n\nWhen you are ready, press any key to continue to the experiment.')
            else:
                show_message('Take a break!\n\nWhen you are ready, press any key to continue the experiment.')
            if trial_num != len(trials):
                win.clear()
                draw_plus()
                win.flip()
                win.clear()
                draw_fixation()
                wait(ITI)           
        #reset the response and iterate the trial counter
        win.response=False      
        trial_num = trial_num + 1   


######################
# Run the experiment #
######################

#get subject info
sub_info = get_sub_info()
sub_info_for_file = '\t'.join(map(str,sub_info))

#initialize the data file
data_file = initialize_data_file()

win.clear()
draw_fixation()
win.flip()
wait_for_response()
# show_message('Press any key to begin practice.')
run_block('practice')

for i in range(number_of_blocks):
    block = i+1
    run_block(block)

show_message('You\'re all done!\n\nPlease alert the person conducting this experiment that you have finished.')
win.close()
sys.exit()
