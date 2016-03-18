#!/bin/bash
file=(`ls /dev/input/by-id | grep -m 1 "event-joystick"`)

if [ $# -ne 1 ]
  	then
    echo "This script needs just one argument: parameters.py"
else
	echo "Choose between these OPTIONS"
	echo "1 - Visual Recognition - press q to quit"
	echo "2 - Test Monitor - press q to quit"
	echo "3 - Calibration - press q to quit"
	echo "4 - Pre-training - press q to quit"
	echo "5 - Sequence Condition - press q to quit"
	echo "6 - Random Condition - press q to quit"
	echo "7 - Control Condition - press q to quit"
	echo "8 - Rest: start EMG acquisition - press q to quit"
	echo "9 - Show parameters"
	read -p "Choose an OPTION number and press ENTER: " OPTION

	echo "##########################"
	echo "##########################"

	cwd=$(pwd)
    rm -rf ./src/parameters.py
	ln -s $cwd/$1 $cwd/src/parameters.py

	if [ "$OPTION" = "1" ];then
		echo "Visual Recognition"
		./src/visual_recognition.py
	elif [ "$OPTION" = "2" ];then
		echo "Test Monitor"
		./src/visualise_targets.py
	elif [ "$OPTION" = "3" ];then
		echo "Calibration"
		./src/calibration.py "/dev/input/by-id/$file";
	elif [ "$OPTION" = "4" ];then
		echo "Pre-training"
		./src/training.py "/dev/input/by-id/$file";
	elif [ "$OPTION" = "5" ];then
		echo "Sequence Condition"
		./src/joystick_task.py "/dev/input/by-id/$file" 1;
	elif [ "$OPTION" = "6" ];then
		echo "Random Condition"
		./src/joystick_task.py "/dev/input/by-id/$file" 2;
	elif [ "$OPTION" = "7" ];then
		echo "Control Condition"
		./src/joystick_task.py "/dev/input/by-id/$file" 3;
	elif [ "$OPTION" = "8" ];then
		echo "Rest: start EMG acquisition"
		./src/display_rest.py "/dev/input/by-id/$file";
	elif [ "$OPTION" = "9" ];then
		./src/show_parameters.py
	else
		echo 'not coded yet'
	fi

	rm -rf ./src/parameters.py
	rm -rf ./src/*.pyc
fi


date +"%m-%d-%Y"
echo "arnaud.bore@gmail.com"