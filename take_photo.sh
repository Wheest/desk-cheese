#!/bin/bash
# Takes a photo if the time is between a given range
# and saves the image to a directory, with the file named
# after the timestamp.
# To automate it, add it as a cronjob by running `crontab -e` and adding the line
# */20 * * * * bash ${path_to_script}/take_photo.sh
# Which will make it take a picture every 20 mins, which can be adjusted as needed
# You will need the fswebcam package

BASE_DIR="/home/pez/Pictures/thesis/pics/"
TIME_LOWER_BOUND="08:00:00"
TIME_UPPER_BOUND="19:00:00"
CURRENT_DAY=$(date +%u)

# Check if today is between Monday and Saturday
if [[ $CURRENT_DAY -ge 1 && $CURRENT_DAY -le 6 ]]; then
  CURRENT_TIME=$(date +%T)
  SECONDS_LOWER=$(date -d $TIME_LOWER_BOUND +%s)
  SECONDS_UPPER=$(date -d $TIME_UPPER_BOUND +%s)
  SECONDS_CURRENT=$(date -d $CURRENT_TIME +%s)

  # Check if the current time is between the defined range
  if [[ $SECONDS_CURRENT -ge $SECONDS_LOWER && $SECONDS_CURRENT -le $SECONDS_UPPER ]]; then
    TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)
    FILENAME="$BASE_DIR/$TIMESTAMP.jpg"

    # Take 3 photos with a 2-second delay and save the last one
    for i in {1..3}; do
      if [ "$i" -eq 3 ]; then
        fswebcam -r 1280x720 --no-banner $FILENAME
      else
        fswebcam -r 1280x720 --no-banner - >/dev/null 2>&1
        sleep 0.1
      fi
    done
  fi
fi
