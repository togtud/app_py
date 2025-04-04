import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Model
class TreeModel:
    def __init__(self):
        self.items = [
            {"name": "Node 1", "children": [{"name": "Child 1"}, {"name": "Child 2"}]},
            {"name": "Node 2", "children": []},
        ]

    def add_item(self, parent_name, new_item_name):
        parent = self.find_item(self.items, parent_name)
        if parent:
            parent['children'].append({"name": new_item_name})
        else:
            self.items.append({"name": new_item_name, "children": []})

    def delete_item(self, item_name):
        def _delete(items):
            for item in items:
                if item['name'] == item_name:
                    items.remove(item)
                    return True
                if _delete(item.get('children', [])):
                    return True
            return False
        
        _delete(self.items)

    def find_item(self, items, name):
        for item in items:
            if item['name'] == name:
                return item
            found = self.find_item(item.get('children', []), name)
            if found:
                return found
        return None

    def get_items(self):
        return self.items


# View
class TreeView(ttk.Treeview):
    def __init__(self, parent, on_select):
        super().__init__(parent)
        self.on_select = on_select
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.populate_tree()

    def populate_tree(self):
        self.delete(*self.get_children())

        def add_nodes(parent, items):
            for item in items:
                node = self.insert(parent, 'end', text=item['name'])
                add_nodes(node, item.get('children', []))

        add_nodes('', self.on_select.model.get_items())

    def on_tree_select(self, event):
        selected_item = self.selection()
        if selected_item:
            item_name = self.item(selected_item, 'text')
            self.on_select(item_name)


# Controller
class TreeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.selected_item = None
        self.setup_ui()

    def setup_ui(self):
        # Create the Details Panel
        self.details_frame = tk.Frame()
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.details_label = tk.Label(self.details_frame, text="Select an item to see details.")
        self.details_label.pack(pady=10)

        self.add_button = tk.Button(self.details_frame, text='Add Item', command=self.add_item)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self.details_frame, text='Delete Item', command=self.delete_item)
        self.delete_button.pack(pady=5)

    def add_item(self):
        new_item_name = tk.simpledialog.askstring("Add Item", "Enter name for new item:")
        if new_item_name:
            self.model.add_item(self.selected_item, new_item_name)
            self.view.populate_tree()

    def delete_item(self):
        if self.selected_item:
            self.model.delete_item(self.selected_item)
            self.selected_item = None
            self.details_label.config(text="Select an item to see details.")
            self.view.populate_tree()

    def update_selection(self, item_name):
        self.selected_item = item_name
        self.details_label.config(text=f"Selected Item: {item_name}")


# Main Application

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MVC Tree View Example")
        self.geometry("400x300")
        
        self.model = TreeModel()
        self.controller = TreeController(self.model, self.create_tree_view())

    def create_tree_view(self):
        view = TreeView(self, self.controller.update_selection)
        return view

if __name__ == "__main__":
    app = App(tk.Tk)
    app.mainloop()



