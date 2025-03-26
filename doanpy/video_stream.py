from PIL import Image, ImageTk
import cv2
import tkinter as tk

class VideoStreamHandler:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None
        self.photo = None
        
        if not self.cap.isOpened():
            print("Không thể mở camera.")
            self.cap = None

    def video_stream(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                self.photo = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(10, self.video_stream)  # Cập nhật mỗi 10ms

    def start_stream(self):
        if self.cap:
            self.video_stream()

    def get_current_frame(self):
        return self.current_frame

    def stop_video(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            print("Đã dừng video.")

