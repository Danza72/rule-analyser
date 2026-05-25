import threading
import tkinter as tk
from tkinter import font as tkfont

from model import analyze_rule


# ── Helpers ──────────────────────────────────────────────────────────────────

def set_output(text: str):
    """Replace the output panel content (safe to call from any thread via after())."""
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)


def run_analysis():
    """Read input, call model in a background thread, stream result to output."""
    rule = input_text.get("1.0", tk.END).strip()
    if not rule:
        set_output("⚠  Please enter a rule before running.")
        return

    # Disable button while running
    run_btn.config(state=tk.DISABLED, text="⏳  Analysing…")
    set_output("Sending to model, please wait…")

    def worker():
        try:
            result = analyze_rule(rule)
        except Exception as exc:
            result = f"Error:\n{exc}"
        # Schedule UI update back on the main thread
        root.after(0, lambda: finish(result))

    threading.Thread(target=worker, daemon=True).start()


def finish(result: str):
    set_output(result)
    run_btn.config(state=tk.NORMAL, text="▶  Analyse Rule")


def clear_input():
    input_text.delete("1.0", tk.END)


def clear_output():
    set_output("")


# ── Window ────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Rule Analyser")
root.configure(bg="#1a1a2e")
root.geometry("1000x600")
root.minsize(720, 420)

MONO  = tkfont.Font(family="Courier New", size=11)
LABEL = tkfont.Font(family="Courier New", size=9,  weight="bold")
BTN   = tkfont.Font(family="Courier New", size=10, weight="bold")

BG       = "#1a1a2e"
PANEL    = "#16213e"
FG       = "#e2e8f0"
ACCENT   = "#4fc3f7"   # blue  – input side
ACCENT2  = "#81c784"   # green – output side
MUTED    = "#4a5568"
BTN_BG   = "#0f3460"
BTN_HOV  = "#1a4a7a"

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)

# ── Column headers ────────────────────────────────────────────────────────────
tk.Label(root, text="▎ RULE INPUT", font=LABEL, bg=BG, fg=ACCENT,
         anchor="w", padx=12, pady=8).grid(row=0, column=0, sticky="ew")

tk.Frame(root, bg=MUTED, width=1).grid(row=0, column=1, rowspan=3,
                                        sticky="ns", padx=4)

tk.Label(root, text="▎ ANALYSIS OUTPUT", font=LABEL, bg=BG, fg=ACCENT2,
         anchor="w", padx=12, pady=8).grid(row=0, column=2, sticky="ew")

# ── Input panel ───────────────────────────────────────────────────────────────
def make_panel(col):
    f = tk.Frame(root, bg=PANEL, padx=6, pady=6)
    f.grid(row=1, column=col, sticky="nsew",
           padx=(8 if col == 0 else 0, 0 if col == 0 else 8), pady=(0, 6))
    f.rowconfigure(0, weight=1)
    f.columnconfigure(0, weight=1)
    return f

in_frame = make_panel(0)
input_text = tk.Text(
    in_frame, font=MONO, bg=PANEL, fg=FG,
    insertbackground=ACCENT,
    selectbackground=ACCENT, selectforeground=BG,
    relief=tk.FLAT, bd=0, wrap=tk.WORD, undo=True,
)
input_text.grid(row=0, column=0, sticky="nsew")
sy_in = tk.Scrollbar(in_frame, orient=tk.VERTICAL, command=input_text.yview,
                      bg=BG, troughcolor=PANEL, relief=tk.FLAT)
sy_in.grid(row=0, column=1, sticky="ns")
input_text.config(yscrollcommand=sy_in.set)

# ── Output panel ──────────────────────────────────────────────────────────────
out_frame = make_panel(2)
output_text = tk.Text(
    out_frame, font=MONO, bg=PANEL, fg=ACCENT2,
    insertbackground=ACCENT2,
    selectbackground=ACCENT2, selectforeground=BG,
    relief=tk.FLAT, bd=0, wrap=tk.WORD, state=tk.DISABLED,
)
output_text.grid(row=0, column=0, sticky="nsew")
sy_out = tk.Scrollbar(out_frame, orient=tk.VERTICAL, command=output_text.yview,
                       bg=BG, troughcolor=PANEL, relief=tk.FLAT)
sy_out.grid(row=0, column=1, sticky="ns")
output_text.config(yscrollcommand=sy_out.set)

# ── Button bar ────────────────────────────────────────────────────────────────
btn_bar = tk.Frame(root, bg=BG)
btn_bar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 10))

def make_btn(text, cmd, fg):
    b = tk.Button(btn_bar, text=text, command=cmd,
                  font=BTN, bg=BTN_BG, fg=fg,
                  activebackground=BTN_HOV, activeforeground=fg,
                  relief=tk.FLAT, bd=0, padx=16, pady=7, cursor="hand2")
    b.pack(side=tk.LEFT, padx=4)
    return b

run_btn = make_btn("▶  Analyse Rule", run_analysis, ACCENT)
make_btn("✕  Clear Input",  clear_input,  MUTED)
make_btn("✕  Clear Output", clear_output, MUTED)

tk.Label(root, text="Paste or type a rule on the left, then click Analyse Rule.",
         font=LABEL, bg=BG, fg=MUTED, anchor="w", padx=12, pady=4
         ).grid(row=3, column=0, columnspan=3, sticky="ew")

root.mainloop()