import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import os
import re
import base64
from pathlib import Path
from typing import List, Tuple
from tkinterdnd2 import DND_FILES, TkinterDnD


class MarkdownChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkdownChanger")
        self.root.geometry("700x620")
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.selected_path = ctk.StringVar()
        self.path_type = ctk.StringVar()
        self.save_dir = ctk.StringVar()
        self.processing = False
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="MarkdownChanger",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#1a1a1a"
        )
        title_label.pack(pady=(0, 25))
        
        path_frame = ctk.CTkFrame(main_frame, fg_color="#f5f5f5", corner_radius=12)
        path_frame.pack(fill=tk.X, pady=(0, 15))
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="选择文件或文件夹",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="normal"),
            text_color="#555555",
            anchor="w"
        )
        path_label.pack(fill=tk.X, padx=20, pady=(12, 4))
        
        path_entry_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_entry_frame.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        self.path_entry = ctk.CTkEntry(
            path_entry_frame,
            textvariable=self.selected_path,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            height=38,
            placeholder_text="拖拽文件或文件夹到此处",
            state="readonly"
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(
            path_entry_frame,
            text="浏览",
            command=self.select_path,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="normal"),
            width=80,
            height=38,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=8
        )
        browse_button.pack(side=tk.RIGHT)
        
        drop_frame = ctk.CTkFrame(main_frame, fg_color="#e3f2fd", corner_radius=12, border_width=2, border_color="#2196F3")
        drop_frame.pack(fill=tk.X, pady=(0, 15))
        
        drop_label = ctk.CTkLabel(
            drop_frame,
            text="拖拽文件或文件夹到此处",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#555555"
        )
        drop_label.pack(pady=18)
        
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        self.root.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.root.dnd_bind('<<DragLeave>>', self.on_drag_leave)
        
        self.drop_label = drop_label
        self.drop_frame = drop_frame
        
        save_dir_frame = ctk.CTkFrame(main_frame, fg_color="#f5f5f5", corner_radius=12)
        save_dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        save_dir_label = ctk.CTkLabel(
            save_dir_frame,
            text="图片保存目录 (仅用于'转为引用'模式，可不选，默认在当前目录)",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="normal"),
            text_color="#555555",
            anchor="w"
        )
        save_dir_label.pack(fill=tk.X, padx=20, pady=(12, 4))
        
        save_dir_entry_frame = ctk.CTkFrame(save_dir_frame, fg_color="transparent")
        save_dir_entry_frame.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        self.save_dir_entry = ctk.CTkEntry(
            save_dir_entry_frame,
            textvariable=self.save_dir,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            height=38,
            placeholder_text="选择图片保存目录",
            state="readonly"
        )
        self.save_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        save_dir_button = ctk.CTkButton(
            save_dir_entry_frame,
            text="浏览",
            command=self.select_save_dir,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="normal"),
            width=80,
            height=38,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=8
        )
        save_dir_button.pack(side=tk.RIGHT)
        
        log_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff", corner_radius=12, border_width=1, border_color="#e0e0e0")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 18))
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="处理日志",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#333333",
            anchor="w"
        )
        log_label.pack(fill=tk.X, padx=15, pady=(10, 6))
        
        self.log_text = tk.Text(
            log_frame,
            height=6,
            font=("Consolas", 9),
            bg="#fafafa",
            fg="#333333",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 12))
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill=tk.X)
        
        self.to_base64_button = ctk.CTkButton(
            button_frame,
            text="转为 Base64",
            command=lambda: self.start_conversion("to_base64"),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            width=180,
            height=44,
            fg_color="#4CAF50",
            hover_color="#43A047",
            corner_radius=12
        )
        self.to_base64_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.to_ref_button = ctk.CTkButton(
            button_frame,
            text="转为引用",
            command=lambda: self.start_conversion("to_ref"),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            width=180,
            height=44,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=12
        )
        self.to_ref_button.pack(side=tk.RIGHT)
        
        clear_button = ctk.CTkButton(
            button_frame,
            text="清空日志",
            command=self.clear_log,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="normal"),
            width=90,
            height=44,
            fg_color="#757575",
            hover_color="#616161",
            corner_radius=12
        )
        clear_button.pack(side=tk.RIGHT, padx=(0, 12))
    
    def on_drag_enter(self, event):
        self.drop_frame.configure(fg_color="#c8e6c9", border_color="#4CAF50")
        self.drop_label.configure(text="释放以添加", text_color="#2E7D32")
    
    def on_drag_leave(self, event):
        self.drop_frame.configure(fg_color="#e3f2fd", border_color="#2196F3")
        self.drop_label.configure(text="拖拽文件或文件夹到此处", text_color="#555555")
    
    def on_drop(self, event):
        self.drop_frame.configure(fg_color="#e3f2fd", border_color="#2196F3")
        self.drop_label.configure(text="拖拽文件或文件夹到此处", text_color="#555555")
        
        files = self.root.tk.splitlist(event.data)
        if files:
            path = files[0]
            path = path.replace('{', '').replace('}', '').strip()
            if os.path.exists(path):
                self.set_selected_path(path)
    
    def select_path(self):
        choice = messagebox.askyesno(
            "选择类型",
            "要选择文件夹还是文件？\n\n是 = 文件夹\n否 = 文件"
        )
        
        if choice:
            path = filedialog.askdirectory(title="选择包含Markdown文件的文件夹")
            if path:
                self.set_selected_path(path)
        else:
            path = filedialog.askopenfilename(
                title="选择Markdown文件",
                filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
            )
            if path:
                self.set_selected_path(path)
    
    def select_save_dir(self):
        dir_path = filedialog.askdirectory(title="选择图片保存目录")
        if dir_path:
            self.save_dir.set(dir_path)
            self.log(f"已设置图片保存目录: {dir_path}")
    
    def set_selected_path(self, path):
        if os.path.isfile(path):
            self.path_type.set("file")
            self.log(f"已选择文件: {path}")
        elif os.path.isdir(path):
            self.path_type.set("folder")
            self.log(f"已选择文件夹: {path}")
        else:
            self.log(f"错误: 无效的路径 - {path}")
            return
        
        self.selected_path.set(path)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def image_to_base64(self, image_path: str) -> str:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            
            ext = Path(image_path).suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/png')
            
            return f"data:{mime_type};base64,{base64_data}"
    
    def base64_to_image(self, base64_data: str, save_path: str) -> Tuple[bool, str]:
        try:
            match = re.match(r'data:(image/[a-zA-Z+]+);base64,(.+)', base64_data)
            if not match:
                return False, ""
            
            mime_type, encoded_data = match.groups()
            
            ext_map = {
                'image/png': '.png',
                'image/jpeg': '.jpg',
                'image/gif': '.gif',
                'image/bmp': '.bmp',
                'image/webp': '.webp'
            }
            
            ext = ext_map.get(mime_type, '.png')
            
            filename = os.path.basename(save_path)
            dirname = os.path.dirname(save_path)
            
            name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
            final_filename = name_without_ext + ext
            final_path = os.path.join(dirname, final_filename) if dirname else final_filename
            
            image_data = base64.b64decode(encoded_data)
            
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            with open(final_path, 'wb') as f:
                f.write(image_data)
            
            return True, final_path
        except Exception as e:
            return False, ""
    
    def process_markdown_to_base64(self, md_file_path: str) -> Tuple[bool, str]:
        try:
            md_dir = os.path.dirname(md_file_path)
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
            images = re.findall(image_pattern, content)
            
            self.log(f"  找到 {len(images)} 个图片引用")
            
            if not images:
                return False, "未找到本地图片"
            
            converted_count = 0
            for alt_text, image_path in images:
                image_path = image_path.strip()
                self.log(f"  检查图片: {image_path}")
                
                if image_path.startswith(('http://', 'https://')):
                    self.log(f"    跳过网络图片")
                    continue
                
                if image_path.startswith('data:'):
                    self.log(f"    已经是Base64编码，跳过")
                    continue
                
                if os.path.isabs(image_path):
                    full_image_path = image_path
                    self.log(f"    检测到绝对路径")
                else:
                    full_image_path = os.path.join(md_dir, image_path)
                    full_image_path = os.path.normpath(full_image_path)
                    self.log(f"    检测到相对路径，拼接后: {full_image_path}")
                
                if not os.path.exists(full_image_path):
                    self.log(f"  警告: 图片不存在 - {full_image_path}")
                    continue
                
                try:
                    base64_image = self.image_to_base64(full_image_path)
                    self.log(f"    Base64编码长度: {len(base64_image)} 字符")
                    
                    escaped_alt = re.escape(alt_text)
                    escaped_path = re.escape(image_path)
                    old_pattern = f'!\\[{escaped_alt}\\]\\({escaped_path}\\)'
                    new_pattern = f'![{alt_text}]({base64_image})'
                    content = re.sub(old_pattern, new_pattern, content)
                    converted_count += 1
                    self.log(f"  已转换: {image_path}")
                except Exception as e:
                    self.log(f"  错误: 无法转换 {image_path} - {str(e)}")
            
            if converted_count == 0:
                return False, "没有可转换的本地图片"
            
            output_path = md_file_path.replace('.md', '-base64.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, f"成功转换 {converted_count} 张图片"
            
        except Exception as e:
            return False, f"处理失败: {str(e)}"
    
    def process_markdown_to_ref(self, md_file_path: str) -> Tuple[bool, str]:
        try:
            save_dir = self.save_dir.get()
            if not save_dir:
                md_dir = os.path.dirname(md_file_path)
                save_dir = md_dir
                self.log(f"  未指定保存目录，使用Markdown文件所在目录")
            
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            base64_pattern = r'!\[([^\]]*)\]\((data:image/[a-zA-Z+]+;base64,[^)]+)\)'
            images = re.findall(base64_pattern, content)
            
            self.log(f"  找到 {len(images)} 个Base64图片")
            
            if not images:
                return False, "未找到Base64编码的图片"
            
            converted_count = 0
            for alt_text, base64_data in images:
                self.log(f"  处理Base64图片")
                
                image_name = f"image_{converted_count + 1}"
                if alt_text:
                    safe_name = re.sub(r'[<>:"/\\|?*]', '_', alt_text)
                    if safe_name:
                        image_name = safe_name
                
                image_path = os.path.join(save_dir, image_name)
                
                try:
                    success, final_image_path = self.base64_to_image(base64_data, image_path)
                    if success:
                        rel_path = os.path.relpath(final_image_path, os.path.dirname(md_file_path))
                        rel_path = rel_path.replace('\\', '/')
                        
                        escaped_alt = re.escape(alt_text)
                        escaped_base64 = re.escape(base64_data)
                        old_pattern = f'!\\[{escaped_alt}\\]\\({escaped_base64}\\)'
                        new_pattern = f'![{alt_text}]({rel_path})'
                        content = re.sub(old_pattern, new_pattern, content)
                        
                        self.log(f"  已提取: {final_image_path}")
                        converted_count += 1
                    else:
                        self.log(f"  错误: 无法解码Base64数据")
                except Exception as e:
                    self.log(f"  错误: 无法提取图片 - {str(e)}")
            
            if converted_count == 0:
                return False, "没有可提取的Base64图片"
            
            output_path = md_file_path.replace('.md', '-ref.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, f"成功提取 {converted_count} 张图片"
            
        except Exception as e:
            return False, f"处理失败: {str(e)}"
    
    def start_conversion(self, mode):
        if self.processing:
            return
        
        path = self.selected_path.get()
        path_type = self.path_type.get()
        
        if not path:
            messagebox.showwarning("警告", "请选择文件或文件夹")
            return
        
        if mode == "to_ref":
            save_dir = self.save_dir.get()
            if not save_dir:
                self.log("提示: 未指定保存目录，将使用Markdown文件所在目录")
        
        self.processing = True
        self.to_base64_button.configure(state=tk.DISABLED)
        self.to_ref_button.configure(state=tk.DISABLED)
        self.clear_log()
        
        mode_name = "转为Base64" if mode == "to_base64" else "转为引用"
        self.log("=" * 50)
        self.log(f"开始处理 - {mode_name}")
        self.log("=" * 50)
        
        try:
            if path_type == "file":
                self.log(f"\n处理文件: {os.path.basename(path)}")
                if mode == "to_base64":
                    success, message = self.process_markdown_to_base64(path)
                    suffix = "-base64.md"
                else:
                    success, message = self.process_markdown_to_ref(path)
                    suffix = "-ref.md"
                
                if success:
                    self.log(f"✓ {message}")
                    output_file = path.replace('.md', suffix)
                    self.log(f"输出文件: {output_file}")
                else:
                    self.log(f"✗ {message}")
            else:
                md_files = []
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.md'):
                            md_files.append(os.path.join(root, file))
                
                if not md_files:
                    self.log("\n未找到Markdown文件")
                else:
                    self.log(f"\n找到 {len(md_files)} 个Markdown文件\n")
                    
                    success_count = 0
                    for md_file in md_files:
                        rel_path = os.path.relpath(md_file, path)
                        self.log(f"处理: {rel_path}")
                        
                        if mode == "to_base64":
                            success, message = self.process_markdown_to_base64(md_file)
                        else:
                            success, message = self.process_markdown_to_ref(md_file)
                        
                        if success:
                            self.log(f"✓ {message}")
                            success_count += 1
                        else:
                            self.log(f"✗ {message}")
                        self.log("-" * 40)
                    
                    self.log(f"\n总计: {success_count}/{len(md_files)} 个文件处理成功")
            
            self.log("\n" + "=" * 50)
            self.log("转化完成!")
            self.log("=" * 50)
            
        except Exception as e:
            self.log(f"\n错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误:\n{str(e)}")
        
        finally:
            self.processing = False
            self.to_base64_button.configure(state=tk.NORMAL)
            self.to_ref_button.configure(state=tk.NORMAL)


def main():
    root = TkinterDnD.Tk()
    app = MarkdownChanger(root)
    root.mainloop()


if __name__ == "__main__":
    main()
