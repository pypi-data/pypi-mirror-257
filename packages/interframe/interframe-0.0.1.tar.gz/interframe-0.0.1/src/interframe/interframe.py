import argparse
import math
from datetime import datetime
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import mediapy as media

class Interpolator:
    def __init__(self, align = 64):
        self._model = hub.load('https://tfhub.dev/google/film/1')
        self._align = align

    def _pad_to_align(self, x):
        height, width = x.shape[-3:-1]
        height_to_pad = (self._align - height % self._align) if height % self._align != 0 else 0
        width_to_pad = (self._align - width % self._align) if width % self._align != 0 else 0
        bbox_to_pad = {
            'offset_height': height_to_pad // 2,
            'offset_width': width_to_pad // 2,
            'target_height': height + height_to_pad,
            'target_width': width + width_to_pad
        }
        padded_x = tf.image.pad_to_bounding_box(x, **bbox_to_pad)
        bbox_to_crop = {
            'offset_height': height_to_pad // 2,
            'offset_width': width_to_pad // 2,
            'target_height': height,
            'target_width': width
        }
        return padded_x, bbox_to_crop

    def __call__(self, x0, x1, dt):
        if self._align is not None:
            x0, bbox_to_crop = self._pad_to_align(x0)
            x1, _ = self._pad_to_align(x1)

        inputs = {'x0': x0, 'x1': x1, 'time': dt[..., np.newaxis]}
        result = self._model(inputs, training=False)
        image = result['image']

        if self._align is not None:
            image = tf.image.crop_to_bounding_box(image, **bbox_to_crop)
        return image.numpy()

def frame_generator(frame1, frame2, num_recursions, interpolator):
    if num_recursions == 0:
        yield frame1
    else:
        time = np.full(shape=(1,), fill_value=0.5, dtype=np.float32)
        mid_frame = interpolator(np.expand_dims(frame1, axis=0), np.expand_dims(frame2, axis=0), time)[0]
        yield from frame_generator(frame1, mid_frame, num_recursions - 1, interpolator)
        yield from frame_generator(mid_frame, frame2, num_recursions - 1, interpolator)

def interpolate(frames, num_recursions):
    interpolator = Interpolator()
    num_input_frames = len(frames)
    for i in range(1, num_input_frames):
        yield from frame_generator(frames[i - 1], frames[i], num_recursions, interpolator)
    yield frames[-1]

def read_frame(path):
    raw_frame_data = tf.io.read_file(path)
    decoded_frame = tf.image.decode_image(raw_frame_data, channels=3)
    return tf.cast(decoded_frame, dtype=tf.float32).numpy() / float(np.iinfo(np.uint8).max)

def required_arg_length(nmin,nmax):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin<=len(values)<=nmax:
                msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest,nmin=nmin,nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength

def main():
    parser = argparse.ArgumentParser(
        prog='interframe',
        description='Interpolates between two or more images'
    )
    parser.add_argument('-i', '--input', nargs='+', type=str, action=required_arg_length(2, math.inf), required=True, help='Paths for two or more input images')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output directory')
    parser.add_argument('-n', '--num_recursions', type=int, default=3, help='Number of recursions for interpolating between frames')
    parser.add_argument('--save_video', action='store_true', help='Save the output as a video')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for the output video')
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        exit()

    input_frames = [read_frame(frame) for frame in args.input]
    output_frames = list(interpolate(input_frames, args.num_recursions))

    base_name = datetime.isoformat(datetime.now(), timespec='seconds')

    if args.save_video:
        media.write_video(f'{args.output}/{base_name}.mp4', output_frames, fps=args.fps)
    else:
        for i, frame in enumerate(output_frames):
            media.write_image(f'{args.output}/{base_name}_{i}.png', frame)


if __name__ == '__main__':
    main()
