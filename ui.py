import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database import create_table, add_contact, get_all_contacts, delete_contact, update_contact

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Contatos")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Create table if it doesn't exist
        create_table()

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame for top area
        self.frame_top = tk.Frame(self.root, bg='#f5f5f5')
        self.frame_top.pack(fill=tk.X, pady=10)

        # Title Label
        self.label_title = tk.Label(self.frame_top, text="Gerenciador de Contatos", font=('Helvetica', 16, 'bold'), bg='#f5f5f5')
        self.label_title.pack(pady=10)

        # Frame for form
        self.frame_form = tk.Frame(self.root)
        self.frame_form.pack(pady=10)

        # Name Label and Entry
        self.label_name = tk.Label(self.frame_form, text="Nome:", font=('Helvetica', 12))
        self.label_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(self.frame_form, width=40)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        # Phone Label and Entry
        self.label_phone = tk.Label(self.frame_form, text="Telefone:", font=('Helvetica', 12))
        self.label_phone.grid(row=1, column=0, padx=5, pady=5)
        self.entry_phone = tk.Entry(self.frame_form, width=40)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        self.button_add = tk.Button(self.frame_form, text="Adicionar Contato", command=self.add_contact, bg='#4CAF50', fg='white')
        self.button_add.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_view = tk.Button(self.frame_form, text="Visualizar Contatos", command=self.view_contacts, bg='#2196F3', fg='white')
        self.button_view.grid(row=3, column=0, columnspan=2, pady=10)

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Opções", menu=self.menu)
        self.menu.add_command(label="Editar Contato", command=self.edit_contact)
        self.menu.add_command(label="Excluir Contato", command=self.delete_contact)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview for contacts
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Telefone"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbars
        self.v_scroll = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.v_scroll.set)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scroll = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.h_scroll.set)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    def add_contact(self):
        """Add a new contact to the database."""
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        if self.validate_data(name, phone):
            add_contact(name, phone)
            self.status_bar.config(text="Contato adicionado com sucesso!")
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
            self.update_treeview()
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos com dados válidos.")

    def view_contacts(self):
        """Display all contacts in a table."""
        self.update_treeview()

    def update_treeview(self):
        """Update the Treeview widget with the latest contacts from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        contacts = get_all_contacts()
        for contact in contacts:
            self.tree.insert("", tk.END, values=contact)

    def edit_contact(self):
        """Edit an existing contact."""
        contact_id = simpledialog.askinteger("Editar Contato", "Digite o ID do contato que deseja editar:")
        if contact_id:
            new_name = simpledialog.askstring("Editar Contato", "Digite o novo nome:")
            new_phone = simpledialog.askstring("Editar Contato", "Digite o novo telefone:")
            if self.validate_data(new_name, new_phone):
                update_contact(contact_id, new_name, new_phone)
                self.status_bar.config(text="Contato atualizado com sucesso!")
                self.update_treeview()
            else:
                messagebox.showwarning("Aviso", "Dados inválidos. Por favor, preencha todos os campos com dados válidos.")

    def delete_contact(self):
        """Delete an existing contact."""
        contact_id = simpledialog.askinteger("Excluir Contato", "Digite o ID do contato que deseja excluir:")
        if contact_id:
            delete_contact(contact_id)
            self.status_bar.config(text="Contato excluído com sucesso!")
            self.update_treeview()

    def validate_data(self, name, phone):
        """Validate name and phone data."""
        return name and phone and phone.isdigit() and len(phone) >= 10