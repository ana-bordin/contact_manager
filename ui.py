import tkinter as tk
from tkinter import messagebox, simpledialog
from database import create_table, add_contact, get_all_contacts, delete_contact, update_contact

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Contatos")

        # Create table if it doesn't exist
        create_table()

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame for form
        self.frame_form = tk.Frame(self.root)
        self.frame_form.pack(pady=10)

        # Name Label and Entry
        self.label_name = tk.Label(self.frame_form, text="Nome:")
        self.label_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(self.frame_form)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        # Phone Label and Entry
        self.label_phone = tk.Label(self.frame_form, text="Telefone:")
        self.label_phone.grid(row=1, column=0, padx=5, pady=5)
        self.entry_phone = tk.Entry(self.frame_form)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        self.button_add = tk.Button(self.frame_form, text="Adicionar Contato", command=self.add_contact)
        self.button_add.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_view = tk.Button(self.frame_form, text="Visualizar Contatos", command=self.view_contacts)
        self.button_view.grid(row=3, column=0, columnspan=2, pady=10)

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Opções", menu=self.menu)
        self.menu.add_command(label="Editar Contato", command=self.edit_contact)
        self.menu.add_command(label="Excluir Contato", command=self.delete_contact)

    def add_contact(self):
        """Add a new contact to the database."""
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        if self.validate_data(name, phone):
            add_contact(name, phone)
            messagebox.showinfo("Sucesso", "Contato adicionado com sucesso!")
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos com dados válidos.")

    def view_contacts(self):
        """Display all contacts in a message box."""
        contacts = get_all_contacts()
        if contacts:
            contacts_list = '\n'.join([f'ID: {contact[0]}, Nome: {contact[1]}, Telefone: {contact[2]}' for contact in contacts])
            messagebox.showinfo("Contatos", contacts_list)
        else:
            messagebox.showinfo("Contatos", "Nenhum contato encontrado.")

    def edit_contact(self):
        """Edit an existing contact."""
        contact_id = simpledialog.askinteger("Editar Contato", "Digite o ID do contato que deseja editar:")
        if contact_id:
            new_name = simpledialog.askstring("Editar Contato", "Digite o novo nome:")
            new_phone = simpledialog.askstring("Editar Contato", "Digite o novo telefone:")
            if self.validate_data(new_name, new_phone):
                update_contact(contact_id, new_name, new_phone)
                messagebox.showinfo("Sucesso", "Contato atualizado com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Dados inválidos. Por favor, preencha todos os campos com dados válidos.")

    def delete_contact(self):
        """Delete an existing contact."""
        contact_id = simpledialog.askinteger("Excluir Contato", "Digite o ID do contato que deseja excluir:")
        if contact_id:
            delete_contact(contact_id)
            messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")

    def validate_data(self, name, phone):
        """Validate name and phone data."""
        return name and phone and phone.isdigit() and len(phone) >= 10