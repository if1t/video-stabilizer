from converter import Converter
from frame_stabilizer import FrameStabilizer

if __name__ == '__main__':
    converter = Converter()
    stabilizer = FrameStabilizer()

    converter.video_to_frames('source/video.mp4', 'source/frames')

    stabilized_frames = stabilizer.stabilizeFrames('source/frames')
    stabilizer.saveStabilizedFrames(stabilized_frames, 'source/stabilized-frames')

    converter.frames_to_video('source/stabilized-frames', 'source/stabilized-video.mp4')
