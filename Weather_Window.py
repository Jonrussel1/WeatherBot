from tkinter import Frame, Button, StringVar, Entry, Label, Toplevel

class Weather_Window(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # window styling
        self.title('Weather information')
        self.geometry("800x600")
        self.configure(bg='teal')

        # --- Header ---
        self.header = Frame(self, bg='teal')
        self.header.pack(fill="x", pady=(18, 6))

        self.title_label = Label(
            self.header, text='Weather Info',
            font=('Helvetica', 30, 'bold'),
            fg='white', bg='teal'
        )
        self.title_label.pack()

        self.subtitle_label = Label(
            self.header,
            text='Search by ZIP or "lat, lon" to see current conditions',
            font=('Helvetica', 12),
            fg='#e0f2f1', bg='teal'
        )
        self.subtitle_label.pack(pady=(4, 0))

        # --- Content split ---
        self.content = Frame(self, bg='teal')
        self.content.pack(fill="both", expand=True, padx=24, pady=12)

        self.left = Frame(self.content, bg='teal')
        self.left.pack(side='left', fill='y', padx=(0, 12))

        self.right = Frame(self.content, bg='teal')
        self.right.pack(side='right', fill='both', expand=True, padx=(12, 0))

        # CTA + result card
        self.start_button()
        self._build_result_card()

    # ---------- UI pieces ----------
    def start_button(self):
        self.start_btn = Button(
            self.left, text="Start", command=self.show_searchbar,
            bg="#0ea5e9", fg="white", bd=0,
            font=("Helvetica", 14, "bold"),
            activebackground="#0284c7", activeforeground="white",
            relief="flat", padx=16, pady=10, cursor="hand2",
            highlightthickness=2, highlightbackground="teal",
            highlightcolor="#38bdf8"
        )
        self.start_btn.pack(pady=16, ipadx=4)
        self.start_btn.bind("<Enter>", lambda e: e.widget.configure(bg="#0284c7"))
        self.start_btn.bind("<Leave>", lambda e: e.widget.configure(bg="#0ea5e9"))

    def show_searchbar(self):
        if hasattr(self, "start_btn") and self.start_btn.winfo_exists():
            self.start_btn.destroy()

        self.search_group = Frame(self.left, bg="teal")
        self.search_group.pack(pady=8, fill="x")

        self.search_wrap = Frame(self.search_group, bg="#008080")
        self.search_wrap.pack(fill="x", padx=2, pady=2)

        self.search_var = StringVar()
        placeholder = "Enter ZIP or coordinates (lat, lon)"

        self.search_entry = Entry(
            self.search_wrap, textvariable=self.search_var,
            font=("Helvetica", 12), bg="#f0f8ff", fg="#95a5a6",
            relief="flat", insertbackground="#2c3e50",
            highlightthickness=1, highlightbackground="#008080",
            highlightcolor="#00a0a0"
        )
        self.search_entry.pack(side="left", fill="x", expand=True,
                               ipady=10, padx=(15, 5), pady=5)
        self.search_var.set(placeholder)

        def on_entry_click(_):
            if self.search_var.get() == placeholder:
                self.search_var.set("")
                self.search_entry.config(fg="#2c3e50")

        def on_focusout(_):
            if self.search_var.get().strip() == "":
                self.search_var.set(placeholder)
                self.search_entry.config(fg="#95a5a6")

        self.search_entry.bind("<FocusIn>", on_entry_click)
        self.search_entry.bind("<FocusOut>", on_focusout)
        self.search_entry.bind("<Return>", lambda _e: self._do_search())

        self.search_button = Button(
            self.search_wrap, text="🔍 Search",
            font=("Helvetica", 11, "bold"),
            bg="#00a0a0", fg="white",
            activebackground="#008080", activeforeground="white",
            relief="flat", bd=0, command=self._do_search
        )
        self.search_button.pack(side="right", padx=(5, 15),
                                pady=5, ipadx=15, ipady=8)
        self.search_button.bind("<Enter>", lambda e: e.widget.configure(bg="#008080"))
        self.search_button.bind("<Leave>", lambda e: e.widget.configure(bg="#00a0a0"))

        self.status = Label(self.left, text="", bg='teal', fg='#e0f2f1',
                            font=("Helvetica", 10))
        self.status.pack(anchor='w', pady=(6, 0))

    def _build_result_card(self):
        # Outer card
        self.card = Frame(self.right, bg="#0d9488")
        self.card.pack(fill="both", expand=True, pady=6)

        # Inner content surface
        self.card_inner = Frame(self.card, bg="#134e4a")
        self.card_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # Location
        self.loc_label = Label(
            self.card_inner, text="Location —",
            font=("Helvetica", 18, "bold"),
            fg="#ecfeff", bg="#134e4a"
        )
        self.loc_label.pack(anchor="w", pady=(2, 6))

        # Temperature big
        self.temp_label = Label(
            self.card_inner, text="— °",
            font=("Helvetica", 44, "bold"),
            fg="#a7f3d0", bg="#134e4a"
        )
        self.temp_label.pack(anchor="w", pady=(2, 2))

        # Condition pill
        self.cond_wrap = Frame(self.card_inner, bg="#134e4a")
        self.cond_wrap.pack(anchor="w", pady=(0, 10))
        self.cond_pill = Label(
            self.cond_wrap, text="—",
            font=("Helvetica", 12, "bold"),
            fg="#064e3b", bg="#a7f3d0",
            padx=10, pady=4
        )
        self.cond_pill.pack(side="left")

    # ---------- Logic ----------
    def _do_search(self):
        query = self.search_var.get().strip() if hasattr(self, 'search_var') else ""
        if not query or "Enter ZIP" in query:
            self._set_status("Type a ZIP or coordinates first.")
            return

        try:
            _ = self.master.Get_Weather(query)  # updates self.master.forecast
            fc = getattr(self.master, "forecast", None)

            if isinstance(fc, dict):
                location = fc.get("location", "—")
                temp = fc.get("temp", "—")
                weather = fc.get("weather", "—")
            else:
                location, temp, weather = "—", "—", str(_)

            self._render_summary(location, temp, weather)
            self._set_status("Updated ✓")
        except Exception as e:
            self._render_summary("—", "—", "Error")
            self._set_status(f"Error: {e}")

    def _render_summary(self, location, temp, weather):
        self.loc_label.config(text=location)
        s = str(temp)
        if "°" not in s:
            s = f"{s}°"
        self.temp_label.config(text=s)
        pretty = (weather or "—").strip().title()
        self.cond_pill.config(text=pretty)

    def _set_status(self, msg):
        if hasattr(self, "status"):
            self.status.config(text=msg)
