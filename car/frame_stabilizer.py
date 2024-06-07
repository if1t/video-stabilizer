import glob
from pathlib import Path
import cv2
import numpy as np
from scipy import signal


class FrameStabilizer:
    @staticmethod
    def get_frames_from_path(path_to_frames):
        return [
            cv2.imread(path_to_frame)
            for path_to_frame in sorted(glob.glob(f"{path_to_frames}/*"))
        ]

    @staticmethod
    def stabilizeFrames(primary_frame, frames):
        stabilized_frames = []

        for current_frame in frames:
            stabilized_frame = FrameStabilizer.stabilize(primary_frame, current_frame)
            stabilized_frames.append(stabilized_frame)

        return stabilized_frames

    @staticmethod
    def saveStabilizedFrames(stabilized_frames, output_dir):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for i, frame in enumerate(stabilized_frames):
            cv2.imwrite(f"{output_dir}/frame_{i}.jpg", frame)

    @staticmethod
    def stabilize(primary_frame, current_frame):
        # Преобразуем кадры в оттеночные изображения
        gray_previous_frame = cv2.cvtColor(primary_frame, cv2.COLOR_BGR2GRAY)
        gray_current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Нормализуем пиксели кадров
        gray_previous_frame = cv2.normalize(gray_previous_frame, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)
        gray_current_frame = cv2.normalize(gray_current_frame, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)

        len_x = len(gray_previous_frame[0])
        len_y = len(gray_previous_frame)

        center_x = len_x / 2
        center_y = len_y / 2

        corr = signal.correlate2d(gray_current_frame, gray_previous_frame, boundary='symm', mode='same')
        corr_max_indexes = np.unravel_index(np.argmax(corr), corr.shape)

        x = corr_max_indexes[1]
        y = corr_max_indexes[0]

        # Находим разницу, при смещении на которую получим максимальную кореляцию изображений
        shift = [x - center_x, y - center_y]
        print(shift)

        # корректируем текущий кадр
        current_frame = cv2.warpAffine(
            current_frame,
            np.array([[1, 0, -shift[0]], [0, 1, -shift[1]]]),
            (current_frame.shape[1],
             current_frame.shape[0])
        )

        return current_frame
