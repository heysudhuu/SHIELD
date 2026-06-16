import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
from datetime import datetime

# Import local modules
from modules.password_generator import generate_password
from modules.password_checker import check_password_strength
from modules.hash_checker import calculate_file_hash, verify_file_integrity
from modules.educational_info import get_port_scanning_info, get_network_scanning_info, get_vulnerability_catalog

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

class CyberToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ SHIELD//CORE - Personal Security Console")
        self.root.geometry("1160x740")
        self.root.minsize(1020, 680)

        # Set up project paths
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.reports_dir = os.path.join(self.project_dir, "reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
        self.history_file = os.path.join(self.project_dir, "scan_history.json")
        self.history = self.load_history()

        # Theme Variables (Dark Mode default)
        self.dark_mode = True
        
        # High-Tech HSL / Neon Color Palette (Cyber Sentry Theme)
        self.colors = {
            "dark": {
                "bg": "#090911",           # Midnight Space Base
                "sidebar": "#040408",      # Abyss Deep Black
                "card": "#101021",         # Dark Slate Card
                "fg": "#e1e6f0",           # Cold Ice White Text
                "fg_dim": "#7c89a3",       # Muted Blue-grey Text
                "accent_blue": "#00f2fe",  # Cyber Neon Cyan
                "accent_green": "#00ff87", # Cyber Neon Green
                "accent_red": "#ff075b",   # Cyber Neon Red
                "accent_yellow": "#ffea00",# Cyber Neon Yellow
                "border": "#1c1c38",       # Cyber Cobalt Border
                "btn_bg": "#161630",       # Deep Cobalt Button
                "btn_active": "#22224d",   # Brightened Cobalt Hover
                "console": "#020205"       # Pure Black console screen
            },
            "light": {
                "bg": "#f0f4f8",           # Soft clean light grey
                "sidebar": "#e1e8f0",      # Light slate sidebar
                "card": "#ffffff",         # Plain white cards
                "fg": "#1a202c",           # Dark charcoal text
                "fg_dim": "#718096",       # Slate grey text
                "accent_blue": "#3182ce",  # Steel Blue
                "accent_green": "#38a169", # Forest Green
                "accent_red": "#e53e3e",   # Crimson Red
                "accent_yellow": "#dd6b20",# Dark Amber Yellow
                "border": "#cbd5e0",       # Clean light borders
                "btn_bg": "#e2e8f0",       # Soft light grey button
                "btn_active": "#cbd5e0",   # Selected state
                "console": "#f7fafc"       # White terminal
            }
        }

        # Configure Fonts
        self.font_family = "Segoe UI"
        self.root.option_add("*Font", (self.font_family, 10))

        # Setup custom Ttk styles for select elements (Scrollbars, Comboboxes)
        self.style = ttk.Style()
        self.configure_ttk_styles()

        # Tracking running simulation timers to allow cancellation
        self.active_sim_timer = None

        # Build UI layout
        self.setup_ui_layout()
        
        # Select first tab by default
        self.select_tab("password_gen")

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_history(self, action_type, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "type": action_type,
            "description": description
        }
        self.history.insert(0, entry)
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")
        
        if hasattr(self, "history_listbox"):
            self.refresh_history_ui()

    def get_color(self, key):
        theme = "dark" if self.dark_mode else "light"
        return self.colors[theme][key]

    def configure_ttk_styles(self):
        theme = "clam"
        self.style.theme_use(theme)

        bg = self.get_color("bg")
        fg = self.get_color("fg")
        border = self.get_color("border")
        btn_bg = self.get_color("btn_bg")

        # Scrollbar custom styling
        self.style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background=btn_bg,
            troughcolor=bg,
            bordercolor=bg,
            arrowcolor=fg,
            lightcolor=bg,
            darkcolor=bg
        )
        self.style.map(
            "Vertical.TScrollbar",
            background=[("active", self.get_color("btn_active"))]
        )

        # Combobox / OptionMenu custom styling
        self.style.configure(
            "TCombobox",
            font=(self.font_family, 10),
            fieldbackground=bg,
            background=btn_bg,
            foreground=fg,
            bordercolor=border,
            arrowcolor=fg,
            darkcolor=bg,
            lightcolor=bg
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", bg)],
            foreground=[("readonly", fg)]
        )

    def draw_round_rect(self, canvas, x1, y1, x2, y2, radius=8, **kwargs):
        """Draws a rounded capsule on a Tkinter canvas using a smooth polygon path."""
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    # ==========================================
    # Custom Modern UI Widget Factories
    # ==========================================
    def create_custom_button(self, parent, text, command, accent="default", font_size=10, font_weight="bold", **kwargs):
        """Creates a modern flat button with built-in cursor shapes and hover states."""
        theme_fg = self.get_color("fg")
        card_color = self.get_color("card")
        
        if accent == "blue":
            bg = self.get_color("accent_blue")
            fg = "#040408" if self.dark_mode else "#ffffff"
            hover_bg = "#80f8ff" if self.dark_mode else "#2b6cb0"
        elif accent == "green":
            bg = self.get_color("accent_green")
            fg = "#040408" if self.dark_mode else "#ffffff"
            hover_bg = "#80ffc3" if self.dark_mode else "#2f855a"
        elif accent == "red":
            bg = self.get_color("accent_red")
            fg = "#040408" if self.dark_mode else "#ffffff"
            hover_bg = "#ff80ac" if self.dark_mode else "#c53030"
        else: # Default gray style
            bg = self.get_color("btn_bg")
            fg = theme_fg
            hover_bg = self.get_color("btn_active")

        btn = tk.Button(
            parent,
            text=text,
            font=(self.font_family, font_size, font_weight),
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            command=command,
            **kwargs
        )

        def on_enter(e):
            if btn.cget("state") != "disabled":
                btn.config(bg=hover_bg)

        def on_leave(e):
            if btn.cget("state") != "disabled":
                btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_custom_entry(self, parent, textvariable=None, show=None, state="normal", **kwargs):
        """Creates a modern input entry that glows its borders when selected."""
        bg = self.get_color("bg")
        fg = self.get_color("fg")
        border = self.get_color("border")
        accent = self.get_color("accent_blue")

        entry = tk.Entry(
            parent,
            textvariable=textvariable,
            show=show,
            state=state,
            font=("Consolas", 11) if show else (self.font_family, 10),
            bg=bg,
            fg=fg,
            bd=0,
            highlightthickness=1,
            highlightbackground=border,
            highlightcolor=accent, # Glow accent when focused
            insertbackground=fg,   # cursor matches text color
            **kwargs
        )
        return entry

    def create_card_frame(self, parent, **kwargs):
        """Creates a neat padded card frame styled with thin borders for containing controls."""
        return tk.Frame(
            parent, 
            bg=self.get_color("card"),
            highlightthickness=1, 
            highlightbackground=self.get_color("border"),
            padx=28, 
            pady=24,
            **kwargs
        )

    # ==========================================
    # Main Sidebar and Layout Setup
    # ==========================================
    def setup_ui_layout(self):
        theme_bg = self.get_color("bg")
        theme_sidebar = self.get_color("sidebar")
        theme_fg = self.get_color("fg")

        self.root.configure(bg=theme_bg)

        # Sidebar Panel
        self.sidebar = tk.Frame(self.root, bg=theme_sidebar, width=250, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Right Content Viewport
        self.content_area = tk.Frame(self.root, bg=theme_bg)
        self.content_area.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        # Logo / Title (Cyberpunk Shield Core Branding)
        self.logo_frame = tk.Frame(self.sidebar, bg=theme_sidebar, pady=25)
        self.logo_frame.pack(fill="x", padx=15)

        self.logo_label = tk.Label(
            self.logo_frame, 
            text="🛡️ SHIELD // CORE", 
            font=(self.font_family, 14, "bold"), 
            bg=theme_sidebar, 
            fg=self.get_color("accent_blue"),
            anchor="w"
        )
        self.logo_label.pack(fill="x")

        self.sublogo_label = tk.Label(
            self.logo_frame, 
            text="PERSONAL SECURITY CONSOLE", 
            font=("Courier New", 8, "bold"), 
            bg=theme_sidebar, 
            fg=self.get_color("fg_dim"),
            anchor="w"
        )
        self.sublogo_label.pack(fill="x", pady=(2, 0))

        # Navigation Buttons Setup - VS Code style left vertical accent bars!
        self.nav_buttons = {}
        self.nav_indicators = {}
        tabs = [
            ("password_gen", "🔑 Password Gen"),
            ("password_check", "🛡️ Strength Checker"),
            ("port_scanner", "🌐 Port Scanner (Edu)"),
            ("network_scanner", "📡 Network Scanner (Edu)"),
            ("hash_checker", "🔍 File Hash Checker"),
            ("history_reports", "📜 History & Reports")
        ]

        for tab_id, label in tabs:
            # Container Frame for each navigation item
            item_frame = tk.Frame(self.sidebar, bg=theme_sidebar)
            item_frame.pack(fill="x", pady=2)

            # Left vertical indicator bar (lights up neon cyan when active)
            ind = tk.Frame(item_frame, bg=theme_sidebar, width=4)
            ind.pack(side="left", fill="y")
            self.nav_indicators[tab_id] = ind

            btn = tk.Button(
                item_frame,
                text=label,
                font=(self.font_family, 10, "bold"),
                bg=theme_sidebar,
                fg=theme_fg,
                activebackground=self.get_color("btn_active"),
                activeforeground=theme_fg,
                bd=0,
                padx=20,
                pady=11,
                anchor="w",
                cursor="hand2",
                command=lambda tid=tab_id: self.select_tab(tid)
            )
            btn.pack(side="right", fill="x", expand=True)
            self.nav_buttons[tab_id] = btn

            # Attach hover behaviors
            def on_enter(e, b=btn, tid=tab_id):
                if self.current_tab != tid:
                    b.config(bg=self.get_color("btn_bg"))
            def on_leave(e, b=btn, tid=tab_id):
                if self.current_tab != tid:
                    b.config(bg=theme_sidebar)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Theme & Exit Toggles (Sidebar Bottom)
        self.theme_btn = tk.Button(
            self.sidebar,
            text="🌙 Dark Mode" if self.dark_mode else "☀ Light Mode",
            font=(self.font_family, 9, "bold"),
            bg=self.get_color("btn_bg"),
            fg=theme_fg,
            bd=0,
            pady=9,
            cursor="hand2",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="bottom", fill="x", padx=16, pady=(5, 12))

        self.exit_btn = tk.Button(
            self.sidebar,
            text="Exit Application",
            font=(self.font_family, 9, "bold"),
            bg=self.get_color("btn_bg"),
            fg=self.get_color("accent_red"),
            bd=0,
            pady=9,
            cursor="hand2",
            command=self.root.quit
        )
        self.exit_btn.pack(side="bottom", fill="x", padx=16, pady=5)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.theme_btn.config(text="🌙 Dark Mode" if self.dark_mode else "☀ Light Mode")
        
        # Cancel any active simulation animation timers to avoid race conditions
        self.cancel_sim_timer()

        # Re-apply styling variables
        self.configure_ttk_styles()

        theme_bg = self.get_color("bg")
        theme_sidebar = self.get_color("sidebar")
        theme_fg = self.get_color("fg")

        self.root.configure(bg=theme_bg)
        self.sidebar.config(bg=theme_sidebar)
        self.logo_label.config(bg=theme_sidebar, fg=self.get_color("accent_blue"))
        self.sublogo_label.config(bg=theme_sidebar, fg=self.get_color("fg_dim"))
        self.content_area.config(bg=theme_bg)

        # Refresh sidebar styles
        for tab_id, btn in self.nav_buttons.items():
            btn.config(
                bg=theme_sidebar,
                fg=theme_fg,
                activebackground=self.get_color("btn_active"),
                activeforeground=theme_fg
            )
        self.theme_btn.config(bg=self.get_color("btn_bg"), fg=theme_fg)
        self.exit_btn.config(bg=self.get_color("btn_bg"), fg=self.get_color("accent_red"))

        # Re-draw the active page view
        self.select_tab(self.current_tab)

    def select_tab(self, tab_id):
        self.current_tab = tab_id
        
        # Cancel any active simulation animation timers to avoid background crashes
        self.cancel_sim_timer()

        # Clear out current viewport frame contents
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Update button highlights and indicator states
        theme_sidebar = self.get_color("sidebar")
        theme_btn_bg = self.get_color("btn_bg")
        for tid, btn in self.nav_buttons.items():
            ind = self.nav_indicators[tid]
            if tid == tab_id:
                btn.config(bg=theme_btn_bg, fg=self.get_color("accent_blue"))
                ind.config(bg=self.get_color("accent_blue"))
            else:
                btn.config(bg=theme_sidebar, fg=self.get_color("fg"))
                ind.config(bg=theme_sidebar)

        # Render selected tool module
        if tab_id == "password_gen":
            self.render_password_generator()
        elif tab_id == "password_check":
            self.render_password_checker()
        elif tab_id == "port_scanner":
            self.render_port_scanner_edu()
        elif tab_id == "network_scanner":
            self.render_network_scanner_edu()
        elif tab_id == "hash_checker":
            self.render_hash_checker()
        elif tab_id == "history_reports":
            self.render_history_reports()

    def cancel_sim_timer(self):
        if self.active_sim_timer:
            try:
                self.root.after_cancel(self.active_sim_timer)
            except Exception:
                pass
            self.active_sim_timer = None

    def copy_to_clipboard(self, text, indicator_label):
        if HAS_PYPERCLIP:
            pyperclip.copy(text)
        else:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        
        # Temp feedback notice
        original_text = indicator_label.cget("text")
        indicator_label.config(text="✓ Copied!", fg=self.get_color("accent_green"))
        self.root.after(1500, lambda: indicator_label.config(text=original_text, fg=self.get_color("fg_dim")))

    # ==========================================
    # Module View 1: Password Generator UI
    # ==========================================
    def render_password_generator(self):
        bg_color = self.get_color("bg")
        card_color = self.get_color("card")
        fg_color = self.get_color("fg")
        dim_color = self.get_color("fg_dim")

        # Container Panel
        card = self.create_card_frame(self.content_area)
        card.pack(fill="both", expand=True)

        # Header Info
        header = tk.Label(card, text="🔑 Cryptographically Secure Password Generator", font=(self.font_family, 15, "bold"), bg=card_color, fg=self.get_color("accent_blue"))
        header.pack(anchor="w", pady=(0, 4))

        sub = tk.Label(card, text="Generates random password using cryptographically secure parameters (secrets module).", font=(self.font_family, 10), bg=card_color, fg=dim_color)
        sub.pack(anchor="w", pady=(0, 20))

        # Main horizontal split
        body_frame = tk.Frame(card, bg=card_color)
        body_frame.pack(fill="both", expand=True)

        # Left Panel (Settings)
        left_panel = tk.Frame(body_frame, bg=card_color)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Length Setting (Sleek [ - ] [ 16 ] [ + ] decrement/increment controls!)
        len_frame = tk.Frame(left_panel, bg=card_color)
        len_frame.pack(fill="x", pady=(10, 15))

        len_label = tk.Label(len_frame, text="Password Length:", font=(self.font_family, 10, "bold"), bg=card_color, fg=fg_color)
        len_label.pack(side="left", pady=5)

        # Length variable
        self.pass_len_var = tk.IntVar(value=16)

        def dec_len():
            val = self.pass_len_var.get()
            if val > 6:
                self.pass_len_var.set(val - 1)

        def inc_len():
            val = self.pass_len_var.get()
            if val < 128:
                self.pass_len_var.set(val + 1)

        dec_btn = self.create_custom_button(len_frame, text="-", command=dec_len, font_size=10, font_weight="bold")
        dec_btn.pack(side="left", padx=(15, 0))
        dec_btn.config(pady=3, padx=12)

        len_val_lbl = tk.Label(len_frame, textvariable=self.pass_len_var, font=(self.font_family, 11, "bold"), bg=card_color, fg=self.get_color("accent_blue"), width=4)
        len_val_lbl.pack(side="left", padx=5)

        inc_btn = self.create_custom_button(len_frame, text="+", command=inc_len, font_size=10, font_weight="bold")
        inc_btn.pack(side="left")
        inc_btn.config(pady=3, padx=12)

        # Config Checkboxes
        self.opt_upper = tk.BooleanVar(value=True)
        self.opt_lower = tk.BooleanVar(value=True)
        self.opt_digits = tk.BooleanVar(value=True)
        self.opt_special = tk.BooleanVar(value=True)

        chk_opts = [
            ("Include Uppercase Letters (A-Z)", self.opt_upper),
            ("Include Lowercase Letters (a-z)", self.opt_lower),
            ("Include Numeric Digits (0-9)", self.opt_digits),
            ("Include Special Symbols (!@#$...)", self.opt_special)
        ]

        for label_text, var in chk_opts:
            chk = tk.Checkbutton(
                left_panel, 
                text=label_text, 
                variable=var, 
                font=(self.font_family, 10),
                bg=card_color, 
                fg=fg_color, 
                activebackground=card_color,
                activeforeground=fg_color,
                selectcolor=bg_color if self.dark_mode else "#ffffff",
                bd=0,
                pady=5
            )
            chk.pack(anchor="w")

        # Action Trigger
        gen_btn = self.create_custom_button(
            left_panel,
            text="Generate Password",
            command=self.on_generate_password,
            accent="blue"
        )
        gen_btn.pack(anchor="w", pady=(25, 0))

        # Right Panel (Output Display & Visual Feedback)
        right_panel = tk.Frame(body_frame, bg=card_color, highlightthickness=1, highlightbackground=self.get_color("border"), padx=25, pady=25)
        right_panel.pack(side="right", fill="both", expand=True, padx=(20, 0))

        result_title = tk.Label(right_panel, text="Generated Output", font=(self.font_family, 11, "bold"), bg=card_color, fg=fg_color)
        result_title.pack(anchor="w", pady=(0, 5))

        self.pass_output_var = tk.StringVar(value="Click 'Generate Password'...")
        self.pass_output_entry = tk.Entry(
            right_panel, 
            textvariable=self.pass_output_var, 
            font=("Consolas", 13), 
            state="readonly",
            bg=bg_color, 
            readonlybackground=bg_color,
            fg=self.get_color("accent_green") if self.dark_mode else fg_color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.get_color("border"),
            justify="center"
        )
        self.pass_output_entry.pack(fill="x", pady=12, ipady=10)

        # Copy & Status Indicator Frame
        copy_frame = tk.Frame(right_panel, bg=card_color)
        copy_frame.pack(fill="x", pady=5)

        self.copy_status_lbl = tk.Label(copy_frame, text="Generate to enable options", font=(self.font_family, 9), bg=card_color, fg=dim_color)
        self.copy_status_lbl.pack(side="left")

        copy_btn = self.create_custom_button(
            copy_frame,
            text="Copy to Clipboard",
            command=lambda: self.copy_to_clipboard(self.pass_output_var.get(), self.copy_status_lbl)
        )
        copy_btn.pack(side="right")

        # Visual indicator of strength
        self.gen_strength_lbl = tk.Label(right_panel, text="Strength Score: -", font=(self.font_family, 10, "bold"), bg=card_color, fg=dim_color)
        self.gen_strength_lbl.pack(anchor="w", pady=(25, 5))

    def on_generate_password(self):
        length = self.pass_len_var.get()
        upper = self.opt_upper.get()
        lower = self.opt_lower.get()
        digits = self.opt_digits.get()
        special = self.opt_special.get()

        try:
            password = generate_password(length, upper, lower, digits, special)
            self.pass_output_entry.config(state="normal")
            self.pass_output_var.set(password)
            self.pass_output_entry.config(state="readonly")
            
            # Auto evaluate strength
            analysis = check_password_strength(password)
            score_color = self.get_score_color(analysis["score"])
            self.gen_strength_lbl.config(
                text=f"Estimated Strength: {analysis['strength']} ({analysis['score']}/5)",
                fg=score_color
            )

            self.copy_status_lbl.config(text="Password successfully generated.", fg=self.get_color("fg_dim"))

            # Record Event
            self.save_history("Password Generation", f"Generated secure {length}-character password (Score: {analysis['score']}/5)")
        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Generation failed: {e}")

    # ==========================================
    # Module View 2: Strength Analyzer UI
    # ==========================================
    def render_password_checker(self):
        card_color = self.get_color("card")
        fg_color = self.get_color("fg")
        dim_color = self.get_color("fg_dim")
        bg_color = self.get_color("bg")

        card = self.create_card_frame(self.content_area)
        card.pack(fill="both", expand=True)

        # Header Info
        header = tk.Label(card, text="🛡️ Password Strength & Complexity Analyzer", font=(self.font_family, 15, "bold"), bg=card_color, fg=self.get_color("accent_blue"))
        header.pack(anchor="w", pady=(0, 4))

        sub = tk.Label(card, text="Check password security characteristics and verify complexity baselines in real-time.", font=(self.font_family, 10), bg=card_color, fg=dim_color)
        sub.pack(anchor="w", pady=(0, 20))

        # Input field
        entry_lbl = tk.Label(card, text="Input Password to Analyze:", font=(self.font_family, 10, "bold"), bg=card_color, fg=fg_color)
        entry_lbl.pack(anchor="w", pady=(0, 5))

        entry_frame = tk.Frame(card, bg=card_color)
        entry_frame.pack(fill="x", pady=(0, 20))

        self.check_pass_var = tk.StringVar()
        self.check_pass_var.trace_add("write", self.on_check_password_change)

        self.check_pass_entry = self.create_custom_entry(entry_frame, textvariable=self.check_pass_var, show="*")
        self.check_pass_entry.pack(side="left", fill="x", expand=True, ipady=8)

        self.mask_var = tk.BooleanVar(value=True)
        self.show_hide_btn = self.create_custom_button(
            entry_frame,
            text="👁 Show",
            command=self.toggle_password_visibility
        )
        self.show_hide_btn.pack(side="right", padx=(12, 0))

        # Panel Split: Left (Score details & progress bar) | Right (Security Checklist)
        metrics_panel = tk.Frame(card, bg=card_color)
        metrics_panel.pack(fill="both", expand=True)

        left_col = tk.Frame(metrics_panel, bg=card_color)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))

        self.score_val_lbl = tk.Label(left_col, text="Score: 0 / 5", font=(self.font_family, 18, "bold"), bg=card_color, fg=dim_color)
        self.score_val_lbl.pack(anchor="w", pady=(10, 2))

        self.strength_lbl = tk.Label(left_col, text="Strength: Enter text...", font=(self.font_family, 13, "bold"), bg=card_color, fg=dim_color)
        self.strength_lbl.pack(anchor="w", pady=(2, 10))

        # Custom canvas segmented progress bar (high-tech dashboard style!)
        self.prog_canvas = tk.Canvas(left_col, height=22, bg=card_color, highlightthickness=0)
        self.prog_canvas.pack(fill="x", pady=15)
        self.prog_canvas.bind("<Configure>", lambda e: self.draw_segmented_progress_bar(0))

        # Statically create the "Record Result" button here to prevent dynamic layout jumps and TclErrors!
        self.save_chk_btn = self.create_custom_button(
            left_col,
            text="Record Result to History",
            command=self.log_strength_check
        )
        self.save_chk_btn.pack(anchor="w", pady=(15, 0))

        # Right Column (Checklist Grid)
        right_col = tk.Frame(metrics_panel, bg=card_color, highlightthickness=1, highlightbackground=self.get_color("border"), padx=20, pady=20)
        right_col.pack(side="right", fill="both", expand=True, padx=(20, 0))

        chk_title = tk.Label(right_col, text="Security Requirements", font=(self.font_family, 11, "bold"), bg=card_color, fg=fg_color)
        chk_title.pack(anchor="w", pady=(0, 12))

        self.chk_labels = {}
        criteria = [
            ("length", "Length is at least 10 characters"),
            ("uppercase", "Contains uppercase letters (A-Z)"),
            ("lowercase", "Contains lowercase letters (a-z)"),
            ("digits", "Contains numeric digits (0-9)"),
            ("special", "Contains special characters (!@#$...)")
        ]

        for key, text in criteria:
            lbl = tk.Label(right_col, text=f"⚪  {text}", font=(self.font_family, 10), bg=card_color, fg=dim_color, anchor="w")
            lbl.pack(fill="x", pady=5)
            self.chk_labels[key] = lbl

    def toggle_password_visibility(self):
        masked = self.mask_var.get()
        if masked:
            self.check_pass_entry.config(show="")
            self.show_hide_btn.config(text="🙈 Hide")
            self.mask_var.set(False)
        else:
            self.check_pass_entry.config(show="*")
            self.show_hide_btn.config(text="👁 Show")
            self.mask_var.set(True)

    def draw_segmented_progress_bar(self, score):
        """Draws a premium 5-segment capsule indicator bar representing password strength."""
        self.prog_canvas.delete("all")
        width = self.prog_canvas.winfo_width()
        if width <= 1:
            width = 320
        height = 18
        
        # 5 distinct neon capsules
        gap = 6
        seg_width = int((width - (gap * 4)) / 5.0)
        
        color = self.get_score_color(score)
        
        for i in range(5):
            x1 = i * (seg_width + gap)
            x2 = x1 + seg_width
            
            # If segment index is below score, light it up; else draw disabled border
            if i < score:
                self.draw_round_rect(self.prog_canvas, x1, 2, x2, height-2, radius=4, fill=color, outline="")
            else:
                self.draw_round_rect(self.prog_canvas, x1, 2, x2, height-2, radius=4, fill=self.get_color("border"), outline="")

    def get_score_color(self, score):
        if score <= 2:
            return self.get_color("accent_red")
        elif score <= 4:
            return self.get_color("accent_yellow")
        else:
            return self.get_color("accent_green")

    def on_check_password_change(self, *args):
        # Prevent accessing widgets that may have been destroyed during tab switching
        try:
            if not self.check_pass_entry.winfo_exists():
                return
        except Exception:
            return

        password = self.check_pass_var.get()
        if not password:
            self.score_val_lbl.config(text="Score: 0 / 5", fg=self.get_color("fg_dim"))
            self.strength_lbl.config(text="Strength: Enter text...", fg=self.get_color("fg_dim"))
            self.draw_segmented_progress_bar(0)
            for lbl in self.chk_labels.values():
                original_text = lbl.cget("text")[3:]
                lbl.config(text=f"⚪  {original_text}", fg=self.get_color("fg_dim"))
            return

        analysis = check_password_strength(password)
        score = analysis["score"]
        strength = analysis["strength"]
        checks = analysis["checks"]

        score_color = self.get_score_color(score)
        self.score_val_lbl.config(text=f"Score: {score} / 5", fg=score_color)
        self.strength_lbl.config(text=f"Strength: {strength}", fg=score_color)
        
        self.draw_segmented_progress_bar(score)

        for key, passed in checks.items():
            lbl = self.chk_labels[key]
            original_text = lbl.cget("text")[3:]
            if passed:
                lbl.config(text=f"✓  {original_text}", fg=self.get_color("accent_green"))
            else:
                lbl.config(text=f"✗  {original_text}", fg=self.get_color("accent_red"))

    def log_strength_check(self):
        password = self.check_pass_var.get()
        if not password:
            messagebox.showwarning("Empty Password", "Please enter a password to analyze first.")
            return
        analysis = check_password_strength(password)
        masked_pass = password[0] + "*" * (len(password) - 1) if len(password) > 1 else "*"
        self.save_history("Password Strength Check", f"Assessed strength for '{masked_pass}' (Score: {analysis['score']}/5 - {analysis['strength']})")
        messagebox.showinfo("Log Saved", "Strength audit results successfully written to history log.")

    # ==========================================
    # Module View 3: Port Scanner (Educational Simulator)
    # ==========================================
    def render_port_scanner_edu(self):
        card_color = self.get_color("card")
        fg_color = self.get_color("fg")
        dim_color = self.get_color("fg_dim")
        bg_color = self.get_color("bg")

        card = self.create_card_frame(self.content_area)
        card.pack(fill="both", expand=True)

        header = tk.Label(card, text="🌐 Interactive Port Scanner (Educational Simulator)", font=(self.font_family, 15, "bold"), bg=card_color, fg=self.get_color("accent_blue"))
        header.pack(anchor="w", pady=(0, 4))

        sub = tk.Label(card, text="Simulates active port scans (like TCP Connect/SYN) to illustrate how target discovery works without sending network traffic.", font=(self.font_family, 10), bg=card_color, fg=dim_color)
        sub.pack(anchor="w", pady=(0, 20))

        # Input Zone
        input_frame = tk.Frame(card, bg=card_color)
        input_frame.pack(fill="x", pady=10)

        ip_lbl = tk.Label(input_frame, text="Target IP Address:", font=(self.font_family, 10, "bold"), bg=card_color, fg=fg_color)
        ip_lbl.pack(side="left")

        self.sim_ip_var = tk.StringVar(value="192.168.1.1")
        ip_entry = self.create_custom_entry(input_frame, textvariable=self.sim_ip_var, width=15)
        ip_entry.pack(side="left", padx=12, ipady=6)

        run_sim_btn = self.create_custom_button(
            input_frame,
            text="Simulate Scan Audit",
            command=self.run_port_scan_simulation,
            accent="blue"
        )
        run_sim_btn.pack(side="left", padx=5)

        # Simulation Console View (Styled dark terminal)
        console_frame = tk.Frame(card, bg=self.get_color("console"), highlightthickness=1, highlightbackground=self.get_color("border"))
        console_frame.pack(fill="both", expand=True, pady=(15, 0))

        scrollbar = ttk.Scrollbar(console_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.sim_console = tk.Text(
            console_frame,
            bg=self.get_color("console"),
            fg="#a6e3a1" if self.dark_mode else "#2d3748",
            insertbackground="#ffffff" if self.dark_mode else "#000000",
            font=("Consolas", 10),
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            padx=15,
            pady=15,
            state="disabled"
        )
        self.sim_console.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.sim_console.yview)

        # Configure console tags for syntax color highlighting
        self.sim_console.tag_config("info", foreground=dim_color)
        self.sim_console.tag_config("send", foreground=self.get_color("accent_blue"))
        self.sim_console.tag_config("receive", foreground=self.get_color("accent_green"))
        self.sim_console.tag_config("warn", foreground=self.get_color("accent_red"))
        self.sim_console.tag_config("closed", foreground="#6c7086" if self.dark_mode else "#718096")
        self.sim_console.tag_config("success", foreground=self.get_color("accent_green"), font=("Consolas", 10, "bold"))

        # Pre-populate console with welcome instructions
        self.sim_console.config(state="normal")
        self.sim_console.insert(tk.END, "[~] Educational simulator initialized.\n[~] Enter a target IP and click 'Simulate Scan Audit' to observe how SYN scans discover open ports and services theoretically.\n", "info")
        self.sim_console.config(state="disabled")

    def run_port_scan_simulation(self):
        target_ip = self.sim_ip_var.get().strip()
        if not target_ip:
            messagebox.showwarning("Target Missing", "Please enter a simulated target IP address.")
            return

        self.cancel_sim_timer()
        
        self.sim_console.config(state="normal")
        self.sim_console.delete("1.0", tk.END)
        self.sim_console.config(state="disabled")
        
        simulation_steps = [
            ("info", f"[~] Initializing Simulated TCP SYN Scan on target: {target_ip}...\n"),
            ("send", "[*] Sending TCP SYN packet to Port 21 (FTP)...\n"),
            ("receive", "[+] Received SYN-ACK from Port 21. STATUS: OPEN\n"),
            ("warn", "    --> VULNERABILITY RISK: Anonymous FTP access allowed. Cleartext credentials.\n"),
            ("info", "    --> REMEDIATION: Disable anonymous access, upgrade to SFTP.\n\n"),
            
            ("send", "[*] Sending TCP SYN packet to Port 22 (SSH)...\n"),
            ("receive", "[+] Received SYN-ACK from Port 22. STATUS: OPEN\n"),
            ("info", "    --> BEST PRACTICE: Disable password logins, enforce SSH keys, restrict allowed IPs.\n\n"),
            
            ("send", "[*] Sending TCP SYN packet to Port 23 (Telnet)...\n"),
            ("closed", "[-] Port 23 connection timed out. STATUS: CLOSED/FILTERED\n"),
            ("info", "    --> NOTE: Secured. Telnet is disabled or dropped by host firewall.\n\n"),
            
            ("send", "[*] Sending TCP SYN packet to Port 80 (HTTP)...\n"),
            ("receive", "[+] Received SYN-ACK from Port 80. STATUS: OPEN\n"),
            ("warn", "    --> VULNERABILITY RISK: Plaintext HTTP traffic is susceptible to sniffing.\n"),
            ("info", "    --> REMEDIATION: Enforce HSTS and redirect all HTTP traffic to Port 443 (HTTPS).\n\n"),
            
            ("send", "[*] Sending TCP SYN packet to Port 445 (SMB)...\n"),
            ("receive", "[+] Received SYN-ACK from Port 445. STATUS: OPEN\n"),
            ("warn", "    --> VULNERABILITY RISK: Direct SMB exposure is highly targeted (e.g. EternalBlue).\n"),
            ("info", "    --> REMEDIATION: Block port 445 at firewall boundary, disable SMBv1.\n\n"),
            
            ("success", f"[✓] Simulated scan completed. 4 open ports identified on {target_ip}. Audit logs successfully compiled.\n")
        ]
        
        self.run_sim_step(0, simulation_steps, self.sim_console, "Port Scan")

    def run_sim_step(self, index, steps, console_widget, action_name):
        try:
            if not console_widget.winfo_exists():
                return
        except Exception:
            return

        if index >= len(steps):
            self.save_history(f"Simulated {action_name}", f"Completed simulated sweep showing vulnerabilities for security reference.")
            self.active_sim_timer = None
            return
            
        tag, text = steps[index]
        console_widget.config(state="normal")
        console_widget.insert(tk.END, text, tag)
        console_widget.see(tk.END)
        console_widget.config(state="disabled")
        
        # Animate step execution
        self.active_sim_timer = self.root.after(800, lambda: self.run_sim_step(index + 1, steps, console_widget, action_name))

    # ==========================================
    # Module View 4: Network Scanner (Educational Simulator)
    # ==========================================
    def render_network_scanner_edu(self):
        card_color = self.get_color("card")
        fg_color = self.get_color("fg")
        dim_color = self.get_color("fg_dim")
        bg_color = self.get_color("bg")

        card = self.create_card_frame(self.content_area)
        card.pack(fill="both", expand=True)

        header = tk.Label(card, text="📡 Interactive Network Host Discovery (Educational Simulator)", font=(self.font_family, 15, "bold"), bg=card_color, fg=self.get_color("accent_blue"))
        header.pack(anchor="w", pady=(0, 4))

        sub = tk.Label(card, text="Simulates subnet sweeps (using ARP and ICMP) to demonstrate local device mapping without performing physical network packet broadcasts.", font=(self.font_family, 10), bg=card_color, fg=dim_color)
        sub.pack(anchor="w", pady=(0, 20))

        # Input Zone
        input_frame = tk.Frame(card, bg=card_color)
        input_frame.pack(fill="x", pady=10)

        subnet_lbl = tk.Label(input_frame, text="Subnet Range:", font=(self.font_family, 10, "bold"), bg=card_color, fg=fg_color)
        subnet_lbl.pack(side="left")

        self.sim_subnet_var = tk.StringVar(value="192.168.1.0/24")
        subnet_entry = self.create_custom_entry(input_frame, textvariable=self.sim_subnet_var, width=15)
        subnet_entry.pack(side="left", padx=12, ipady=6)

        run_sim_btn = self.create_custom_button(
            input_frame,
            text="Simulate Subnet Discovery",
            command=self.run_network_scan_simulation,
            accent="blue"
        )
        run_sim_btn.pack(side="left", padx=5)

        # Simulation Console View (Styled dark terminal)
        console_frame = tk.Frame(card, bg=self.get_color("console"), highlightthickness=1, highlightbackground=self.get_color("border"))
        console_frame.pack(fill="both", expand=True, pady=(15, 0))

        scrollbar = ttk.Scrollbar(console_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.net_sim_console = tk.Text(
            console_frame,
            bg=self.get_color("console"),
            fg="#a6e3a1" if self.dark_mode else "#2d3748",
            insertbackground="#ffffff" if self.dark_mode else "#000000",
            font=("Consolas", 10),
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            padx=15,
            pady=15,
            state="disabled"
        )
        self.net_sim_console.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.net_sim_console.yview)

        # Configure console tags
        self.net_sim_console.tag_config("info", foreground=dim_color)
        self.net_sim_console.tag_config("send", foreground=self.get_color("accent_blue"))
        self.net_sim_console.tag_config("receive", foreground=self.get_color("accent_green"))
        self.net_sim_console.tag_config("warn", foreground=self.get_color("accent_yellow"))
        self.net_sim_console.tag_config("closed", foreground="#6c7086" if self.dark_mode else "#718096")
        self.net_sim_console.tag_config("success", foreground=self.get_color("accent_green"), font=("Consolas", 10, "bold"))

        # Pre-populate console
        self.net_sim_console.config(state="normal")
        self.net_sim_console.insert(tk.END, "[~] Network mapping simulator initialized.\n[~] Enter a subnet and click 'Simulate Subnet Discovery' to view how ARP scanning maps active nodes theoretically.\n", "info")
        self.net_sim_console.config(state="disabled")

    def run_network_scan_simulation(self):
        subnet = self.sim_subnet_var.get().strip()
        if not subnet:
            messagebox.showwarning("Subnet Missing", "Please enter a simulated subnet range (e.g. 192.168.1.0/24).")
            return

        self.cancel_sim_timer()
        
        self.net_sim_console.config(state="normal")
        self.net_sim_console.delete("1.0", tk.END)
        self.net_sim_console.config(state="disabled")
        
        simulation_steps = [
            ("info", f"[~] Initializing Simulated Local Subnet Sweep on: {subnet}...\n"),
            ("send", f"[*] Broadasting ARP requests on local segment (Layer 2 Host Discovery)...\n\n"),
            
            ("receive", "[+] Host Mapped: 192.168.1.2\n"),
            ("info", "    --> MAC Address: 00:1A:2B:3C:4D:5E\n"),
            ("info", "    --> Device Type: workstation-laptop (Windows Client OS)\n"),
            ("info", "    --> Host Security baseline: Active. Inbound ICMP requests are dropped.\n\n"),
            
            ("receive", "[+] Host Mapped: 192.168.1.5\n"),
            ("info", "    --> MAC Address: 70:89:76:54:32:10\n"),
            ("info", "    --> Device Type: mobile-handset (Android Client)\n"),
            ("warn", "    --> Security Advisory: Open HTTP services active (sniffing vector).\n\n"),
            
            ("receive", "[+] Host Mapped: 192.168.1.8\n"),
            ("info", "    --> MAC Address: B4:75:0E:1F:2A:3B\n"),
            ("info", "    --> Device Type: iot-appliance (SmartTV Unit)\n"),
            ("warn", "    --> Security Advisory: Exposed Universal Plug and Play (UPnP) daemon.\n\n"),
            
            ("send", "[*] Initiating ICMP Echo pings to verify non-local segments (Layer 3 host discovery)...\n"),
            ("closed", "[-] No active responding nodes discovered outside immediate segment.\n\n"),
            
            ("success", f"[✓] Subnet mapping sweep completed. 3 active devices identified on subnet range {subnet}.\n")
        ]
        
        self.run_sim_step(0, simulation_steps, self.net_sim_console, "Network Scan")

    # ==========================================
    # Module View 5: Hash Integrity Checker UI
    # ==========================================
    def render_hash_checker(self):
        card_color = self.get_color("card")
        fg_color = self.get_color("fg")
        dim_color = self.get_color("fg_dim")
        bg_color = self.get_color("bg")

        card = self.create_card_frame(self.content_area)
        card.pack(fill="both", expand=True)

        # Header Info
        header = tk.Label(card, text="🔍 Cryptographic File Hash Integrity Checker", font=(self.font_family, 15, "bold"), bg=card_color, fg=self.get_color("accent_blue"))
        header.pack(anchor="w", pady=(0, 4))

        sub = tk.Label(card, text="Verify file integrity and authenticity by computing and comparing standard SHA256/SHA1/MD5 checksums.", font=(self.font_family, 10), bg=card_color, fg=dim_color)
        sub.pack(anchor="w", pady=(0, 15))

        # 1. Custom File Picker Box (looks like a modern dashed drag zone!)
        picker_zone = tk.Canvas(card, bg=bg_color, height=110, highlightthickness=0)
        picker_zone.pack(fill="x", pady=10)
        
        # Draw dotted border on canvas load
        def draw_picker_border(event, canvas=picker_zone):
            canvas.delete("border")
            w = canvas.winfo_width()
            self.draw_round_rect(canvas, 2, 2, w-2, 108, radius=6, fill=bg_color, outline=self.get_color("border"), tags="border")
            # Draw dashed inner line
            canvas.create_rectangle(6, 6, w-6, 104, dash=(4, 4), outline=self.get_color("border"), tags="border")
            
        picker_zone.bind("<Configure>", draw_picker_border)

        # Inner frame for widgets placed inside the canvas
        inner_frame = tk.Frame(picker_zone, bg=bg_color)
        picker_zone.create_window((10, 10), window=inner_frame, anchor="nw")
        
        # Make inner_frame pack elements vertically
        lbl_instr = tk.Label(inner_frame, text="📁 Click 'Browse File' to select a target file for integrity checks", font=(self.font_family, 10, "bold"), bg=bg_color, fg=fg_color)
        lbl_instr.pack(anchor="w", padx=15, pady=(8, 2))

        file_select_row = tk.Frame(inner_frame, bg=bg_color)
        file_select_row.pack(fill="x", expand=True, padx=15, pady=5)

        self.file_path_var = tk.StringVar()
        self.file_path_entry = tk.Entry(
            file_select_row, 
            textvariable=self.file_path_var, 
            font=(self.font_family, 9), 
            state="readonly",
            bg=card_color, 
            readonlybackground=card_color,
            fg=fg_color, 
            bd=0, 
            highlightthickness=1,
            highlightbackground=self.get_color("border"),
            width=65
        )
        self.file_path_entry.pack(side="left", fill="x", ipady=6)

        browse_btn = self.create_custom_button(
            file_select_row,
            text="Browse File...",
            command=self.browse_file
        )
        browse_btn.pack(side="left", padx=(12, 0))
        browse_btn.config(pady=4)

        # Update inner window width based on canvas configure
        def on_picker_resize(e, frame=inner_frame):
            w = e.width - 20
            frame.config(width=w)
            
        picker_zone.bind("<Configure>", lambda e: (draw_picker_border(e), on_picker_resize(e)))

        # 2. Config options (Algorithm select)
        algo_frame = tk.Frame(card, bg=card_color)
        algo_frame.pack(fill="x", pady=10)

        algo_lbl = tk.Label(algo_frame, text="Cryptographic Hash Algorithm:", font=(self.font_family, 10, "bold"), bg=card_color, fg=fg_color)
        algo_lbl.pack(side="left")

        self.hash_algo_var = tk.StringVar(value="SHA-256")
        
        # Using styled Ttk Combobox instead of legacy OptionMenu
        self.hash_combo = ttk.Combobox(
            algo_frame, 
            textvariable=self.hash_algo_var, 
            values=["SHA-256", "SHA-1", "MD5"],
            state="readonly",
            width=12
        )
        self.hash_combo.pack(side="left", padx=15)

        # Action Trigger
        calc_btn = self.create_custom_button(
            card,
            text="Compute Checksum",
            command=self.on_calculate_hash,
            accent="blue"
        )
        calc_btn.pack(anchor="w", pady=10)

        # 3. Output results section
        self.results_frame = tk.Frame(card, bg=card_color, highlightthickness=1, highlightbackground=self.get_color("border"), padx=20, pady=15)
        self.results_frame.pack(fill="x", pady=15)

        calculated_title = tk.Label(self.results_frame, text="Calculated Checksum Hash", font=(self.font_family, 10, "bold"), bg=card_color, fg=fg_color)
        calculated_title.pack(anchor="w")

        self.computed_hash_var = tk.StringVar(value="Calculated hash will display here...")
        self.computed_hash_entry = tk.Entry(
            self.results_frame,
            textvariable=self.computed_hash_var,
            font=("Consolas", 10),
            state="readonly",
            bg=bg_color,
            readonlybackground=bg_color,
            fg=self.get_color("accent_blue") if self.dark_mode else fg_color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.get_color("border")
        )
        self.computed_hash_entry.pack(fill="x", pady=8, ipady=7)

        # Integrity Validation Entry
        compare_lbl = tk.Label(self.results_frame, text="Verify Integrity (Paste Expected Checksum):", font=(self.font_family, 10, "bold"), bg=card_color, fg=fg_color)
        compare_lbl.pack(anchor="w", pady=(15, 5))

        compare_frame = tk.Frame(self.results_frame, bg=card_color)
        compare_frame.pack(fill="x")

        self.expected_hash_var = tk.StringVar()
        self.expected_hash_var.trace_add("write", self.on_expected_hash_change)
        
        self.expected_hash_entry = self.create_custom_entry(compare_frame, textvariable=self.expected_hash_var)
        self.expected_hash_entry.pack(side="left", fill="x", expand=True, ipady=6)

        self.match_lbl = tk.Label(compare_frame, text="No Expected Hash", font=(self.font_family, 9, "bold"), bg=card_color, fg=dim_color)
        self.match_lbl.pack(side="right", padx=(15, 0))

    def browse_file(self):
        filepath = filedialog.askopenfilename(title="Select Target File")
        if filepath:
            self.file_path_var.set(filepath)
            self.computed_hash_var.set("Click 'Compute Checksum' to calculate...")
            self.expected_hash_var.set("")
            self.match_lbl.config(text="No Expected Hash", fg=self.get_color("fg_dim"))

    def on_calculate_hash(self):
        filepath = self.file_path_var.get()
        if not filepath:
            messagebox.showwarning("File Missing", "Please select a file to hash first.")
            return

        algo = self.hash_algo_var.get()
        try:
            checksum = calculate_file_hash(filepath, algo)
            
            self.computed_hash_entry.config(state="normal")
            self.computed_hash_var.set(checksum)
            self.computed_hash_entry.config(state="readonly")

            self.on_expected_hash_change()

            filename = os.path.basename(filepath)
            self.save_history("File Hashing", f"Computed {algo} checksum for '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"Checksum calculation failed: {e}")

    def on_expected_hash_change(self, *args):
        # Prevent accessing widgets that may have been destroyed during tab switching
        try:
            if not self.computed_hash_entry.winfo_exists():
                return
        except Exception:
            return

        computed = self.computed_hash_var.get()
        expected = self.expected_hash_var.get().strip()

        if len(computed) < 10 or "Click '" in computed or not expected:
            self.match_lbl.config(text="No Expected Hash", fg=self.get_color("fg_dim"))
            return

        if computed.lower() == expected.lower():
            self.match_lbl.config(text="✓ MATCH (INTEGRITY SECURED)", fg=self.get_color("accent_green"))
        else:
            self.match_lbl.config(text="✗ MISMATCH (TAMPER DETECTED)", fg=self.get_color("accent_red"))

    # ==========================================
    # Module View 6: History & Assessment Reports
    # ==========================================
    def render_history_reports(self):
        card_color = self.get_color("card")
        fg_color = self.get_color("fg")
        dim_color = self.get_color("fg_dim")
        bg_color = self.get_color("bg")

        card = self.create_card_frame(self.content_area)
        card.pack(fill="both", expand=True)

        # Header Info
        header = tk.Label(card, text="📜 Activity Log & Report Exporter", font=(self.font_family, 15, "bold"), bg=card_color, fg=self.get_color("accent_blue"))
        header.pack(anchor="w", pady=(0, 4))

        sub = tk.Label(card, text="Review audit action records and export standard assessment reports.", font=(self.font_family, 10), bg=card_color, fg=dim_color)
        sub.pack(anchor="w", pady=(0, 20))

        # Control Panel buttons
        btn_frame = tk.Frame(card, bg=card_color)
        btn_frame.pack(fill="x", pady=(0, 15))

        clear_btn = self.create_custom_button(
            btn_frame,
            text="Clear Log History",
            command=self.clear_history,
            accent="red"
        )
        clear_btn.pack(side="left")

        export_btn = self.create_custom_button(
            btn_frame,
            text="Export Security Report (.txt)",
            command=self.export_report,
            accent="green"
        )
        export_btn.pack(side="right")

        # History Frame Listbox
        list_container = tk.Frame(card, bg=bg_color, highlightthickness=1, highlightbackground=self.get_color("border"))
        list_container.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(
            list_container,
            bg=bg_color,
            fg=fg_color,
            font=("Consolas", 10),
            bd=0,
            highlightthickness=0,
            selectbackground=self.get_color("btn_active"),
            selectforeground=fg_color,
            yscrollcommand=scrollbar.set
        )
        self.history_listbox.pack(side="left", fill="both", expand=True, padx=12, pady=12)
        scrollbar.config(command=self.history_listbox.yview)

        self.refresh_history_ui()

    def refresh_history_ui(self):
        self.history_listbox.delete(0, tk.END)
        if not self.history:
            self.history_listbox.insert(tk.END, " No assessment records found. Run password configurations or hash matches first.")
            return
            
        for entry in self.history:
            formatted_line = f" [{entry['timestamp']}]  <{entry['type']}>  {entry['description']}"
            self.history_listbox.insert(tk.END, formatted_line)

    def clear_history(self):
        confirm = messagebox.askyesno("Confirm Log Clear", "Are you sure you want to clear your local assessment history?")
        if confirm:
            self.history = []
            if os.path.exists(self.history_file):
                try:
                    os.remove(self.history_file)
                except Exception as e:
                    print(e)
            self.refresh_history_ui()

    def export_report(self):
        if not self.history:
            messagebox.showwarning("Audit Empty", "No history available to compile a report.")
            return

        default_filename = f"cybertoolkit_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = filedialog.asksaveasfilename(
            initialdir=self.reports_dir,
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("========================================================================\n")
                f.write("                PERSONAL CYBERSECURITY TOOLKIT REPORT                  \n")
                f.write(f" Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("========================================================================\n\n")
                
                f.write("1. SUMMARY OF SECURITY AUDITS CONDUCTED\n")
                f.write("------------------------------------------------------------------------\n")
                f.write(f"Total events recorded: {len(self.history)}\n\n")

                f.write("2. SECURITY ASSESSMENT ACTION LOG\n")
                f.write("------------------------------------------------------------------------\n")
                for entry in self.history:
                    f.write(f"[{entry['timestamp']}] [{entry['type']}]\n")
                    f.write(f"  Result Detail: {entry['description']}\n")
                    f.write("  " + "-" * 50 + "\n")

                f.write("\n3. NETWORK DEFENSE & SECURITY BEST PRACTICES (REFERENCE)\n")
                f.write("------------------------------------------------------------------------\n")
                f.write("- Rationale: Automated scanning vectors constitute common reconnaissance phases.\n")
                f.write("- Firewall Baseline: Always drop unsolicited incoming packets; never expose management\n")
                f.write("  ports (like FTP on 21, SSH on 22, SMB on 445) to the public internet.\n")
                f.write("- Key Auditing: Perform regular checksum validations (SHA256) on critical binary\n")
                f.write("  executables and system utilities to verify absence of local code modifications.\n\n")
                f.write("========================================================================\n")
                f.write("                           END OF REPORT                                \n")
                f.write("========================================================================\n")

            messagebox.showinfo("Report Exported", f"Audit report successfully exported to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberToolkitApp(root)
    root.mainloop()
