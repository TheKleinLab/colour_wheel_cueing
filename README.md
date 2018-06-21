# colour\_wheel\_cueing

colour\_wheel\_cueing is a set of experiment programs for a study exploring how both endogenous (i.e. voluntary) and exogenous (i.e. reflexive) attention affect the probability that the colour of targets will be perceived and the accuracy with which they are perceived.

Both experiment programs take the form of modified Posner cueing paradigms, except the target stimuli are coloured 'X's that participants must then indicate the colour of on an RGB colour wheel using the mouse.

## endo.py

![endo_animation](colwheel_endo.gif)

In the endogenous version of the task, participants are given cues at the center of the screen in the form of numbers/letters that tell them how to direct their attention. An '8' made of lines serves as the fixation stimulus. Attention is cued to the left or right by a removal of lines from the fixation '8' to form a '2' or a '5', with participants being instructed at the onset of the session which number indicated which direction. A removal of lines from the '8' to form an 'H' serves as a neutral cue, which informs participants that a target will appear soon without providing any information as to where it will most likely be.

Spatial cues in this experiment are 80% accurate, meaning that they will inform the participant correctly of the target location more often than not. In addition, 20% of the trials are catch trials, in which no target is presented and participants should make no response. Target onsets always follow cue onsets by an interval of 800 ms. 

The number/direction mapping is set during the demographics collection phase at the start of the session, and should be counterbalanced between participants.


## exo.py

![exo_animation](colwheel_exo.gif)

In the exogenous version of the task, participants are given cues in the form of brief brightenings of one of the three placeholder boxes to direct their spatial attention to the left, right, or middle locations. Targets identical to those presented in **endo.py** are then presented at either the left or right location, which participants must respond to by first pressing the space bar, and then indicating the colour of the target to the best of their ability on an RGB colour wheel.

Spatial cues in this experiment are 50% accurate, meaning that they are completely uninformative about the following target's location. In addition, 20% of the trials are catch trials, in which no target is presented and participants should make no response. Target onsets followed cue onsets by either an interval of 100 ms (short SOA) or 800 ms (long SOA). 

## Requirements

Both experiments are programmed in Python (2.5 to 2.7) using the [pyglet module](https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/). It has been developed and tested on macOS (10.5 through 10.13), but should also work with minimal hassle on computers running Linux or Windows.

This experiment requires no external hardware other than a keyboard and mouse.

## Getting Started

### Installation

First, you will need to install pyglet, which you can do by running `pip install pyglet` in a Terminal window.

Then, you can then download and install the experiment program with the following commands (replacing `~/Downloads` with the path to the folder where you would like to put the program folder):

```
cd ~/Downloads
git clone https://github.com/TheKleinLab/colour_wheel_cueing.git
```

You should also edit the values of the `screen_width` and `viewing_distance` variables near the top of the `exo.py` and `endo.py` files to match your screen, in order to ensure that all stimuli are sized correctly.

### Running the Experiments

To run the endogenous version of the experiment, navigate to the colour\_wheel\_cueing folder in Terminal and run `python endo.py`. To run the exogenous version, navigate to the colour\_wheel\_cueing folder in Terminal and run `python exo.py`.

The data for both versions will be recorded to a folder titled `_Data` in the same folder as the experiment programs, under the subfolders `endo` and `exo`, respectively.

## Acknowledgements

Both experiments were programmed by Mike Lawrence ([@mike-lawrence](https://github.com/mike-lawrence)) under the supervision of Dr. Raymond Klein.