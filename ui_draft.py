"""앞유리 사이드 몰딩 분석 프로그램의 화면 UI 기안(시안).

전체 화면 구성(레이아웃·색상·탭 구조)을 먼저 확인해 보기 위한 초안입니다.
데이터 처리 로직을 붙이기 전 단계라 CSV 로딩·전처리·모델 학습·예측 같은 기능은
아직 들어있지 않고, 버튼·콤보박스도 비활성화해 두었습니다. 탭을 눌러 화면
구성만 확인할 수 있습니다.

실행: pip install -r requirements.txt 후 python ui_draft.py
화면 순서는 데이터 입력 -> 전처리 -> 시각화 -> 리터러시 -> 모델링 -> 평가 -> 예측입니다.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# 화면에 표시할 타깃 변수 이름입니다.
TARGET_COLUMN = "PassOrFail"


class MoldingAnalysisApp(tk.Tk):
    """화면 배치만 담당하는 UI 기안 클래스입니다 (실제 분석 기능 없음)."""

    def __init__(self) -> None:
        super().__init__()
        self.title("앞유리 사이드 몰딩 데이터 분석 및 불량 예측")
        self.geometry("1500x900")
        self.minsize(1200, 760)
        self.configure(bg="#f1f5f9")

        # StringVar는 Tkinter 위젯에 표시되는 값을 관리합니다.
        self.file_path = tk.StringVar()
        self.target_var = tk.StringVar(value=TARGET_COLUMN)
        self.model_var = tk.StringVar(value="Random Forest")
        self.test_size_var = tk.StringVar(value="0.2")
        self.cv_var = tk.StringVar(value="5")
        self.status_var = tk.StringVar(value="UI 기안 화면입니다. 위쪽 탭을 눌러 화면 구성만 확인해 주세요. (데이터 입력·분석 기능 없음)")
        self.eda_feature_var = tk.StringVar()
        self.question_var = tk.StringVar(value="불량과 가장 관련이 큰 변수는 무엇인가요?")

        self._make_styles()
        self._build_header()
        self._build_layout()

    def _make_styles(self) -> None:
        """화면의 색상과 글꼴을 통일합니다."""
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f1f5f9")
        style.configure("Card.TFrame", background="#ffffff", relief="flat", borderwidth=0)
        style.configure("Sidebar.TFrame", background="#ffffff", relief="flat", borderwidth=0)
        style.configure("Header.TFrame", background="#0f172a", borderwidth=0)
        style.configure("TLabel", background="#f1f5f9", foreground="#334155", font=("Malgun Gothic", 10))
        style.configure("Card.TLabel", background="#ffffff", foreground="#334155", font=("Malgun Gothic", 10))
        style.configure("Sidebar.TLabel", background="#ffffff", foreground="#475569", font=("Malgun Gothic", 10))
        style.configure("Title.TLabel", background="#0f172a", foreground="#ffffff", font=("Malgun Gothic", 19, "bold"))
        style.configure("Subtitle.TLabel", background="#0f172a", foreground="#94a3b8", font=("Malgun Gothic", 9))
        style.configure("Section.TLabel", background="#f1f5f9", foreground="#1e3a8a", font=("Malgun Gothic", 12, "bold"))
        style.configure("SidebarSection.TLabel", background="#ffffff", foreground="#2563eb", font=("Malgun Gothic", 11, "bold"))
        style.configure("CardSection.TLabel", background="#ffffff", foreground="#1e3a8a", font=("Malgun Gothic", 12, "bold"))
        style.configure("CardValue.TLabel", background="#ffffff", foreground="#2563eb", font=("Malgun Gothic", 14, "bold"))
        style.configure("Blue.TButton", font=("Malgun Gothic", 10, "bold"), foreground="#ffffff", background="#2563eb", borderwidth=0, padding=(12, 9))
        style.map("Blue.TButton", background=[("pressed", "#1d4ed8"), ("active", "#3b82f6")])
        style.configure("Green.TButton", font=("Malgun Gothic", 10, "bold"), foreground="#ffffff", background="#059669", borderwidth=0, padding=(12, 9))
        style.map("Green.TButton", background=[("pressed", "#047857"), ("active", "#10b981")])
        style.configure("TButton", font=("Malgun Gothic", 9), padding=(10, 6), borderwidth=0)
        style.configure("TEntry", padding=7, fieldbackground="#ffffff", bordercolor="#cbd5e1", lightcolor="#cbd5e1", darkcolor="#cbd5e1")
        style.configure("TCombobox", padding=6, fieldbackground="#ffffff", bordercolor="#cbd5e1", arrowsize=14)
        style.configure("TRadiobutton", background="#ffffff", foreground="#334155", font=("Malgun Gothic", 10))
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#334155", rowheight=30, borderwidth=0, font=("Malgun Gothic", 9))
        style.configure("Treeview.Heading", background="#e2e8f0", foreground="#1e293b", relief="flat", padding=(8, 8), font=("Malgun Gothic", 9, "bold"))
        style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#1e3a8a")])
        style.map("Treeview.Heading", background=[("active", "#cbd5e1")])

        # 화살표와 입체 테두리를 없앤 얇은 파란색 스크롤바입니다.
        for orientation in ("Vertical", "Horizontal"):
            scrollbar_style = f"Modern.{orientation}.TScrollbar"
            style.configure(
                scrollbar_style,
                background="#60a5fa",
                troughcolor="#e2e8f0",
                bordercolor="#e2e8f0",
                lightcolor="#60a5fa",
                darkcolor="#60a5fa",
                relief="flat",
                borderwidth=0,
                arrowcolor="#2563eb",
                arrowsize=12,
                width=13,
            )
            style.map(
                scrollbar_style,
                background=[("pressed", "#2563eb"), ("active", "#3b82f6")],
            )

        # 운영체제 기본 레이아웃을 유지해야 Windows에서도 손잡이가 정상 표시됩니다.
        # 탭을 눌러도 크기는 바뀌지 않고 배경 명암으로만 선택 상태를 표시합니다.
        style.configure(
            "TNotebook.Tab",
            padding=(20, 10),
            font=("Malgun Gothic", 10, "bold"),
            background="#e2e8f0",
            foreground="#475569",
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#ffffff"), ("active", "#dbeafe")],
            foreground=[("selected", "#2563eb"), ("active", "#1d4ed8")],
            padding=[("selected", (20, 10)), ("active", (20, 10))],
        )
        # 기본 테마의 점선 포커스 요소를 제외하여 클릭 후 점선이 보이지 않게 합니다.
        style.layout(
            "TNotebook.Tab",
            [("Notebook.tab", {"sticky": "nswe", "children": [
                ("Notebook.padding", {"side": "top", "sticky": "nswe", "children": [
                    ("Notebook.label", {"side": "top", "sticky": ""})
                ]})
            ]})],
        )

    def _build_header(self) -> None:
        header = ttk.Frame(self, style="Header.TFrame", height=76)
        header.pack(fill="x")
        header.pack_propagate(False)
        title_box = ttk.Frame(header, style="Header.TFrame")
        title_box.pack(fill="both", expand=True, padx=26, pady=(12, 10))
        ttk.Label(title_box, text="앞유리 사이드 몰딩 품질 분석", style="Title.TLabel", anchor="w").pack(anchor="w")
        ttk.Label(title_box, text="Injection Molding Quality Analytics", style="Subtitle.TLabel", anchor="w").pack(anchor="w", pady=(2, 0))

    def _build_layout(self) -> None:
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=18, pady=16)
        self._build_control_panel(body)
        self._build_notebook(body)
        ttk.Label(self, textvariable=self.status_var, anchor="w", foreground="#64748b").pack(fill="x", padx=22, pady=(0, 10))

    def _build_control_panel(self, parent: ttk.Frame) -> None:
        """왼쪽에 파일, 타깃, 모델, 학습 설정을 배치합니다. (모두 비활성화 상태)"""
        panel = ttk.Frame(parent, width=330, style="Sidebar.TFrame", padding=(18, 16))
        panel.pack(side="left", fill="y", padx=(0, 16))
        panel.pack_propagate(False)

        ttk.Label(panel, text="1. 데이터 입력", style="SidebarSection.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(panel, text="CSV 파일 선택", style="Sidebar.TLabel").pack(anchor="w")
        file_row = ttk.Frame(panel, style="Sidebar.TFrame")
        file_row.pack(fill="x", pady=(5, 18))
        ttk.Entry(file_row, textvariable=self.file_path, state="disabled").pack(side="left", fill="x", expand=True)
        ttk.Button(file_row, text="열기", state="disabled").pack(side="left", padx=(6, 0))

        ttk.Label(panel, text="2. 문제 유형", style="SidebarSection.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Radiobutton(panel, text="분류(Classification)", value="classification", state="disabled").pack(anchor="w")
        ttk.Radiobutton(panel, text="회귀(Regression) - 이 데이터에서는 사용 안 함", state="disabled").pack(anchor="w", pady=(3, 10))
        ttk.Label(panel, text="타깃 변수", style="Sidebar.TLabel").pack(anchor="w")
        self.target_combo = ttk.Combobox(panel, textvariable=self.target_var, state="disabled")
        self.target_combo.pack(fill="x", pady=(5, 18))

        ttk.Label(panel, text="3. 모델 선택", style="SidebarSection.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Combobox(panel, textvariable=self.model_var, values=["Random Forest", "Logistic Regression"], state="disabled").pack(fill="x", pady=(0, 18))

        ttk.Label(panel, text="4. 학습/검증 설정", style="SidebarSection.TLabel").pack(anchor="w", pady=(0, 8))
        option_grid = ttk.Frame(panel, style="Sidebar.TFrame")
        option_grid.pack(fill="x")
        ttk.Label(option_grid, text="테스트 비율", style="Sidebar.TLabel").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Combobox(option_grid, textvariable=self.test_size_var, values=["0.2", "0.25", "0.3"], width=9, state="disabled").grid(row=0, column=1, sticky="e")
        ttk.Label(option_grid, text="교차검증", style="Sidebar.TLabel").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Combobox(option_grid, textvariable=self.cv_var, values=["3", "5"], width=9, state="disabled").grid(row=1, column=1, sticky="e")
        option_grid.columnconfigure(1, weight=1)

        ttk.Button(panel, text="① 모델 학습하기", style="Blue.TButton", state="disabled").pack(fill="x", pady=(24, 8), ipady=7)
        ttk.Button(panel, text="② 새 제품 예측하기", style="Green.TButton", state="disabled").pack(fill="x", ipady=7)

        info = ("※ PassOrFail은 0=양품, 1=불량으로 가정합니다.\n"
                "※ 불량이 매우 적으므로 정확도만으로 모델을 평가하면 안 됩니다.\n"
                "※ 이 화면은 UI 기안(시안)입니다. 탭 이동 외의 데이터 업로드·학습·예측 기능은 동작하지 않습니다.")
        ttk.Label(panel, text=info, style="Sidebar.TLabel", wraplength=285, foreground="#64748b").pack(anchor="w", pady=(22, 0))

    def _build_notebook(self, parent: ttk.Frame) -> None:
        self.notebook = ttk.Notebook(parent, takefocus=False)
        self.notebook.pack(side="left", fill="both", expand=True)
        self.data_tab = ttk.Frame(self.notebook)
        self.preprocessing_tab = ttk.Frame(self.notebook)
        self.eda_tab = ttk.Frame(self.notebook)
        self.qa_tab = ttk.Frame(self.notebook)
        self.model_tab = ttk.Frame(self.notebook)
        self.evaluation_tab = ttk.Frame(self.notebook)
        self.prediction_tab = ttk.Frame(self.notebook)
        for frame, title in [(self.data_tab, "데이터 입력"), (self.preprocessing_tab, "전처리"),
                             (self.eda_tab, "시각화(EDA)"), (self.qa_tab, "리터러시(Q→A)"),
                             (self.model_tab, "모델링"), (self.evaluation_tab, "평가"),
                             (self.prediction_tab, "예측 결과")]:
            self.notebook.add(frame, text=title)
        self._build_data_tab()
        self._build_preprocessing_tab()
        self._build_eda_tab()
        self._build_qa_tab()
        self._build_model_tab()
        self._build_evaluation_tab()
        self._build_prediction_tab()

    def _build_data_tab(self) -> None:
        top = ttk.Frame(self.data_tab)
        top.pack(fill="x", padx=16, pady=12)
        ttk.Label(top, text="이곳에서는 불러온 CSV의 행·열 개수와 실제 데이터를 확인합니다.").pack(anchor="w", pady=(0, 5))
        self.data_summary_label = ttk.Label(top, text="CSV를 불러오면 이 자리에 데이터 크기와 라벨 분포가 표시됩니다. (추후 구현 예정)", style="Section.TLabel")
        self.data_summary_label.pack(anchor="w")
        table_frame = ttk.Frame(self.data_tab, style="Card.TFrame")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.data_tree = ttk.Treeview(table_frame, show="headings")
        xbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.data_tree.xview, style="Modern.Horizontal.TScrollbar")
        ybar = ttk.Scrollbar(table_frame, orient="vertical", command=self.data_tree.yview, style="Modern.Vertical.TScrollbar")
        self.data_tree.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
        self.data_tree.grid(row=0, column=0, sticky="nsew")
        ybar.grid(row=0, column=1, sticky="ns")
        xbar.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def _build_preprocessing_tab(self) -> None:
        ttk.Label(self.preprocessing_tab, text="전처리란 분석 전에 빈 값, 중복 데이터, 필요 없는 열을 찾아 정리하는 과정입니다.").pack(anchor="w", padx=16, pady=(14, 0))
        self.preprocessing_text = tk.Text(self.preprocessing_tab, font=("Consolas", 11), bg="white", fg="#334155", relief="flat", borderwidth=0, padx=16, pady=14)
        self.preprocessing_text.pack(fill="both", expand=True, padx=16, pady=(8, 16))
        self._set_text(self.preprocessing_text, "CSV를 불러오면 이 자리에 전처리 점검 결과가 표시됩니다. (추후 구현 예정)")

    def _build_eda_tab(self) -> None:
        toolbar = ttk.Frame(self.eda_tab)
        toolbar.pack(fill="x", padx=16, pady=(12, 4))
        ttk.Label(toolbar, text="그래프로 양품과 불량의 차이 및 변수 간 관계를 살펴봅니다.   ").pack(side="left")
        ttk.Label(toolbar, text="상세 분석 변수:").pack(side="left")
        self.eda_combo = ttk.Combobox(toolbar, textvariable=self.eda_feature_var, state="disabled", width=30)
        self.eda_combo.pack(side="left", padx=8)
        ttk.Button(toolbar, text="그래프 새로고침", state="disabled").pack(side="left")
        self.eda_chart_frame = ttk.Frame(self.eda_tab, style="Card.TFrame")
        self.eda_chart_frame.pack(fill="both", expand=True, padx=16, pady=(4, 16))

    def _build_qa_tab(self) -> None:
        card = ttk.Frame(self.qa_tab, style="Card.TFrame")
        card.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(card, text="데이터 리터러시: 질문 → 해답", style="CardSection.TLabel").pack(anchor="w", padx=18, pady=(18, 10))
        self.question_combo = ttk.Combobox(card, textvariable=self.question_var, state="disabled", values=[
            "불량과 가장 관련이 큰 변수는 무엇인가요?", "데이터에서 주의할 품질 문제는 무엇인가요?",
            "정확도가 높으면 좋은 모델인가요?"])
        self.question_combo.pack(fill="x", padx=18, pady=6)
        ttk.Button(card, text="해답 보기", state="disabled").pack(anchor="e", padx=18, pady=6)
        self.answer_label = ttk.Label(card, text="질문을 선택하면 이 자리에 해답이 표시됩니다. (추후 구현 예정)", style="Card.TLabel", wraplength=900, justify="left")
        self.answer_label.pack(anchor="w", padx=18, pady=18)

    def _build_model_tab(self) -> None:
        self.model_text = tk.Text(self.model_tab, font=("Malgun Gothic", 11), bg="white", fg="#334155", relief="flat", borderwidth=0, padx=16, pady=14)
        self.model_text.pack(fill="both", expand=True, padx=16, pady=16)
        self._set_text(self.model_text, "모델 학습을 실행하면 이 자리에 학습 결과가 표시됩니다. (추후 구현 예정)")

    def _build_evaluation_tab(self) -> None:
        ttk.Label(
            self.evaluation_tab,
            text="평가 도움말: 불량을 놓치지 않는 것이 중요하므로 정확도보다 재현율(Recall)과 F1 점수를 함께 확인하세요.",
        ).pack(anchor="w", padx=16, pady=(14, 0))
        self.evaluation_top = ttk.Frame(self.evaluation_tab)
        self.evaluation_top.pack(fill="x", padx=16, pady=(8, 6))
        self.metric_labels: dict[str, ttk.Label] = {}
        metric_titles = {
            "Accuracy": "정확도\nAccuracy",
            "Precision": "정밀도\nPrecision",
            "Recall": "재현율\nRecall",
            "F1-Score": "종합 점수\nF1-Score",
            "ROC-AUC": "구분 능력\nROC-AUC",
        }
        for i, metric in enumerate(["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]):
            card = ttk.Frame(self.evaluation_top, style="Card.TFrame")
            card.grid(row=0, column=i, sticky="nsew", padx=4)
            ttk.Label(card, text=metric_titles[metric], style="Card.TLabel", justify="center").pack(padx=18, pady=(10, 3))
            label = ttk.Label(card, text="-", style="CardValue.TLabel")
            label.pack(padx=18, pady=(0, 10))
            self.metric_labels[metric] = label
            self.evaluation_top.columnconfigure(i, weight=1)
        self.evaluation_chart_frame = ttk.Frame(self.evaluation_tab, style="Card.TFrame")
        self.evaluation_chart_frame.pack(fill="both", expand=True, padx=16, pady=(6, 16))

    def _build_prediction_tab(self) -> None:
        outer = ttk.Frame(self.prediction_tab)
        outer.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(outer, text="공정값 입력", style="Section.TLabel").pack(anchor="w")
        ttk.Label(outer, text="CSV를 불러오면 각 변수의 중앙값이 이 자리에 자동 입력되는 화면입니다. (추후 구현 예정)").pack(anchor="w", pady=(2, 8))
        canvas = tk.Canvas(outer, bg="white", highlightthickness=1, highlightbackground="#d5deea")
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview, style="Modern.Vertical.TScrollbar")
        self.input_frame = ttk.Frame(canvas, style="Card.TFrame")
        self.input_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        self.input_window = canvas.create_window((0, 0), window=self.input_frame, anchor="nw")
        # 창 크기가 바뀌면 입력 프레임도 캔버스 폭에 맞춰져 오른쪽 값이 잘리지 않습니다.
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(self.input_window, width=event.width),
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")
        result_card = ttk.Frame(outer, style="Card.TFrame", width=270)
        result_card.pack(side="left", fill="y", padx=(12, 0))
        result_card.pack_propagate(False)
        ttk.Label(result_card, text="예측 결과", style="CardSection.TLabel").pack(pady=(30, 12))
        self.prediction_result_label = ttk.Label(result_card, text="모델 학습 전", style="Card.TLabel", font=("Malgun Gothic", 18, "bold"), wraplength=230)
        self.prediction_result_label.pack(padx=16, pady=12)
        self.prediction_probability_label = ttk.Label(result_card, text="", style="Card.TLabel", wraplength=230)
        self.prediction_probability_label.pack(padx=16, pady=6)

    # 반복되는 보조 기능 ----------------------------------------------------
    @staticmethod
    def _set_text(widget: tk.Text, content: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.configure(state="disabled")


def main() -> None:
    """이 파일을 직접 실행했을 때 Tkinter 프로그램을 시작합니다."""
    app = MoldingAnalysisApp()
    app.mainloop()


if __name__ == "__main__":
    main()
