**This folder contains our FlexBE states and behavior.** FlexBE is used for a Finite State Machine to model complex robot behavior. The FSM in FlexBE is called a "behavior" and consists of seperate states which we made. For an overview of what the FSM looks like, see the overview.png picture.

To use the behavior we made for the Albert robot in FlexBE, FlexBE needs to be installed and our corresponding Behavior and States need to be downloaded. This process is explained in the cor_mdp_ahold repository readme.

**The instructions for our behavior model in FlexBE are as follows:**

**IMPORTANT: first follow the README instructions in the cor_mdp_ahold repository. in the cor_mdp_ahold readme are instructions for installing flexBE and the simulation**

**1. Launch the simulation in Gazebo and launch the retail_store_skills.** the action servers used in the FlexBE states are contained retail_store_skills and this folder will first need to be run before the FlexBE behavior can be launched.

launch the simulation
```
roslaunch albert_gazebo albert_gazebo_navigation.launch
```
launch the action servers 
```
roslaunch retail_store_skills load_skills.launch
```

**2. Launch the FlexBE app and load the Albert Behavior model.** 

launch FlexBE app
```
roslaunch Flexbe_app Flexbe_full.launch
```

click on "load behavior" in the "behavior dashboard" menu and load the albert behavior.

go to the "runtime control menu" and click on "Start Execution". the behavior will now be executed and the robot should be following the behavior in the Gazebo simulation.







