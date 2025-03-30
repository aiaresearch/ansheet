import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from inter_func import function_a,function_b


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("主界面")
        self.master.geometry("400x300")
        self.w_height=master.winfo_screenheight()
        self.w_width=master.winfo_screenwidth()
        # 主界面组件
        self.btn_single = tk.Button(master, text="首张录入", command=self.start_single, height=3, width=20)
        self.btn_batch = tk.Button(master, text="大批量分拣", command=self.start_batch, height=3, width=20)
        self.btn_single.pack(pady=20)
        self.btn_batch.pack()

    def start_single(self):
        # 执行函数a（示例返回图片路径）
        image_path,dst = function_a()
        self.dst=dst
        if image_path:
            self.master.destroy()  # 关闭主界面
            SingleInputWindow(image_path,self.w_height,self.w_width)

    def start_batch(self):
        self.master.destroy()  # 关闭主界面
        BatchProcessWindow()


class SingleInputWindow:
    def __init__(self, image_path,w_height,w_width):
        self.window = tk.Tk()
        self.window.title("首张录入")

        # 初始化数据
        self.w_height=w_height
        self.w_width=w_width
        self.image_path = image_path
        self.rectangles = []
        self.canvas_objects = []

        # 创建界面组件
        self.create_widgets()
        self.load_image()

        self.window.mainloop()

    # def create_widgets(self):
    #     # 输入区域
    #     input_frame = tk.Frame(self.window)
    #     input_frame.pack(fill=tk.X, padx=10, pady=5)

    #     # 准考证位数
    #     tk.Label(input_frame, text="准考证号位数:").grid(row=0, column=0)
    #     self.num_entry = tk.Entry(input_frame, width=10)
    #     self.num_entry.grid(row=0, column=1)

    #     # 班级信息
    #     tk.Label(input_frame, text="班级信息(如1-3):").grid(row=1, column=0)
    #     self.class_entry = tk.Entry(input_frame, width=10)
    #     self.class_entry.grid(row=1, column=1)
    def create_widgets(self):
    # 输入区域
        input_frame = tk.Frame(self.window)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # 准考证位数（默认6位）
        tk.Label(input_frame, text="准考证号位数:").grid(row=0, column=0)
        self.num_entry = tk.Entry(input_frame, width=10)
        self.num_entry.grid(row=0, column=1)
        self.num_entry.insert(0, '8')  # 设置默认值

        # 班级信息（默认1-3班）
        tk.Label(input_frame, text="班级信息(如1-3):").grid(row=1, column=0)
        self.class_entry = tk.Entry(input_frame, width=10)
        self.class_entry.grid(row=1, column=1)
        self.class_entry.insert(0, '5-6')  # 设置默认值


        # 按钮区域
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=5)

        self.btn_undo = tk.Button(btn_frame, text="撤回", command=self.undo_last, state=tk.DISABLED)
        self.btn_undo.pack(side=tk.LEFT, padx=5)
        self.btn_confirm = tk.Button(btn_frame, text="完成", command=self.confirm)
        self.btn_confirm.pack(side=tk.LEFT)

        # 画布区域
        self.canvas = tk.Canvas(self.window, cursor="cross", bg="#f0f0f0")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 事件绑定
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def compress_jpg(self,input_path, output_path, target_size, quality=85):
        img=Image.open(input_path)
        # 验证为RGB模式（标准JPG格式）
        assert img.mode == 'RGB', "输入必须是标准RGB模式的JPG文件"

        # 获取原始尺寸
        orig_width, orig_height = img.size
        print(f"原始尺寸: {orig_width}x{orig_height}")

        # 自动计算等比缩放后的尺寸
        print('target_size:',target_size)
        ratio = min(target_size[0] / orig_width, target_size[1] / orig_height)
        self.ratio=ratio
        new_size = (int(orig_width * ratio), int(orig_height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        print(f"缩放后尺寸: {new_size}")

        # 保存优化后的JPG
        img.save(
            output_path,
            format='JPEG',
            quality=quality,
            optimize=True,    # 启用霍夫曼表优化
            progressive=True, # 生成渐进式JPG
            subsampling=0     # 保持4:4:4色度采样（最高质量）
        )
            
                
    def load_image(self):
        # 加载并显示图片
        self.image = Image.open(self.image_path)
        self.image_width,self.image_height=self.image.size
        self.tk_image = ImageTk.PhotoImage(self.image)

        if self.w_width>=self.image_width and self.w_height>=self.image_height:
            self.canvas.config(
                width=self.tk_image.width(),
                height=self.tk_image.height()
            )
        else:
            self.compress_jpg(self.image_path,'./ansheet/image/img_resize.jpg',(self.w_width,self.w_height))
            self.image_path='./ansheet/image/img_resize.jpg'
            self.load_image()

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        # 创建临时矩形
        rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline="#FF0000", width=2, dash=(5, 5)
        )
        self.current_rect = rect

    def on_drag(self, event):
        if hasattr(self, 'current_rect'):
            self.canvas.coords(
                self.current_rect,
                self.start_x, self.start_y,
                event.x, event.y
            )

    def on_release(self, event):
        end_x = event.x
        end_y = event.y

        # 计算规范坐标
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        #compute absolute coordinates
        x1,x2,y1,y2=map(lambda x:int(x/self.ratio),[x1,x2,y1,y2])

        # 更新矩形样式
        self.canvas.itemconfig(
            self.current_rect,
            outline="#0000FF",
            dash=None
        )

        # 添加坐标标签
        text_id = self.canvas.create_text(
            (x1 + x2) // 2, (y1 + y2) // 2,
            text=f"({x1},{y1})-({x2},{y2})",
            fill="white",
            font=("Arial", 8)
        )

        # 保存记录
        self.rectangles.append((x1, y1, x2, y2))
        self.canvas_objects.append((self.current_rect, text_id))

        # 激活撤回按钮
        self.btn_undo.config(state=tk.NORMAL)

        delattr(self, 'current_rect')

    def undo_last(self):
        if self.canvas_objects:
            # 删除最后绘制的图形
            rect_id, text_id = self.canvas_objects.pop()
            self.canvas.delete(rect_id)
            self.canvas.delete(text_id)
            self.rectangles.pop()

            if not self.canvas_objects:
                self.btn_undo.config(state=tk.DISABLED)

    def confirm(self):
        # 获取输入数据
        num_str = self.num_entry.get()
        class_str = self.class_entry.get()

        # 输入验证
        if not num_str.isdigit():
            messagebox.showerror("错误", "请输入有效的准考证位数")
            return

        try:
            class_part = tuple(map(int, class_str.split('-')))
        except:
            messagebox.showerror("错误", "班级信息格式错误，示例：1-3")
            return

        # 打包数据传递给函数b
        data = {
            "rectangles": self.rectangles,
            "num_digits": int(num_str),
            "class_range": class_part
        }
        function_b(data,self.dst)
        self.window.destroy()
class BatchProcessWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("大批量分拣")
        self.window.geometry("300x150")
        
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        # 主容器
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # 输入区域
        input_frame = tk.Frame(main_frame)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="要分拣几张答题卡：").pack(side=tk.LEFT)
        self.num_entry = tk.Entry(input_frame, width=10)
        self.num_entry.pack(side=tk.LEFT, padx=5)
        
        # 按钮区域
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="确定", command=self.process_batch).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="返回", command=self.back_to_main).pack(side=tk.LEFT)

    def process_batch(self):
        # 获取输入数量
        num_str = self.num_entry.get()
        
        # 输入验证
        if not num_str.isdigit() or int(num_str) <= 0:
            messagebox.showerror("输入错误", "请输入有效的正整数")
            return
            
        num = int(num_str)
        
        # 执行批量处理函数
        if function_c(num):
            messagebox.showinfo("完成", f"成功处理{num}张答题卡")
            self.window.destroy()
        else:
            messagebox.showerror("错误", "处理过程中发生错误")

    def back_to_main(self):
        self.window.destroy()
        root = tk.Tk()
        MainApp(root)
        root.mainloop()
    

#
# # 示例函数
# def function_a():
#     # 示例：打开文件对话框选择图片
#     path = "./ansheet/image/img1.jpg"# just for example
#     return path


# def function_b(data):
#     # 示例：显示收集到的数据
#     print("传递给函数b的数据：")
#     print(f"准考证位数：{data['num_digits']}")
#     print(f"班级信息段：{data['class_range'][0]}-{data['class_range'][1]}")
#     print("框选区域坐标：")
#     for i, rect in enumerate(data['rectangles']):
#         print(f"区域{i + 1}: {rect}")
def function_c(quantity):
    """批量处理函数示例"""
    print(f"正在批量处理 {quantity} 张答题卡...")
    # 此处添加实际处理逻辑
    return True  # 返回处理结果
def quit_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    #root.attributes('-fullscreen', True) 
    #root.bind('<Escape>', quit_fullscreen)  # 绑定 ESC 键退出
    root.mainloop()