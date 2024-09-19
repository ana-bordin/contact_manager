import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
from database import create_table, add_contact, get_all_contacts, delete_contact, update_contact

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Contatos")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Create table if it doesn't exist
        create_table()

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Gerenciador de Contatos
        self.tab_contacts = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_contacts, text='Contatos')

        # Tab 2: Relatórios
        self.tab_reports = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reports, text='Relatórios')

        # Create Widgets for Contacts Tab
        self.create_contact_widgets()
        
        # Create Widgets for Reports Tab
        self.create_report_widgets()

    def create_contact_widgets(self):
        # Frame for form
        self.frame_form = tk.Frame(self.tab_contacts)
        self.frame_form.pack(pady=10)

        # Name Label and Entry
        self.label_name = tk.Label(self.frame_form, text="Nome:", font=('Helvetica', 12))
        self.label_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(self.frame_form, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        # Phone Label and Entry
        self.label_phone = tk.Label(self.frame_form, text="Telefone:", font=('Helvetica', 12))
        self.label_phone.grid(row=1, column=0, padx=5, pady=5)
        self.entry_phone = tk.Entry(self.frame_form, width=30)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        self.button_add = tk.Button(self.frame_form, text="Adicionar Contato", command=self.add_contact, bg='#4CAF50', fg='white')
        self.button_add.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_view = tk.Button(self.frame_form, text="Visualizar Contatos", command=self.view_contacts, bg='#2196F3', fg='white')
        self.button_view.grid(row=3, column=0, columnspan=2, pady=10)

        # Search Frame
        self.frame_search = tk.Frame(self.tab_contacts)
        self.frame_search.pack(pady=10)
        self.label_search = tk.Label(self.frame_search, text="Buscar por Nome ou Telefone:", font=('Helvetica', 12))
        self.label_search.pack(side=tk.LEFT, padx=5)
        self.entry_search = tk.Entry(self.frame_search, width=30)
        self.entry_search.pack(side=tk.LEFT, padx=5)
        self.button_search = tk.Button(self.frame_search, text="Buscar", command=self.search_contacts, bg='#FFC107', fg='black')
        self.button_search.pack(side=tk.LEFT, padx=5)

        # Treeview for contacts
        self.tree = ttk.Treeview(self.tab_contacts, columns=("ID", "Nome", "Telefone"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbars
        self.v_scroll = ttk.Scrollbar(self.tab_contacts, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.v_scroll.set)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scroll = ttk.Scrollbar(self.tab_contacts, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.h_scroll.set)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    def create_report_widgets(self):
        # Frame for reports
        self.frame_report = tk.Frame(self.tab_reports)
        self.frame_report.pack(pady=10)

        # Report Labels
        self.label_total_contacts = tk.Label(self.frame_report, text="Total de Contatos:", font=('Helvetica', 12))
        self.label_total_contacts.pack(pady=5)
        self.total_contacts_value = tk.Label(self.frame_report, text="0", font=('Helvetica', 12, 'bold'))
        self.total_contacts_value.pack(pady=5)

        # Export Button
        self.button_export = tk.Button(self.frame_report, text="Exportar Contatos", command=self.export_contacts, bg='#FF5722', fg='white')
        self.button_export.pack(pady=10)

        # Update the report on startup
        self.update_report()

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
            self.update_report()
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos com dados válidos.")

    def view_contacts(self):
        """Display all contacts in a table."""
        self.update_treeview()

    def search_contacts(self):
        """Search contacts by name or phone."""
        query = self.entry_search.get()
        if query:
            contacts = [contact for contact in get_all_contacts() if query in contact[1] or query in contact[2]]
            self.update_treeview(contacts)
        else:
            self.update_treeview()

    def update_treeview(self, contacts=None):
        """Update the Treeview widget with the latest contacts from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        if contacts is None:
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
            self.update_report()

    def export_contacts(self):
        """Export contacts to a CSV file."""
        contacts = get_all_contacts()
        with open('contatos.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nome", "Telefone"])
            writer.writerows(contacts)
        messagebox.showinfo("Exportar Contatos", "Contatos exportados com sucesso para 'contatos.csv'.")

    def update_report(self):
        """Update the report with the total number of contacts."""
        total_contacts = len(get_all_contacts())
        self.total_contacts_value.config(text=str(total_contacts))

    def validate_data(self, name, phone):
        """Validate name and phone data."""
        return name and phone and phone.isdigit() and len(phone) >= 10

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
