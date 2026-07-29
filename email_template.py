from __future__ import annotations

from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk


def format_email(
    subject,
    recipient_name,
    message_body,
    sender_name="Sechaba Pro",
    sender_email="support@example.com",
):
    current_date = datetime.now().strftime("%d %B %Y")

    email = f"""Subject: {subject}

Dear {recipient_name},

{message_body}

Warm regards,
{sender_name}
Email: {sender_email}
Date: {current_date}
"""
    return email


class ComposeWindow(tk.Toplevel):
    def __init__(self, parent, on_send=None):
        super().__init__(parent)
        self.parent = parent
        self.on_send = on_send
        self.title("Compose Email")
        self.geometry("760x560")
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)

        header = ttk.Label(self, text="New Message", font=("Segoe UI", 16, "bold"))
        header.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        fields = [
            ("To", "to_entry"),
            ("CC", "cc_entry"),
            ("BCC", "bcc_entry"),
            ("Subject", "subject_entry"),
        ]

        self.entries = {}
        for index, (label_text, attr) in enumerate(fields, start=1):
            label = ttk.Label(self, text=label_text)
            label.grid(row=index, column=0, sticky="w", padx=16, pady=(6, 2))
            entry = ttk.Entry(self)
            entry.grid(row=index + len(fields), column=0, sticky="ew", padx=16, pady=(0, 8))
            self.entries[attr] = entry

        ttk.Label(self, text="Message").grid(row=8, column=0, sticky="w", padx=16, pady=(6, 2))
        self.body_text = tk.Text(self, height=16, wrap="word", font=("Segoe UI", 11))
        self.body_text.grid(row=9, column=0, sticky="nsew", padx=16, pady=(0, 8))

        button_frame = ttk.Frame(self)
        button_frame.grid(row=10, column=0, sticky="e", padx=16, pady=(0, 16))

        ttk.Button(button_frame, text="Save Draft", command=self.save_draft).pack(side="left", padx=(0, 8))
        ttk.Button(button_frame, text="Preview", command=self.preview_message).pack(side="left", padx=(0, 8))
        ttk.Button(button_frame, text="Send", command=self.send_message).pack(side="left")

    def save_draft(self):
        draft = {
            "from": "You",
            "subject": self.entries["subject_entry"].get() or "Untitled Draft",
            "preview": self.body_text.get("1.0", "end").strip()[:80],
            "body": self.body_text.get("1.0", "end").strip(),
            "time": "just now",
            "folder": "Drafts",
            "unread": False,
        }
        self.parent.drafts.append(draft)
        self.parent.refresh_mail_list()
        messagebox.showinfo("Draft Saved", "Your draft has been saved successfully.")
        self.destroy()

    def preview_message(self):
        message = format_email(
            self.entries["subject_entry"].get() or "No Subject",
            self.entries["to_entry"].get() or "Recipient",
            self.body_text.get("1.0", "end").strip() or "Your message will appear here.",
        )
        messagebox.showinfo("Email Preview", message)

    def send_message(self):
        message_body = self.body_text.get("1.0", "end").strip()
        if not message_body:
            messagebox.showwarning("Empty Message", "Please type a message before sending.")
            return

        email = {
            "from": "You",
            "subject": self.entries["subject_entry"].get() or "No Subject",
            "preview": message_body[:80],
            "body": message_body,
            "time": "just now",
            "folder": "Sent",
            "unread": False,
        }
        self.parent.sent_items.append(email)
        self.parent.refresh_mail_list()
        if self.on_send:
            self.on_send(email)
        messagebox.showinfo("Message Sent", "Your email has been delivered to the sending queue.")
        self.destroy()


class AssistantWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("AI Assistant")
        self.geometry("480x340")
        self.resizable(False, False)

        ttk.Label(self, text="AI Assistant", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=16, pady=(16, 8))
        ttk.Label(self, text="Choose a style and I will draft a polished message.", wraplength=400).pack(anchor="w", padx=16, pady=(0, 12))

        self.options = [
            "Job Application",
            "Business Proposal",
            "Complaint",
            "Thank You",
            "Follow-up",
            "Meeting Request",
        ]
        self.selected = tk.StringVar(value=self.options[0])
        for option in self.options:
            ttk.Radiobutton(self, text=option, variable=self.selected, value=option).pack(anchor="w", padx=24)

        ttk.Button(self, text="Generate Draft", command=self.generate_draft).pack(pady=(16, 0))

    def generate_draft(self):
        templates = {
            "Job Application": "Dear Hiring Manager,\n\nI am excited to apply for the role and would welcome the opportunity to discuss how my experience can support your team.\n\nKind regards,\nSechaba Jeremiah",
            "Business Proposal": "Hello,\n\nI would love to explore a partnership that brings measurable value to your business and improves your current workflow.\n\nBest regards,\nSechaba Jeremiah",
            "Complaint": "Hello,\n\nI am writing to express my concern regarding a recent experience and would appreciate a prompt resolution.\n\nSincerely,\nSechaba Jeremiah",
            "Thank You": "Dear Recipient,\n\nThank you for your support and for the time you invested in our conversation.\n\nWarm regards,\nSechaba Jeremiah",
            "Follow-up": "Hello,\n\nI am following up on our previous conversation and would appreciate any update you can share.\n\nBest regards,\nSechaba Jeremiah",
            "Meeting Request": "Hello,\n\nI would like to request a short meeting to discuss the next steps and explore opportunities for collaboration.\n\nKind regards,\nSechaba Jeremiah",
        }
        draft = templates[self.selected.get()]
        self.parent.compose_from_assistant(draft)
        self.destroy()


class ContactsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Contacts")
        self.geometry("520x360")
        self.resizable(False, False)

        ttk.Label(self, text="Contacts", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=16, pady=(16, 8))
        self.tree = ttk.Treeview(self, columns=("name", "email"), show="headings", height=10)
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.column("name", width=220)
        self.tree.column("email", width=260)
        self.tree.pack(fill="both", padx=16, pady=(0, 12))

        for contact in parent.contacts:
            self.tree.insert("", "end", values=(contact["name"], contact["email"]))

        ttk.Button(self, text="Use Selected", command=self.use_selected).pack()

    def use_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Contact", "Select a contact first.")
            return
        values = self.tree.item(selected[0], "values")
        self.parent.compose_to_contact(values[1])
        self.destroy()


class MailFlowDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MailFlow Pro")
        self.geometry("1280x760")
        self.minsize(1120, 700)
        self.configure(bg="#f3f6fb")

        self.dark_mode = False
        self.current_folder = "Inbox"
        self.emails = [
            {
                "from": "Morena Lephoi",
                "subject": "Project Proposal",
                "preview": "Thanks for sending the proposal and the revised timeline.",
                "body": "Thanks for sending the proposal and the revised timeline. We are excited to move forward with the discussion.",
                "time": "2 min ago",
                "folder": "Inbox",
                "tab": "Primary",
                "unread": True,
                "attachments": [("PDF", "Proposal.pdf", "1.2 MB")],
            },
            {
                "from": "Sechaba Mokoena",
                "subject": "Interview Invitation",
                "preview": "We are pleased to invite you for a final interview next week.",
                "body": "We are pleased to invite you for a final interview next week. Please let us know if you have any questions.",
                "time": "12 min ago",
                "folder": "Inbox",
                "tab": "Primary",
                "unread": False,
                "attachments": [("DOCX", "Interview_Notes.docx", "890 KB")],
            },
            {
                "from": "Relebohile Tlhapi",
                "subject": "Weekly Report",
                "preview": "Please review the weekly report before our meeting today.",
                "body": "Please review the weekly report before our meeting today. I have attached a summary of progress.",
                "time": "1 hr ago",
                "folder": "Inbox",
                "tab": "Social",
                "unread": True,
            },
        ]
        self.sent_items = []
        self.drafts = []
        self.contacts = [
            {"name": "Morena Lephoi", "email": "morena@gmail.com"},
            {"name": "Sechaba Mokoena", "email": "sechaba@gmail.com"},
            {"name": "Lerato Khumalo", "email": "lerato@gmail.com"},
            {"name": "Relebohile Tlhapi", "email": "relebohile@gmail.com"},
        ]

        self._build_ui()
        self.refresh_mail_list()
        self.show_folder("Inbox")

    def _build_ui(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=(10, 8), font=("Segoe UI", 10))
        self.style.configure("TEntry", padding=6)
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"))
        self.style.configure("Card.TFrame", background="#ffffff")

        self.configure(bg="#f4f7fb")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        sidebar = tk.Frame(self, bg="#0f172a", width=270)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.columnconfigure(0, weight=1)

        tk.Label(sidebar, text="✉ MailFlow Pro", bg="#0f172a", fg="#f8fafc", font=("Segoe UI", 18, "bold"), anchor="w").grid(row=0, column=0, sticky="ew", padx=18, pady=(22, 16))

        compose_button = tk.Button(
            sidebar,
            text="✉ Compose Email",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=14,
            pady=10,
            cursor="hand2",
            command=self.open_compose,
        )
        compose_button.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))

        tk.Label(sidebar, text="Navigation", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=18, pady=(0, 8))
        self.folder_buttons = {}
        folders = ["Inbox", "Starred", "Sent", "Drafts", "Scheduled", "Important", "Spam", "Trash", "Archive"]
        for index, folder in enumerate(folders, start=3):
            btn = tk.Button(
                sidebar,
                text=f"{self._folder_icon(folder)} {folder}",
                bg="#0f172a",
                fg="#cbd5e1",
                font=("Segoe UI", 10),
                relief="flat",
                anchor="w",
                padx=8,
                pady=7,
                cursor="hand2",
                command=lambda f=folder: self.show_folder(f),
            )
            btn.grid(row=index, column=0, sticky="ew", padx=12)
            self.folder_buttons[folder] = btn

        tk.Label(sidebar, text="Workspace", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 10, "bold")).grid(row=13, column=0, sticky="w", padx=18, pady=(18, 8))
        for row, label in enumerate(["Contacts", "Templates", "AI Assistant", "Settings"], start=14):
            tk.Label(sidebar, text=label, bg="#0f172a", fg="#e2e8f0", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", padx=24, pady=3)

        storage_frame = tk.Frame(sidebar, bg="#111c33", bd=0)
        storage_frame.grid(row=18, column=0, sticky="ew", padx=18, pady=(20, 18))
        tk.Label(storage_frame, text="Storage", bg="#111c33", fg="#f8fafc", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 4))
        tk.Label(storage_frame, text="2.4 GB / 15 GB", bg="#111c33", fg="#93c5fd", font=("Segoe UI", 10)).pack(anchor="w", padx=12, pady=(0, 6))
        tk.Label(storage_frame, text="✓ SMTP Connected\n✓ IMAP Connected\n✓ API Online", bg="#111c33", fg="#cbd5e1", justify="left", font=("Segoe UI", 9), anchor="w").pack(anchor="w", padx=12, pady=(0, 10))

        content = tk.Frame(self, bg="#f4f7fb")
        content.grid(row=0, column=1, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.columnconfigure(2, weight=0)
        content.rowconfigure(1, weight=1)
        content.rowconfigure(2, weight=0)

        header = tk.Frame(content, bg="#ffffff", bd=0)
        header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 14))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        self.search_var = tk.StringVar()
        tk.Label(header, text="Search emails", bg="#ffffff", fg="#64748b", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 0))
        search_entry = ttk.Entry(header, textvariable=self.search_var, width=38)
        search_entry.grid(row=1, column=0, sticky="ew", padx=18, pady=(6, 18))
        action_frame = tk.Frame(header, bg="#ffffff")
        action_frame.grid(row=0, column=1, rowspan=2, sticky="e", padx=18, pady=(16, 18))
        ttk.Button(action_frame, text="🌙 Theme", command=self.toggle_theme).pack(side="left", padx=(0, 8))
        ttk.Button(action_frame, text="🔔 Alerts", command=self.filter_emails).pack(side="left", padx=(0, 8))
        ttk.Button(action_frame, text="Sechaba", command=self.open_contacts).pack(side="left")

        self.mail_frame = tk.Frame(content, bg="#ffffff", bd=0)
        self.mail_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.mail_frame.columnconfigure(0, weight=1)
        self.mail_frame.rowconfigure(1, weight=1)
        tk.Label(self.mail_frame, text="Inbox", bg="#ffffff", fg="#111827", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        tabs_frame = tk.Frame(self.mail_frame, bg="#ffffff")
        tabs_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        self.tab_buttons = {}
        for tab in ["Primary", "Social", "Promotions"]:
            btn = tk.Button(
                tabs_frame,
                text=tab,
                bg="#f1f5f9",
                fg="#475569",
                relief="flat",
                padx=10,
                pady=6,
                cursor="hand2",
                command=lambda t=tab: self.switch_tab(t),
            )
            btn.pack(side="left", padx=(0, 8))
            self.tab_buttons[tab] = btn
        self.current_tab = "Primary"
        self._update_tabs()

        self.mail_tree = ttk.Treeview(self.mail_frame, columns=("from", "subject", "preview", "time"), show="headings", height=12)
        self.mail_tree.heading("from", text="From")
        self.mail_tree.heading("subject", text="Subject")
        self.mail_tree.heading("preview", text="Preview")
        self.mail_tree.heading("time", text="Time")
        self.mail_tree.column("from", width=140)
        self.mail_tree.column("subject", width=220)
        self.mail_tree.column("preview", width=280)
        self.mail_tree.column("time", width=90)
        self.mail_tree.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 8))
        self.mail_tree.tag_configure("unread", foreground="#1d4ed8", font=("Segoe UI", 10, "bold"))
        self.mail_tree.tag_configure("read", foreground="#475569", font=("Segoe UI", 10))
        self.mail_tree.bind("<<TreeviewSelect>>", self.on_mail_select)

        self.empty_state = tk.Label(self.mail_frame, text="No messages in this view yet.", bg="#ffffff", fg="#64748b", font=("Segoe UI", 10))
        self.empty_state.grid(row=3, column=0, sticky="n", padx=16, pady=(0, 16))
        self.empty_state.grid_remove()

        self.status_bar = tk.Label(content, text="● Connected • AI Ready • 3 new messages", bg="#f8fafc", fg="#0f172a", font=("Segoe UI", 9), anchor="w")
        self.status_bar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=(6, 10))

        preview_frame = tk.Frame(content, bg="#ffffff", bd=0)
        preview_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(3, weight=1)
        tk.Label(preview_frame, text="Email Preview", bg="#ffffff", fg="#111827", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 12))
        self.preview_title = tk.Label(preview_frame, text="Select an email", bg="#ffffff", fg="#111827", font=("Segoe UI", 12, "bold"), wraplength=300, justify="left")
        self.preview_title.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 6))
        self.preview_meta = tk.Label(preview_frame, text="", bg="#ffffff", fg="#64748b", wraplength=300, justify="left")
        self.preview_meta.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 8))
        toolbar = tk.Frame(preview_frame, bg="#ffffff")
        toolbar.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 10))
        ttk.Button(toolbar, text="Reply").pack(side="left", padx=(0, 8))
        ttk.Button(toolbar, text="Reply All").pack(side="left", padx=(0, 8))
        ttk.Button(toolbar, text="Forward").pack(side="left")
        self.preview_body = tk.Text(preview_frame, wrap="word", height=14, font=("Segoe UI", 10), bd=0, highlightthickness=0)
        self.preview_body.grid(row=4, column=0, sticky="nsew", padx=16, pady=(0, 10))
        self.preview_body.configure(state="disabled")

        attachments_title = tk.Label(preview_frame, text="Attachments", bg="#ffffff", fg="#111827", font=("Segoe UI", 11, "bold"))
        attachments_title.grid(row=5, column=0, sticky="w", padx=16, pady=(0, 6))
        self.attachments_frame = tk.Frame(preview_frame, bg="#ffffff")
        self.attachments_frame.grid(row=6, column=0, sticky="ew", padx=16, pady=(0, 12))

        widget_panel = tk.Frame(content, bg="#ffffff", bd=0)
        widget_panel.grid(row=1, column=2, sticky="nsew")
        widget_panel.columnconfigure(0, weight=1)
        tk.Label(widget_panel, text="AI Assistant", bg="#ffffff", fg="#111827", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 10))
        ai_card = tk.Frame(widget_panel, bg="#eff6ff", bd=0)
        ai_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))
        tk.Label(ai_card, text="Need help writing?", bg="#eff6ff", fg="#1d4ed8", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        tk.Label(ai_card, text="Start writing polished replies, summaries, or proposals in one click.", bg="#eff6ff", fg="#475569", wraplength=220, justify="left").pack(anchor="w", padx=12, pady=(0, 12))
        ttk.Button(ai_card, text="Open Assistant", command=self.open_ai_assistant).pack(anchor="w", padx=12, pady=(0, 12))

        stats_card = tk.Frame(widget_panel, bg="#f8fafc", bd=0)
        stats_card.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 10))
        tk.Label(stats_card, text="Quick Stats", bg="#f8fafc", fg="#111827", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(12, 8))
        for label, value in [("Emails Sent", "45"), ("Replies", "18"), ("Scheduled", "4"), ("New Contacts", "6")]:
            row_frame = tk.Frame(stats_card, bg="#f8fafc")
            row_frame.pack(fill="x", padx=12, pady=2)
            tk.Label(row_frame, text=label, bg="#f8fafc", fg="#64748b").pack(side="left")
            tk.Label(row_frame, text=value, bg="#f8fafc", fg="#0f172a", font=("Segoe UI", 10, "bold")).pack(side="right")

        contacts_card = tk.Frame(widget_panel, bg="#f8fafc", bd=0)
        contacts_card.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 10))
        tk.Label(contacts_card, text="Frequent Contacts", bg="#f8fafc", fg="#111827", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(12, 8))
        for name, email in [("Morena Lephoi", "morena@gmail.com"), ("Sechaba Mokoena", "sechaba@gmail.com"), ("Lerato Khumalo", "lerato@gmail.com")]:
            contact_row = tk.Frame(contacts_card, bg="#f8fafc")
            contact_row.pack(fill="x", padx=12, pady=4)
            tk.Label(contact_row, text="●", bg="#f8fafc", fg="#22c55e").pack(side="left")
            tk.Label(contact_row, text=name, bg="#f8fafc", fg="#0f172a", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(6, 4))
            tk.Label(contact_row, text=email, bg="#f8fafc", fg="#64748b", font=("Segoe UI", 8)).pack(side="left")

        footer = tk.Frame(content, bg="#f4f7fb")
        footer.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(12, 8))
        tk.Label(footer, text="© MailFlow Pro · Privacy · Terms · Help", bg="#f4f7fb", fg="#64748b", font=("Segoe UI", 9)).pack(anchor="w", padx=20)

        self.bind("<Control-n>", lambda event: self.open_compose())

    def _folder_icon(self, folder):
        icons = {
            "Inbox": "📥",
            "Starred": "⭐",
            "Sent": "📤",
            "Drafts": "📝",
            "Scheduled": "⏰",
            "Important": "📌",
            "Spam": "🚫",
            "Trash": "🗑",
            "Archive": "📁",
        }
        return icons.get(folder, "📩")

    def _update_tabs(self):
        for tab_name, button in self.tab_buttons.items():
            button.configure(bg="#f1f5f9" if tab_name != self.current_tab else "#dbeafe", fg="#475569" if tab_name != self.current_tab else "#1d4ed8", relief="flat")

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        self._update_tabs()
        self.refresh_mail_list()

    def refresh_mail_list(self):
        for item in self.mail_tree.get_children():
            self.mail_tree.delete(item)

        visible = [
            email
            for email in self.emails + self.sent_items + self.drafts
            if email.get("folder") == self.current_folder
        ]
        if self.current_tab != "Primary":
            visible = [email for email in visible if email.get("tab", "Primary") == self.current_tab]
        if self.search_var.get().strip():
            query = self.search_var.get().strip().lower()
            visible = [
                email
                for email in visible
                if query in email.get("subject", "").lower() or query in email.get("preview", "").lower() or query in email.get("from", "").lower()
            ]

        for email in visible:
            self.mail_tree.insert(
                "",
                "end",
                values=(email["from"], email["subject"], email["preview"], email["time"]),
                tags=("unread" if email.get("unread") else "read",),
            )

        self.empty_state.grid_remove()
        if not visible:
            self.empty_state.grid()
            self.preview_title.config(text="No message selected")
            self.preview_meta.config(text="")
            self.preview_body.configure(state="normal")
            self.preview_body.delete("1.0", "end")
            self.preview_body.insert("1.0", "Select an email to preview it here.")
            self.preview_body.configure(state="disabled")
            return

        self.mail_tree.selection_set(self.mail_tree.get_children()[0])
        self.on_mail_select(None)

    def show_folder(self, folder):
        self.current_folder = folder
        self.refresh_mail_list()
        for button_name, button in self.folder_buttons.items():
            button.configure(
                bg="#2563eb" if button_name == folder else "#0f172a",
                fg="white" if button_name == folder else "#cbd5e1",
            )
        self.mail_frame.winfo_children()[0].config(text=folder)

    def filter_emails(self):
        self.refresh_mail_list()

    def on_mail_select(self, _event):
        selected = self.mail_tree.selection()
        if not selected:
            return
        item_id = selected[0]
        values = self.mail_tree.item(item_id, "values")
        subject = values[1]
        preview = values[2]
        email = next((entry for entry in self.emails + self.sent_items + self.drafts if entry.get("subject") == subject and entry.get("preview") == preview), None)
        if email:
            self.preview_title.config(text=subject)
            self.preview_meta.config(text=f"From: {email['from']}  •  To: you@mailflow.com  •  {email['time']}")
            self.preview_body.configure(state="normal")
            self.preview_body.delete("1.0", "end")
            self.preview_body.insert("1.0", email.get("body", preview))
            self.preview_body.configure(state="disabled")
            for widget in self.attachments_frame.winfo_children():
                widget.destroy()
            attachments = email.get("attachments", [])
            if attachments:
                for attachment in attachments:
                    card = tk.Frame(self.attachments_frame, bg="#f8fafc", bd=0)
                    card.pack(fill="x", pady=4)
                    tk.Label(card, text=attachment[0], bg="#f8fafc", fg="#2563eb", font=("Segoe UI", 9, "bold")).pack(anchor="w")
                    tk.Label(card, text=attachment[1], bg="#f8fafc", fg="#334155", font=("Segoe UI", 9)).pack(anchor="w")
                    tk.Label(card, text=attachment[2], bg="#f8fafc", fg="#64748b", font=("Segoe UI", 8)).pack(anchor="w")
            else:
                tk.Label(self.attachments_frame, text="No attachments", bg="#ffffff", fg="#64748b").pack(anchor="w")

    def open_compose(self):
        ComposeWindow(self)

    def open_ai_assistant(self):
        AssistantWindow(self)

    def open_contacts(self):
        ContactsWindow(self)

    def compose_from_assistant(self, draft_body):
        compose_window = ComposeWindow(self)
        compose_window.entries["subject_entry"].insert(0, "Draft from AI Assistant")
        compose_window.body_text.insert("1.0", draft_body)

    def compose_to_contact(self, email):
        compose_window = ComposeWindow(self)
        compose_window.entries["to_entry"].insert(0, email)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.configure(bg="#121826")
            self.style.configure("TFrame", background="#121826")
            self.style.configure("TLabel", background="#121826", foreground="#f3f4f6")
            self.style.configure("TEntry", fieldbackground="#1f2937")
            self.style.configure("TButton", background="#1f2937", foreground="#f3f4f6")
            self.style.configure("Treeview", background="#1f2937", fieldbackground="#1f2937", foreground="#f3f4f6")
            self.style.configure("Treeview.Heading", background="#263449", foreground="#f3f4f6")
            self.style.map("Treeview", background=[("selected", "#4f46e5")])
        else:
            self.configure(bg="#f3f6fb")
            self.style.configure("TFrame", background="#f3f6fb")
            self.style.configure("TLabel", background="#f3f6fb", foreground="#111827")
            self.style.configure("TEntry", fieldbackground="white")
            self.style.configure("TButton", background="#e5e7eb", foreground="#111827")
            self.style.configure("Treeview", background="white", fieldbackground="white", foreground="#111827")
            self.style.configure("Treeview.Heading", background="#e5e7eb", foreground="#111827")
            self.style.map("Treeview", background=[("selected", "#4f46e5")])



if __name__ == "__main__":
    app = MailFlowDashboard()
    app.mainloop()
