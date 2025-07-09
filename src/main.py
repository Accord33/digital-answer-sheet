import tkinter as tk
from tkinter import ttk


class AnswerGetterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("デジタル回答用紙")
        self.root.geometry("1200x750")
        self.root.configure(bg='lightgray')
        
        # 四角の数
        self.num_boxes = 100
        
        # 現在の位置（どの四角に次の入力をするか）
        self.current_position = 0
        
        # 各四角の状態を保持するリスト（None, "○", "×"）
        self.box_states = [None] * self.num_boxes
        
        # 入力パターン（右矢印で○、左矢印で×）
        self.input_pattern = "○"
        
        self.setup_ui()
        self.setup_bindings()
        
        # フォーカスを設定してキー入力を受け取れるようにする
        self.root.focus_set()
    
    def setup_ui(self):
        # メインフレーム
        main_frame = tk.Frame(self.root, bg='lightgray')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # タイトル
        title_label = tk.Label(main_frame, text="デジタル回答用紙", 
                              font=('Arial', 24, 'bold'), 
                              bg='lightgray', fg='darkblue')
        title_label.pack(pady=(0, 30))
        
        # 四角を配置するフレーム
        boxes_frame = tk.Frame(main_frame, bg='lightgray')
        boxes_frame.pack(pady=20)
        
        # 四角のリストを作成（横20個×5段）
        self.boxes = []
        boxes_per_row = 20
        
        for row in range(5):  # 5段
            row_frame = tk.Frame(boxes_frame, bg='lightgray')
            row_frame.pack(pady=5)
            
            for col in range(boxes_per_row):  # 1行あたり20個
                # 各四角とその番号を含むコンテナフレーム
                box_container = tk.Frame(row_frame, bg='lightgray')
                box_container.pack(side='left', padx=2)
                
                # 四角
                box_index = row * boxes_per_row + col
                box = tk.Label(box_container, text="", 
                              width=4, height=2,
                              relief='raised', borderwidth=1,
                              bg='white', fg='black',
                              font=('Arial', 20, 'bold'))
                box.pack()
                
                # クリックイベントを追加
                box.bind("<Button-1>", lambda event, idx=box_index: self.on_box_click(idx))
                
                # 番号ラベル
                box_number = row * boxes_per_row + col + 1
                number_label = tk.Label(box_container, text=str(box_number),
                                       font=('Arial', 10),
                                       bg='lightgray', fg='darkblue')
                number_label.pack()
                
                self.boxes.append(box)
        
        # 現在位置を示すインジケーター
        indicator_frame = tk.Frame(main_frame, bg='lightgray')
        indicator_frame.pack(pady=15)
        
        self.position_label = tk.Label(indicator_frame, 
                                      text=f"現在位置: {self.current_position + 1}",
                                      font=('Arial', 14),
                                      bg='lightgray', fg='darkgreen')
        self.position_label.pack()
        
        # 操作説明
        instruction_label = tk.Label(main_frame, 
                                   text="右矢印キー: ○   左矢印キー: ×",
                                   font=('Arial', 12),
                                   bg='lightgray', fg='black')
        instruction_label.pack(pady=8)
        
        # リセットボタン
        reset_button = tk.Button(main_frame, text="リセット", 
                                font=('Arial', 14, 'bold'),
                                bg='red', fg='white',
                                command=self.reset_boxes,
                                width=10, height=2)
        reset_button.pack(pady=15)
        
        self.update_display()
    
    def setup_bindings(self):
        # キーバインドを設定
        self.root.bind('<Right>', self.on_right_arrow)
        self.root.bind('<Left>', self.on_left_arrow)
        self.root.bind('<Return>', self.reset_boxes)  # Enterキーでもリセット可能
    
    def on_box_click(self, box_index):
        """四角がクリックされた時の処理（その位置にカーソルを移動）"""
        self.current_position = box_index
        self.update_display()
        # フォーカスを戻す
        self.root.focus_set()
    
    def on_right_arrow(self, event):
        """右矢印キーが押された時の処理（○を入力）"""
        if self.current_position < self.num_boxes:
            self.box_states[self.current_position] = "○"
            # 最後の問題でなければ次に進む
            if self.current_position < self.num_boxes - 1:
                self.current_position += 1
            self.update_display()
    
    def on_left_arrow(self, event):
        """左矢印キーが押された時の処理（×を入力）"""
        if self.current_position < self.num_boxes:
            self.box_states[self.current_position] = "×"
            # 最後の問題でなければ次に進む
            if self.current_position < self.num_boxes - 1:
                self.current_position += 1
            self.update_display()
    
    def reset_boxes(self, event=None):
        """全ての四角をリセット"""
        self.box_states = [None] * self.num_boxes
        self.current_position = 0
        self.update_display()
    
    def update_display(self):
        """画面の表示を更新"""
        # 各四角の表示を更新
        for i, box in enumerate(self.boxes):
            if i == self.current_position:
                # 現在位置をハイライト（記入済みかどうかに関わらず青色）
                if self.box_states[i] is not None:
                    # 記入済みの場合は○×を表示しつつ青い背景
                    box.config(text=self.box_states[i], bg='lightblue', fg='darkblue')
                else:
                    # 未記入の場合は空で青い背景
                    box.config(text="", bg='lightblue', fg='black')
            elif self.box_states[i] is not None:
                # 記入済みで現在位置ではない場合は黄色背景
                box.config(text=self.box_states[i], bg='lightyellow', fg='black')
            else:
                # 未記入で現在位置ではない場合は白背景
                box.config(text="", bg='white', fg='black')
        
        # 位置ラベルを更新
        if self.current_position < self.num_boxes:
            self.position_label.config(text=f"現在位置: {self.current_position + 1}")
        else:
            self.position_label.config(text="入力完了")


def main():
    root = tk.Tk()
    app = AnswerGetterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
