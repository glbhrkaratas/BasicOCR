import tkinter as tk
from tkinter import filedialog, messagebox
from app.processing import process_image, save_text_to_file
import os
import shutil


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Uygulaması")
        self.root.geometry("400x600")

        self.image_paths = []

        self.languages = {
            "Otomatik Algılama": "auto",
            "Tek Dil (İngilizce)": "eng",
            "Tek Dil (Türkçe)": "tur",
            "Tek Dil (Almanca)": "deu",
            "Tek Dil (Fransızca)": "fra",
            "Tek Dil (İspanyolca)": "spa",
            "Tek Dil (Arapça)": "ara",
            "Tek Dil (Rusça)": "rus",
            "Çoklu Dil (İngilizce + Türkçe)": "eng+tur",
            "Çoklu Dil (İngilizce + Almanca + Fransızca)": "eng+deu+fra"
        }

        self.label = tk.Label(root, text="OCR Uygulamasına Hoş Geldiniz!")
        self.label.pack(pady=10)

        self.lang_label = tk.Label(root, text="Dil Seçimi:")
        self.lang_label.pack()

        self.lang_var = tk.StringVar(value="auto")
        self.lang_menu = tk.OptionMenu(root, self.lang_var, *self.languages.values())
        self.lang_menu.pack(pady=5)

        self.upload_button = tk.Button(root, text="Dosya(lar) Yükle", command=self.upload_files)
        self.upload_button.pack(pady=10)

        self.file_list = tk.Listbox(root, height=5, width=40)
        self.file_list.pack(pady=10)

        self.delete_button = tk.Button(root, text="Seçili Dosyayı Sil", command=self.delete_file, state=tk.DISABLED)
        self.delete_button.pack(pady=5)

        self.continue_button = tk.Button(root, text="Devam", command=self.continue_process, state=tk.DISABLED)
        self.continue_button.pack(pady=5)

        self.process_button = tk.Button(root, text="İşle", command=self.process_files, state=tk.DISABLED)
        self.process_button.pack(pady=5)

        self.text_area_label = tk.Label(root, text="Çıkarılan Metin:")
        self.text_area_label.pack()
        self.text_area_note = tk.Label(root,
                                       text="Not: El yazısı metinler yanlış algılanabilir, lütfen metni kontrol edin ve düzenleyin.",
                                       wraplength=350)
        self.text_area_note.pack()
        self.text_area = tk.Text(root, height=12, width=40)
        self.text_area.pack(pady=10)

    def upload_files(self):
        files = filedialog.askopenfilenames(
            initialdir="input/",
            title="Dosya(lar) Seç",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*"))
        )

        if files:
            input_dir = "input"
            if not os.path.exists(input_dir):
                os.makedirs(input_dir)

            for file in files:
                file_name = os.path.basename(file)
                new_path = os.path.join(input_dir, file_name)
                shutil.copy(file, new_path)
                self.image_paths.append(new_path)
                self.file_list.insert(tk.END, new_path)

            self.continue_button.config(state=tk.NORMAL)
            self.process_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)

    def continue_process(self):
        self.upload_files()

    def delete_file(self):
        selected_index = self.file_list.curselection()
        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir dosya seçin!")
            return

        selected_file = self.image_paths[selected_index[0]]
        try:
            os.remove(selected_file)
            self.image_paths.pop(selected_index[0])
            self.file_list.delete(selected_index)

            if not self.image_paths:
                self.continue_button.config(state=tk.DISABLED)
                self.process_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)

            messagebox.showinfo("Başarılı", f"{selected_file} silindi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya silinirken bir hata oluştu: {e}")

    def process_files(self):
        if not self.image_paths:
            messagebox.showwarning("Uyarı", "Lütfen önce dosya yükleyin!")
            return

        try:
            lang = self.lang_var.get()

            all_text = ""
            for image_path in self.image_paths:
                try:
                    extracted_text, detected_lang = process_image(image_path, lang)
                    all_text += f"--- {image_path} ---\n"
                    if lang == "auto":
                        all_text += f"Algılanan Dil: {detected_lang}\n"
                    all_text += f"{extracted_text}\n\n"
                except Exception as e:
                    all_text += f"--- {image_path} ---\n"
                    all_text += f"Hata: {str(e)}. Bu dosya için metin çıkarılamadı.\n\n"

            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, all_text)

            if messagebox.askyesno("Kaydet", "Çıkarılan metni bilgisayarınıza kaydetmek ister misiniz?"):
                output_path = filedialog.asksaveasfilename(
                    initialdir="output/",
                    title="Metni Kaydet",
                    defaultextension=".txt",
                    filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
                )
                if output_path:
                    final_text = self.text_area.get(1.0, tk.END).strip()
                    save_text_to_file(final_text, output_path)
                    messagebox.showinfo("Başarılı", f"Metin {output_path} dosyasına kaydedildi!")

        except Exception as e:
            messagebox.showerror("Hata", f"Genel bir hata oluştu: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()