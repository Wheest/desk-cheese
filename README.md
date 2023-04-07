<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Wheest/desk-cheese">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Desk Cheese.</h3>

  <p align="center">
    A tool to take periodic webcam photos, and filter humanless ones
  </p>
</div>



## About

I thought it would be interesting to get a timelapse of myself as I wrote my thesis, so I wrote this tool to do just that.
It has a `bash` script (`take_photo.sh`) to take a photograph using the webcam, and saves it as a timestamped image.
The script should be run as a `cronjob`, with an example of how to do that given in the script itself.

Then, there is then a Python script that runs the [YOLOv3 object detection model](https://pjreddie.com/darknet/yolo/) on the images, to see which ones contain a person.
The script saves lists of images that it thinks contains humans and those it doesn't, and caches the inference results so we don't need to repeat.

The final script `create_animated_gif.sh` takes the images and turns them into an animated GIF.

> Why the name?

The tool is intended to run while one is working at one's desk, and "cheese" is [something people say in English to smile when they are being photographed](https://en.wikipedia.org/wiki/Say_cheese).

## Usage

As well as the Python dependencies `tqdm opencv-python numpy`, you also the `imagemagick` and `fswebcam` packages.

Edit the `take_photo.sh` script to define where you want to save the files, as well as your working hours.
Add the script as a cronjob.
From that point on, you can just leave it to do its thing.
There's a chance if you have multiple webcams it could take things from the wrong input, so it's worth keeping an eye on that.

## Critique

> Running YOLOv3 with opencv is not the fastest way to do DNN inference

Correct, but it _was_ the quickest from a development perspective.

> The class name you are detecting is `person`

Yeah, it only detects humans (and perhaps not all humans with equal accuracy).
Are all humans persons and are all persons human?
That ain't for this tool to decide.

> If everything was in Python it would probably be more portable

Yeah, but I asked GPT-4 to generate a couple of _a couple of GIF generation functions using `Pillow` and `imageio` and they were just hung.
imagemagick does the job for me.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

### Built With

* [OpenCV](https://opencv.org/)
* [YoloV3](https://pjreddie.com/darknet/yolo/)
* [fswebcam](https://www.sanslogic.co.uk/fswebcam/)
* [imagemagick](https://imagemagick.org/index.php)
