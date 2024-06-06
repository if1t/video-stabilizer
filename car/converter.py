import os
from datetime import timedelta

import cv2
import numpy as np


class Converter:
    SAVING_FRAMES_PER_SECOND = 20

    def video_to_frames(self, video_file, output_path):
        # создаем папку по названию видео файла
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        # читать видео файл
        cap = cv2.VideoCapture(video_file)
        # получить FPS видео
        fps = cap.get(cv2.CAP_PROP_FPS)
        # если SAVING_FRAMES_PER_SECOND выше видео FPS, то установите его на FPS (как максимум)
        saving_frames_per_second = min(fps, self.SAVING_FRAMES_PER_SECOND)
        # получить список длительностей для сохранения
        saving_frames_durations = self.__get_saving_frames_durations(cap, saving_frames_per_second)
        # запускаем цикл
        count = 0
        while True:
            is_read, frame = cap.read()
            if not is_read:
                # выйти из цикла, если нет фреймов для чтения
                break
            # получаем продолжительность, разделив количество кадров на FPS
            frame_duration = count / fps
            try:
                # получить самую раннюю продолжительность для сохранения
                closest_duration = saving_frames_durations[0]
            except IndexError:
                # список пуст, все кадры длительности сохранены
                break
            if frame_duration >= closest_duration:
                # если ближайшая длительность меньше или равна длительности кадра,
                # затем сохраняем фрейм
                frame_duration_formatted = self.__format_timedelta(timedelta(seconds=frame_duration))
                cv2.imwrite(os.path.join(output_path, f"frame{frame_duration_formatted}.jpg"), frame)
                # удалить точку продолжительности из списка, так как эта точка длительности уже сохранена
                try:
                    saving_frames_durations.pop(0)
                except IndexError:
                    pass
            # увеличить количество кадров
            count += 1

    @staticmethod
    def __get_saving_frames_durations(cap, saving_fps):
        s = []
        # получаем продолжительность клипа, разделив количество кадров на количество кадров в секунду
        clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        # используйте np.arange () для выполнения шагов с плавающей запятой
        for i in np.arange(0, clip_duration, 1 / saving_fps):
            s.append(i)
        return s

    @staticmethod
    def __format_timedelta(td):
        result = str(td)
        try:
            result, ms = result.split(".")
        except ValueError:
            return result + ".00".replace(":", "-")
        ms = int(ms)
        ms = round(ms / 1e4)
        return f"{result}.{ms:02}".replace(":", "-")

    def frames_to_video(self, frames_path, video_path):
        # Получаем список имен файлов кадров в каталоге
        frames = os.listdir(frames_path)

        # Сортируем кадры по имени файла
        frames.sort()

        # Получаем размер первого кадра, чтобы определить размер выходного видео
        frame = cv2.imread(os.path.join(frames_path, frames[0]))
        height, width, channels = frame.shape

        # Создаем объект VideoWriter для записи видео
        writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), self.SAVING_FRAMES_PER_SECOND,(width, height))

        # Перебираем кадры и пишем их в видео
        for frame_name in frames:
            frame = cv2.imread(os.path.join(frames_path, frame_name))
            writer.write(frame)

        # Освобождаем объект VideoWriter
        writer.release()