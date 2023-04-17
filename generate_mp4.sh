#!/bin/bash

input_directory="${1:-pics}"
duration=0.2  # duration of each frame
root=${PWD}
audio_file="${2:${root}/song.mp3}"

while read -r file_list; do
  cd ${input_directory}
  input_file="${file_list}"
  output_file="${file_list%.*}.mp4"
  compressed_output_file="${file_list%.*}_compressed.mp4"
  audio_output_file="${file_list%.*}_audio.mp4"

  if [ -f "$input_file" ]; then
    echo "Creating MP4 video $output_file from $input_file."

    # Create the list of image files
    images_list=()
    while read -r image; do
      images_list+=("${image}")
    done < "${input_file}"

    # Generate a temporary file with the complete list of image paths
    image_list_file=$(mktemp)
    printf "file '${PWD}/%s'\nduration $duration\n" "${images_list[@]}" > "${image_list_file}"

    echo ${image_list_file}

    # Generate the MP4 video
    # ffmpeg -y -f concat -i %3d.jpg "${framerate}" -c:v libx264 -pix_fmt yuv420p -crf 23 "${output_file}"

    # Compress the MP4 video
    #ffmpeg -i "${output_file}" -vf "scale=iw/2:ih/2" -c:v libx264 -preset slow -crf 30 "${compressed_output_file}"

    # Generate the MP4 video
    ffmpeg -y -f concat -safe 0 -i "${image_list_file}" -vf fps=$framerate -c:v libx264 -pix_fmt yuv420p -crf 23 "${output_file}"

    # Compress the MP4 video
    ffmpeg -y -i "${output_file}" -c:v libx264 -preset slow -crf 30 "${compressed_output_file}"

    # Remove the temporary file
    rm "${image_list_file}"

    # Add audio file
    ffmpeg -y -i "${compressed_output_file}" -i "${audio_file}" -map 0:v -map 1:a -c:v copy -shortest "${audio_output_file}"
  else
    echo "File $input_file does not exist."
  fi
done < <(echo -e "human.txt")
# done < <(echo -e "human.txt\nnon_human.txt")
