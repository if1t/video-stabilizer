import os
import tkinter as tk

import cv2
from PIL import ImageTk, Image

from converter import Converter
from frame_stabilizer import FrameStabilizer
import tkinter.messagebox

# Создание главной формы
root = tk.Tk()
root.title("Видеоредактор")
root.geometry("600x400")

# Создание полей ввода
input_video_path = tk.StringVar()
input_video_label = tk.Label(root, text="Видео, которое нужно стабилизировать: ")
input_video_label.grid(row=0, column=0)
input_video_entry = tk.Entry(root, textvariable=input_video_path)
input_video_entry.grid(row=0, column=1)

input_frames_path = tk.StringVar()
input_frames_label = tk.Label(root, text="Сохранить кадры в каталог: ")
input_frames_label.grid(row=1, column=0)
input_frames_entry = tk.Entry(root, textvariable=input_frames_path)
input_frames_entry.grid(row=1, column=1)

# Создание кнопки "Разбить на кадры"
convert_button = tk.Button(root, text="Разбить на кадры",
                           command=lambda: Converter.video_to_frames(input_video_path.get(), input_frames_path.get()))
convert_button.grid(row=3, column=1)

# Функция, которая будет вызвана после нажатия на кнопку "Разбить на кадры"
def after_convert():
    # Удаление полей ввода для видео, кадров
    input_video_label.destroy()
    input_video_entry.destroy()
    input_frames_label.destroy()
    input_frames_entry.destroy()
    convert_button.destroy()

    # Создание кнопки выбора кадра
    select_frame_button = tk.Button(root, text="Выбрать кадр", command=open_frames_window)
    select_frame_button.grid(row=4, column=1)

# Открытие окна с кадрами
def open_frames_window():
    frames_window = tk.Toplevel()
    frames_window.title("Выбор кадра")
    frames_window.geometry("800x600")

    global current_frame_label  # Создаем глобальную переменную для метки с изображением

    # Функция для обновления изображения кадра
    def update_frame_image(event):
        global current_frame_label
        selected_frame = frames_list.get(tk.ACTIVE)
        frame_path = os.path.join(input_frames_path.get(), selected_frame)

        # Загрузка изображения с помощью Pillow
        img = Image.open(frame_path)
        img.thumbnail((700, 500))  # Изменение размера изображения для отображения
        photo = ImageTk.PhotoImage(img)

        # Обновление метки с изображением
        if current_frame_label is None:
            current_frame_label = tk.Label(frames_window, image=photo)
            current_frame_label.image = photo  # Сохранение ссылки на изображение
            current_frame_label.pack()
        else:
            current_frame_label.config(image=photo)
            current_frame_label.image = photo  # Сохранение ссылки на изображение

    # Создание скроллбара
    scrollbar = tk.Scrollbar(frames_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Создание списка кадров
    frames_list = tk.Listbox(frames_window, yscrollcommand=scrollbar.set)
    for frame in os.listdir(input_frames_path.get()):
        frames_list.insert(tk.END, frame)
    frames_list.pack(side=tk.LEFT, fill=tk.BOTH)

    # Привязка события выбора элемента списка к функции обновления изображения
    frames_list.bind('<<ListboxSelect>>', update_frame_image)

    current_frame_label = None  # Инициализируем метку с изображением

    # Функция для выбора кадра
    def select_frame():
        global primary_frame
        primary_frame = cv2.imread(os.path.join(input_frames_path.get(), frames_list.get(tk.ACTIVE)))

        # Удаление списка кадров
        frames_window.destroy()

        # Создание полей ввода для стабилизированных кадров и видео
        output_frames_path = tk.StringVar()
        output_frames_label = tk.Label(root, text="Путь для сохранения стабилизированных кадров: ")
        output_frames_label.grid(row=5, column=0)
        output_frames_entry = tk.Entry(root, textvariable=output_frames_path)
        output_frames_entry.grid(row=5, column=1)

        output_video_path = tk.StringVar()
        output_video_label = tk.Label(root, text="Сохранить стабилизированное видео как: ")
        output_video_label.grid(row=6, column=0)
        output_video_entry = tk.Entry(root, textvariable=output_video_path)
        output_video_entry.grid(row=6, column=1)

        # Создание кнопки "Стабилизировать"
        stabilize_button = tk.Button(root, text="Стабилизировать", command=lambda: stabilize_video(primary_frame, input_frames_path.get(), output_frames_path.get(), output_video_path.get()))
        stabilize_button.grid(row=7, column=1)

    # Создание кнопки выбора кадра
    select_frame_button = tk.Button(frames_window, text="Выбрать главным", command=select_frame)
    select_frame_button.pack(side=tk.BOTTOM)

# Запуск функции after_convert после завершения конвертации
convert_button.config(command=lambda: [Converter.video_to_frames(input_video_path.get(), input_frames_path.get()), after_convert()])

# Функция стабилизации видео
def stabilize_video(primary_frame, input_frames_path, output_frames_path, output_video_path):
    # Стабилизация кадров
    frames = FrameStabilizer.get_frames_from_path(input_frames_path)
    stabilized_frames = FrameStabilizer.stabilizeFrames(primary_frame, frames)

    # Сохранение стабилизированных кадров
    FrameStabilizer.saveStabilizedFrames(stabilized_frames, output_frames_path)

    # Конвертация кадров в видео
    Converter.frames_to_video(output_frames_path, output_video_path)
    root.destroy()

    # Вывод сообщения об успехе
    tkinter.messagebox.showinfo("Успех!", "Видео стабилизировано!")

# Запуск приложения
root.mainloop()