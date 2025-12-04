from tkinter import Frame, Button, StringVar, Entry, Label, Toplevel

class Weather_Window(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # window styling
        self.title('Weather information')
        self.an = self.winfo_screenwidth()
        self.al = self.winfo_screenheight()
        self.tam = '%dx%d'%(self.an,self.al)
        self.geometry(self.tam)
        self.configure(bg="#5d7fa1")

        # --- Header ---
        self.header = Frame(self,  bg="#dfeaf5")
        self.header.pack(fill="x", pady=(20, 8))

        self.title_label = Label(
            self.header, text='Weather Info',
            font=('Helvetica', 56, 'bold'),
            bg="#deeeff", fg="#1f2b33",height=2
        )
        self.title_label.pack()

        self.subtitle_label = Label(
            self.header,
            text='Search by ZIP to see current conditions',
            font=('Helvetica', 38),
            fg="#000000", bg="#dfeaf5"
        )
        self.subtitle_label.pack(pady=(6, 1))

        # --- Content split ---
        self.content = Frame(self, bg="#abbac9")
        self.content.pack(fill="both", expand=True, padx=24, pady=12)

        self.left = Frame(self.content, bg="#ecf3fb")
        self.left.pack(side='left', fill='y', padx=(12, 12))

        self.right = Frame(self.content, bg="#466d93")
        self.right.pack(side='right', fill='both', expand=True, padx=(15, 0))

        # CTA + result card
        self.start_button()
        self._build_result_card()

    # ---------- UI pieces ----------
    def start_button(self):
        self.start_btn = Button(
            self.left, text="Start", command=self.show_searchbar,
            bg="#1c5e7d", fg="white", bd=20,
            font=("Helvetica", 44, "bold"),
            activebackground="#040404", activeforeground="white",
            relief="raised", padx=16, pady=10, cursor="hand2",
            highlightthickness=2, highlightbackground="#23434d",
            highlightcolor="#ffffff", width=10
        )
        self.start_btn.pack(pady=16, ipadx=12)
        self.start_btn.bind("<Enter>", lambda e: e.widget.configure(bg="#2d4b5a"))
        self.start_btn.bind("<Leave>", lambda e: e.widget.configure(bg="#2e4865"))

    def show_searchbar(self):
        if hasattr(self, "start_btn") and self.start_btn.winfo_exists():
            self.start_btn.destroy()

        self.search_group = Frame(self.left, bg="#62a4c2", width=15)
        self.search_group.pack(padx=5, pady=30, fill="x")

        self.search_wrap = Frame(self.search_group, bg="#396392")
        self.search_wrap.pack(side='left',fill="x", padx=5, pady=20)

        self.search_var = StringVar()
        placeholder = "Enter ZIP code..."

        self.search_entry = Entry(
            self.search_wrap, textvariable=self.search_var,
            font=("Helvetica", 38), bg="#f0f8ff", fg="#95a5a6",
            relief="flat", insertbackground="#2c3e50",
            highlightthickness=1, highlightbackground="#132232",
            highlightcolor="#ccd6f1", width=15
        )
        self.search_entry.pack(side="left", fill="x", expand=True,
                               ipady=10, padx=(18, 8), pady=5)
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
            font=("Helvetica", 33, "bold"),
            bg="#263f56", fg="white",
            activebackground="#99B3ED", activeforeground="white",
            relief="raised", bd=25, command=self._do_search
        )
        self.search_button.pack(side="right", padx=(5, 15),
                                pady=5, ipadx=15, ipady=8)
        self.search_button.bind("<Enter>", lambda e: e.widget.configure(bg="#1F2B3D"))
        self.search_button.bind("<Leave>", lambda e: e.widget.configure(bg="#2B3B54"))

        self.status = Label(self.left, text="", bg="#334f69", fg='#e0f2f1',
        font=("Helvetica", 44))
        self.status.pack(anchor='w', pady=(12, 4))

    def _build_result_card(self):
        # Outer card
        self.card = Frame(self.right, bg="#1d3245")
        self.card.pack(fill="both", expand=True, pady=6)

        # Inner content surface
        self.card_inner = Frame(self.card, bg="#d4edf8")
        self.card_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # Location
        self.loc_label = Label(
            self.card_inner, text="Location Unknown",
            font=("Helvetica", 48, "bold"),
            fg="#ecfeff", bg="#192745", width=18
        )
        self.loc_label.pack(anchor="w", pady=(4, 10))

        # Temperature big
        self.temp_label = Label(
            self.card_inner, text="Unknown",
            font=("Helvetica", 48, "bold"),
            fg="#ecfeff", bg="#192745", width=18
        )
        self.temp_label.pack(anchor="w", pady=(4, 10))

        # Condition pill
        self.cond_wrap = Frame(self.card_inner, bg="#39dcf9")
        self.cond_wrap.pack(anchor="w", pady=(0, 10))
        self.cond_pill = Label(
            self.cond_wrap, text="Unknown",
            font=("Helvetica", 48, "bold"),
            fg="#100b3f", bg="#5f9c9d",
            padx=10, pady=4
        )
        self.cond_pill.pack(side="left")

    # ---------- Logic ----------
    def _do_search(self):
        query = self.search_var.get().strip() if hasattr(self, 'search_var') else ""
        if not query or "Enter ZIP" in query:
            self._set_status("Type a ZIP first.")
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
