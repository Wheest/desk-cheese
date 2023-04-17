#!/bin/bash

input_directory="${1:-pics}"
duration=50  # in milliseconds

while read -r file_list; do
  input_file="${input_directory}/${file_list}"
  output_file="${input_directory}/${file_list%.*}.gif"


  if [ -f "$input_file" ]; then
    echo "Creating animated GIF $output_file from $input_file."

    images=()
    while read -r image; do
      images+=("${input_directory}/${image}")
    done < "${input_file}"

    convert -delay "${duration}" -loop 0 -dispose Background "${images[@]}" "${output_file}"
  else
    echo "File $input_file does not exist."
  fi
done < <(echo -e "human.txt\nnon_human.txt")
