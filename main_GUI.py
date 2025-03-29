import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
from borax.calendars.lunardate import LunarDate
import datetime

# 六宫定义（含五行属性）
LIU_GONG = [
    ('大安', '吉', '木', '安稳清吉，贵人扶持'),
    ('留连', '凶', '土', '反复拖延，纠缠不休'),
    ('速喜', '吉', '火', '喜讯速至，合作有利'),
    ('赤口', '凶', '金', '官非口舌，金属血光'),
    ('小吉', '吉', '水', '谋事可成，出行有利'),
    ('空亡', '凶', '土', '事有不成，财防落空')
]

# 时辰对照表（新增分钟计算）
SHI_CHEN = [
    ('子', '23:00-01:00'), ('丑', '01:00-03:00'),
    ('寅', '03:00-05:00'), ('卯', '05:00-07:00'),
    ('辰', '07:00-09:00'), ('巳', '09:00-11:00'),
    ('午', '11:00-13:00'), ('未', '13:00-15:00'),
    ('申', '15:00-17:00'), ('酉', '17:00-19:00'),
    ('戌', '19:00-21:00'), ('亥', '21:00-23:00')
]

COLORS = {
    'background': '#F0F4F7',
    'card_bg': '#FFFFFF',
    'primary': '#2A5CAA',
    'secondary': '#5E9ED6',
    'success': '#67C23A',
    'danger': '#F56C6C',
    'text': '#303133'
}


def resource_path(relative_path):
    """获取资源的绝对路径（兼容开发环境和打包后环境）"""
    try:
        base_path = sys._MEIPASS  # PyInstaller创建的临时文件夹
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DivinationApp:
    def __init__(self, root):
        self.root = root
        # 修改图标加载方式
        icon_path = resource_path("generated_image_march_29__2025___8_33pm_ouV_icon.ico")
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"加载图标失败: {e}")  # 调试用
        self.root.title("小六壬算你命")
        self.root.geometry("720x600")
        self.root.configure(bg=COLORS['background'])
        self.setup_ui()

    def setup_ui(self):
        # 字体配置
        self.title_font = font.Font(family='Microsoft YaHei', size=18, weight='bold')
        self.body_font = font.Font(family='Microsoft YaHei', size=11)
        self.symbol_font = font.Font(family='SimSun', size=20)

        # 主布局
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # 输入面板
        input_frame = tk.LabelFrame(main_frame, text=" 时间设置 ", font=self.title_font,
                                    bg=COLORS['card_bg'], fg=COLORS['primary'])
        input_frame.pack(fill=tk.X, pady=10)

        self.create_time_inputs(input_frame)

        # 操作按钮
        btn_frame = tk.Frame(main_frame, bg=COLORS['background'])
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="立即占卜", command=self.calculate,
                   style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="重置", command=self.reset).pack(side=tk.LEFT, padx=5)

        # 结果展示
        result_frame = tk.LabelFrame(main_frame, text=" 卦象解读 ", font=self.title_font,
                                     bg=COLORS['card_bg'], fg=COLORS['primary'])
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, bg=COLORS['card_bg'],
                                   font=self.body_font, padx=15, pady=15)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 样式配置
        self.style = ttk.Style()
        self.style.configure('Accent.TButton', foreground='white',
                             background=COLORS['secondary'], font=self.body_font)

    def create_time_inputs(self, parent):
        time_vars = {
            'year': tk.StringVar(value=str(datetime.datetime.now().year)),
            'month': tk.StringVar(value=str(datetime.datetime.now().month)),
            'day': tk.StringVar(value=str(datetime.datetime.now().day)),
            'hour': tk.StringVar(value=str(datetime.datetime.now().hour))
        }

        input_grid = tk.Frame(parent, bg=COLORS['card_bg'])
        input_grid.pack(padx=10, pady=10)

        for col, (label, var) in enumerate(zip(['年', '月', '日', '时'], time_vars.values())):
            frame = tk.Frame(input_grid, bg=COLORS['card_bg'])
            frame.grid(row=0, column=col, padx=10)

            tk.Label(frame, text=label, bg=COLORS['card_bg'],
                     font=self.body_font).pack()
            ttk.Entry(frame, textvariable=var, width=8,
                      font=self.body_font, justify='center').pack(pady=5)

        self.time_vars = time_vars

    def validate_date(self):
        try:
            return (
                int(self.time_vars['year'].get()),
                int(self.time_vars['month'].get()),
                int(self.time_vars['day'].get()),
                int(self.time_vars['hour'].get())
            )
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
            return None

    def calculate(self):
        inputs = self.validate_date()
        if not inputs: return

        y, m, d, h = inputs

        try:
            # 计算农历和时辰
            dt = datetime.datetime(y, m, d, h)
            lunar_date = LunarDate.from_solar_date(y, m, d)

            # 时辰计算
            shi_chen_idx = (h + 1) // 2 % 12  # 简化计算逻辑
            sc_name, sc_range = SHI_CHEN[shi_chen_idx]

            # 三宫定位算法
            month_index = (lunar_date.month - 1) % 6
            day_index = (month_index + lunar_date.day - 1) % 6
            hour_index = (day_index + shi_chen_idx) % 6

            # 构建结果
            result = {
                '公历': dt.strftime('%Y-%m-%d %H:%M'),
                '农历': f'{lunar_date.month}月{lunar_date.day}日' + ('(闰)' if lunar_date.leap else ''),
                '时辰': f'{sc_name}时 ({sc_range})',
                '卦象': {
                    '月宫': LIU_GONG[month_index],
                    '日宫': LIU_GONG[day_index],
                    '时宫': LIU_GONG[hour_index]
                }
            }

            self.show_result(result)

        except Exception as e:
            messagebox.showerror("计算错误", f"算法异常：{str(e)}")

    def show_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        # 基础信息
        self.result_text.insert(tk.END, "✨ 卦象报告\n", 'title')
        self.result_text.insert(tk.END, f"公历时间：{result['公历']}\n")
        self.result_text.insert(tk.END, f"农历时间：{result['农历']}\n")
        self.result_text.insert(tk.END, f"当前时辰：{result['时辰']}\n\n")

        # 卦象解读
        for pos in ['月宫', '日宫', '时宫']:
            name, jx, wx, desc = result['卦象'][pos]
            color = COLORS['success'] if jx == '吉' else COLORS['danger']

            self.result_text.insert(tk.END, f"▍{pos}\n", 'subtitle')
            self.result_text.insert(tk.END, f"• 名称：", 'label')
            self.result_text.insert(tk.END, f"{name}\n", ('value', color))
            self.result_text.insert(tk.END, f"• 属性：", 'label')
            self.result_text.insert(tk.END, f"{wx}\n", 'value')
            self.result_text.insert(tk.END, f"• 解读：{desc}\n\n")

        # 设置文本样式
        self.result_text.tag_configure('title', font=self.title_font, foreground=COLORS['primary'])
        self.result_text.tag_configure('subtitle', font=self.body_font, foreground=COLORS['text'])
        self.result_text.tag_configure('label', font=self.body_font, foreground='#606266')
        self.result_text.tag_configure('value', font=('Microsoft YaHei', 11, 'bold'))
        self.result_text.config(state=tk.DISABLED)

    def reset(self):
        now = datetime.datetime.now()
        self.time_vars['year'].set(str(now.year))
        self.time_vars['month'].set(str(now.month))
        self.time_vars['day'].set(str(now.day))
        self.time_vars['hour'].set(str(now.hour))
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = DivinationApp(root)
    root.mainloop()