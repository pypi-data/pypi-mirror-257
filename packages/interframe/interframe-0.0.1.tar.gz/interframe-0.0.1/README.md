# interframe

Python CLI for generating intermediate image frames by interpolating between input key frames.

## Dependencies

 - [Python 3.x](https://python.org)
 - [numpy/numpy](https://github.com/numpy/numpy)
 - [google/mediapy](https://github.com/google/mediapy)
 - [tensorflow/tensorflow](https://github.com/tensorflow/tensorflow)
 - [tensorflow/hub](https://github.com/tensorflow/hub)

## Installation

```sh
$  pip install interframe
```

## Usage

```
usage: interframe [-h] -i INPUT [INPUT ...] -o OUTPUT [-n NUM_RECURSIONS]
                [--save_video] [--fps FPS]

Interpolates between two or more images

options:
  -h, --help            show this help message and exit
  -i INPUT INPUT [INPUT ...], --input INPUT INPUT [INPUT ...]
                        Paths for two or more input images
  -o OUTPUT, --output OUTPUT
                        Output directory
  -n NUM_RECURSIONS, --num_recursions NUM_RECURSIONS
                        Number of recursions for interpolating
                        between frames
  --save_video          Save the output as a video
  --fps FPS             Frames per second for the output video
```
