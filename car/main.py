from converter import Converter
from frame_stabilizer import FrameStabilizer
import modal_player

if __name__ == '__main__':
    # converter = Converter()
    # stabilizer = FrameStabilizer()
    #
    # converter.video_to_frames('source/video.mp4', 'source/frames-10')
    # frames = stabilizer.get_frames_from_path('source/frames-10')
    # stabilized_frames = stabilizer.stabilizeFrames(frames[0], frames)
    # stabilizer.saveStabilizedFrames(stabilized_frames, 'source/stabilized-frames-10')
    #
    # converter.frames_to_video('source/stabilized-frames', 'source/stabilized-video-10.mp4')
    modal_player
