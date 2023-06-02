**This folder contains our FlexBE states and behavior.** FlexBE is used for a Finite State Machine to model complex robot behavior. The FSM in FlexBE is called a "behavior" and consists of seperate states which we made. here is an overview of what the FSM looks like:

<overview of current FlexBE behavior state>

To use the behavior we made for the Albert robot in FlexBE. FlexBE needs to be installed and our corresponding Behavior and States need to be downloaded.

**The instructions for installing and running FlexBE are as follows:**

**1. install the FlexBE app.** more detailed instructions can be found here: http://philserver.bplaced.net/fbe/download.php.

to install FlexBE run the following commands:

clone the FlexBE repositories
```
cd ~/catkin_ws/src # or alternative workspace name, same folder as cor_mdp_ahold
git clone https://github.com/team-vigir/flexbe_behavior_engine.git
git clone https://github.com/FlexBE/flexbe_app.git
```

clone the FlexBE repository from git containing our states and behaviors (still inside src folder). 

```
git clone git@gitlab.tudelft.nl:cor/ro47007/2023/team-20/albert_flexbe.git 
```

build FlexBE and the Albert simulation

```
cd ~/catkin_ws 
catkin build
source devel/setup.bash
```

**2. Launch the simulation in Gazebo and launch the retail_store_skills.** the action servers used in the FlexBE states are contained retail_store_skills and this folder will first need to be run before the FlexBE behavior can be launched.

launch the simulation
```
roslaunch albert_gazebo albert_gazebo_navigation.launch
```
launch the action servers 
```
roslaunch retail_store_skills load_skills.launch
```

**3. Launch the FlexBE app and load the Albert Behavior model.** 

launch FlexBE app
```
roslaunch Flexbe_app Flexbe_full.launch
```

click on "load behavior" in the "behavior dashboard" menu and load the albert behavior.

go to the "runtime control menu" and click on "Start Execution". the behavior will now be executed and the robot should be following the behavior in the Gazebo simulation.







