import random
import tkinter as tk
from tkinter import ttk
from ..base_nodes import Node


class RandomNode(Node):
    def __init__(self, range_node, decimals):
        self.range_node = range_node
        self.decimals = decimals
    
    def evaluate(self, env):
        range_val = self.range_node.evaluate(env)
        
        if isinstance(range_val, list) and len(range_val) == 2:
            start = range_val[0]
            end = range_val[1]
        else:
            raise TypeError("Ожидается диапазон в формате start:end")
        
        decimals = self.decimals.evaluate(env)
        if not isinstance(decimals, (int, float)):
            decimals = int(decimals)
        else:
            decimals = int(decimals)
        
        if decimals == 0:
            return random.randint(int(start), int(end))
        else:
            return round(random.uniform(float(start), float(end)), decimals)
    
    def execute(self, env):
        return self.evaluate(env)
    
    def __repr__(self):
        return f"Random({self.range_node}, {self.decimals})"


class PrintShowNode(Node):
    def __init__(self, title, data):
        self.title = title
        self.data = data
    
    def execute(self, env):
        if isinstance(self.data, str):
            matrix_obj = env.get(self.data)
        else:
            matrix_obj = self.data.evaluate(env)
        
        if not hasattr(matrix_obj, 'data') or not hasattr(matrix_obj, 'rows'):
            raise TypeError("PrintShow работает только с матрицами!")
        
        if self.title is None:
            title_text = "Матрица"
        else:
            title_text = str(self.title.evaluate(env)) if hasattr(self.title, 'evaluate') else str(self.title)
            if title_text == "":
                title_text = "Матрица"
        
        root = tk.Toplevel()
        root.title(title_text)
        root.geometry("800x500")
        
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame)
        v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        table_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")
        
        col_widths = []
        for j in range(matrix_obj.cols):
            max_width = 80
            for i in range(matrix_obj.rows):
                cell = str(matrix_obj.data[i][j])
                width = len(cell) * 10 + 20
                if width > max_width:
                    max_width = width
            col_widths.append(max_width)
        
        for i in range(matrix_obj.rows):
            for j in range(matrix_obj.cols):
                value = matrix_obj.data[i][j]
                cell_text = str(value)
                
                cell = tk.Label(table_frame, text=cell_text, 
                               bg="white", font=("Consolas", 10),
                               width=col_widths[j]//8, height=1,
                               relief=tk.RAISED, bd=1)
                cell.grid(row=i, column=j, padx=1, pady=1, sticky="ew")
                
                coord = f"[{i+1}, {j+1}]"
                cell.bind("<Enter>", lambda e, c=cell, coord=coord: on_enter(c, coord))
                cell.bind("<Leave>", lambda e, c=cell: on_leave(c))
        
        def on_enter(cell, coord):
            cell.config(bg="#FFD54F", cursor="hand2")
            tooltip = tk.Toplevel(cell)
            tooltip.wm_overrideredirect(True)
            x = cell.winfo_rootx() + 10
            y = cell.winfo_rooty() + 10
            tooltip.geometry(f"+{x}+{y}")
            label = tk.Label(tooltip, text=coord, 
                           bg="#FFFFCC", fg="#333", 
                           font=("Arial", 10, "bold"),
                           relief=tk.SOLID, bd=1, padx=5, pady=2)
            label.pack()
            cell.tooltip = tooltip
        
        def on_leave(cell):
            cell.config(bg="white")
            if hasattr(cell, 'tooltip'):
                cell.tooltip.destroy()
                del cell.tooltip
        
        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        btn_close = tk.Button(root, text="✕ Закрыть", 
                             command=root.destroy,
                             font=("Arial", 12, "bold"),
                             bg="#f44336", fg="white",
                             padx=20, pady=5)
        btn_close.pack(pady=10)
        
        root.transient()
        root.grab_set()
        root.focus_force()
        root.wait_window()
    
    def __repr__(self):
        return f"PrintShow({self.title}; {self.data})"