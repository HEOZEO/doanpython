import threading
import cv2
from PIL import Image
import io
from dotenv import load_dotenv
import os
import tkinter as tk
import google.generativeai as genai
import google.ai.generativelanguage as glm

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")

class ContentDescriber:
    def __init__(self, root, user_input, video_handler):
        self.root = root
        self.user_input = user_input
        self.video_handler = video_handler
        self.message_var = tk.StringVar()
        self.is_processing = False

    def describe_content(self):
        current_frame = self.video_handler.get_current_frame()
        if current_frame is not None:
            try:
                self.root.after(0, self.message_var.set, "Đang mô tả...")
                pil_image = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='JPEG')
                blob = glm.Blob(mime_type='image/jpeg', data=img_byte_arr.getvalue())
                user_request = "Trả lời bằng tiếng Việt, mô tả ngắn gọn và trả lời chính xác."
                response = model.generate_content([user_request, blob], stream=True)
                for chunk in response:
                    self.root.after(0, self.update_message, chunk.text)
            except Exception as e:
                self.root.after(0, self.update_message, f"Lỗi: {str(e)}")
            finally:
                self.is_processing = False
        else:
            self.root.after(0, self.update_message, "Không có khung hình khả dụng")
            self.is_processing = False

    def threaded_describe_content(self):
        if not self.is_processing:
            self.is_processing = True
            describe_thread = threading.Thread(target=self.describe_content)
            describe_thread.start()

    def update_message(self, new_text):
        current_text = self.message_var.get()
        updated_text = current_text + new_text + "\n"
        self.message_var.set(updated_text)
