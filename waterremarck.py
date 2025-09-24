import cv2
import numpy as np
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class WatermarkRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Удаление водяных знаков")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
      
        self.image_path = tk.StringVar()
        self.x1 = tk.StringVar(value="10")
        self.y1 = tk.StringVar(value="10")
        self.x2 = tk.StringVar(value="200")
        self.y2 = tk.StringVar(value="50")
        
        self.create_widgets()
    
    def create_widgets(self):
       
        tk.Label(self.root, text="Удаление водяных знаков", font=("Arial", 16, "bold")).pack(pady=10)
        
      
        frame_file = tk.Frame(self.root)
        frame_file.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_file, text="Изображение:").pack(side="left")
        tk.Entry(frame_file, textvariable=self.image_path, width=35).pack(side="left", padx=5, fill="x", expand=True)
        tk.Button(frame_file, text="Выбрать", command=self.select_image).pack(side="left")
        
       
        frame_coords = tk.LabelFrame(self.root, text="Координаты водяного знака (x1 y1 x2 y2)", padx=10, pady=10)
        frame_coords.pack(fill="x", padx=20, pady=10)
        
     
        grid = ttk.Frame(frame_coords)
        grid.pack()
        
        labels = ["x1:", "y1:", "x2:", "y2:"]
        for i, label in enumerate(labels):
            tk.Label(grid, text=label).grid(row=0, column=i*2, padx=5, pady=5)
            entry = tk.Entry(grid, width=8)
            entry.grid(row=0, column=i*2+1, padx=5, pady=5)
            
            if i == 0: self.x1_entry = entry
            elif i == 1: self.y1_entry = entry
            elif i == 2: self.x2_entry = entry
            elif i == 3: self.y2_entry = entry
        
        # Кнопки
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Удалить водяной знак", 
                 command=self.process_image, 
                 bg="#4CAF50", fg="white", width=20).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Выход", 
                 command=self.root.quit, 
                 bg="#f44336", fg="white", width=10).pack(side="left", padx=5)
        
        # Статус
        self.status = tk.Label(self.root, text="Готов к работе", fg="blue")
        self.status.pack(side="bottom", pady=5)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path.set(file_path)
            self.status.config(text=f"Выбрано: {os.path.basename(file_path)}")
    
    def process_image(self):
        try:
            
            if not self.image_path.get():
                messagebox.showerror("Ошибка", "Выберите изображение")
                return
            
            try:
                x1 = int(self.x1_entry.get())
                y1 = int(self.y1_entry.get())
                x2 = int(self.x2_entry.get())
                y2 = int(self.y2_entry.get())
                
                if x1 >= x2 or y1 >= y2:
                    raise ValueError("Некорректные координаты")
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Некорректные координаты: {str(e)}")
                return
            
            
            input_path = self.image_path.get()
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_cleaned{ext}"
            
            self.remove_watermark(input_path, output_path, x1, y1, x2, y2)
            
           
            self.status.config(text=f"Готово! Результат: {os.path.basename(output_path)}", fg="green")
            messagebox.showinfo("Успех", "Водяной знак удален успешно!")
            
        except Exception as e:
            self.status.config(text=f"Ошибка: {str(e)}", fg="red")
            messagebox.showerror("Ошибка", str(e))
    
    def remove_watermark(self, input_path, output_path, x1, y1, x2, y2):
        """Основная логика удаления водяного знака"""
       
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Изображение не найдено: {input_path}")
        
        
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Не удалось загрузить изображение: {input_path}")
        
       
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
        
      
        result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        
    
        cv2.imwrite(output_path, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkRemoverApp(root)
    root.mainloop()