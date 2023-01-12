import os
from tkinter import (
    Tk,
    Label,
    Button,
    Frame,
    LabelFrame,
    messagebox,
    StringVar,
    Radiobutton,
)
from tkinter.filedialog import askdirectory
from tkinter import ttk

import json
from PIL import Image


from flags_hierarchy import hierarchy


def get_complete_text(tree, item):
    item_text = tree.item(item, "text")
    parent = tree.parent(item)
    if parent:
        item_text = f"{get_complete_text(tree, parent)}/{item_text}"
    return item_text


class Annotator:
    def __init__(self, master):
        self.master = master
        master.title("Annotator Studio")

        self.controls = LabelFrame(master, text="Controls", padx=5, pady=5)
        self.controls.pack(padx=15, fill="x")
        self.select_button = Button(
            self.controls, text="Select", command=self.select_image
        )
        self.select_button.pack(side="left")
        self.back_button = Button(
            self.controls, text="Back", command=self.back_image, state="disabled"
        )
        self.back_button.pack(side="left")
        self.next_button = Button(
            self.controls, text="Next", command=self.next_image, state="disabled"
        )
        self.next_button.pack(side="left")
        self.annotate_button = Button(
            self.controls,
            text="Annotate",
            command=self.annotate_image,
            state="disabled",
        )
        self.annotate_button.pack(side="left")
        self.save_button = Button(
            self.controls, text="Save", command=self.save_annotation, state="disabled"
        )
        self.save_button.pack(side="left")

        self.image = LabelFrame(master, text="Image", padx=5, pady=5)
        self.image.pack(padx=15, fill="x")
        self.inner_frame = Frame(self.image)
        self.inner_frame.grid(sticky="w")
        self.image_label = Label(self.inner_frame, text="No image selected.")
        self.image_label.pack(side="left")
        self.image_label.pack()

        self.labels = LabelFrame(master, text="Labels", padx=5, pady=5)
        self.labels.pack(padx=15, pady=15, fill="x")
        self.var = StringVar()
        self.var.set(None)
        positive_button = Radiobutton(
            self.labels, text="Positive", variable=self.var, value="Positive"
        )
        negative_button = Radiobutton(
            self.labels, text="Negative", variable=self.var, value="Negative"
        )

        positive_button.pack(side="left")
        negative_button.pack(side="left")

        self.flags_label = ttk.Label(master, text="Flags")
        self.flags_label.pack()
        self.tree = ttk.Treeview(master, show="tree", selectmode="extended")

        def add_node(k, v):
            for i, j in v.items():
                self.tree.insert(k, 1, i, text=i)
                if isinstance(j, dict):
                    add_node(i, j)

        for k, v in hierarchy.items():
            self.tree.insert("", 1, k, text=k)
            add_node(k, v)

        self.tree.pack(expand=True, fill="both")

        self.image_files = []
        self.file_index = 0

    def select_image(self):
        self.directory = askdirectory()
        self.image_files = [
            f
            for f in os.listdir(self.directory)
            if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")
        ]
        self.file_index = 0
        self.filepath = os.path.join(self.directory, self.image_files[self.file_index])
        self.image_label.config(
            text="Image selected: " + os.path.basename(self.filepath)
        )
        self.next_button.config(state="normal")
        self.annotate_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.var.set(0)
        if len(self.image_files) > 1:
            self.back_button.config(state="normal")

    def back_image(self):
        if self.file_index == 0:
            messagebox.showinfo("No more images", "This is the first image.")
            self.back_button.config(state="disabled")
            return
        self.file_index -= 1
        self.filepath = os.path.join(self.directory, self.image_files[self.file_index])
        self.image_label.config(
            text="Image selected: " + os.path.basename(self.filepath)
        )
        self.next_button.config(state="normal")
        self.annotate_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.var.set(0)
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.selection_remove(item)

    def annotate_image(self):
        self.save_button.config(state="normal")
        with Image.open(self.filepath) as image:
            image.show()
        self.save_button.config(state="normal")

    def next_image(self):
        self.file_index += 1
        if self.file_index >= len(self.image_files):
            messagebox.showinfo(
                "No more images", "There are no more images in this folder."
            )
            self.next_button.config(state="disabled")
            return
        self.filepath = os.path.join(self.directory, self.image_files[self.file_index])
        self.image_label.config(
            text="Image selected: " + os.path.basename(self.filepath)
        )
        self.annotate_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.var.set(0)
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.selection_remove(item)

    def save_annotation(self):
        annotations = {}
        annotations["labels"] = {}
        annotations["flags"] = {}
        filename = self.image_files[self.file_index]

        flags = []
        selected_items = self.tree.selection()
        for item in selected_items:
            item_text = get_complete_text(self.tree, item)
            flags.append(item_text)

        annotations["flags"] = flags

        if self.var.get() in ["Positive", "Negative"]:
            annotations["labels"]["label"] = self.var.get()
        else:
            messagebox.showerror("Error", "Please select a class before saving.")
            return

        try:
            with open("annotations.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}

        if filename not in data:
            data[filename] = {}
        data[filename].update(annotations)

        with open("annotations.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

        messagebox.showinfo(
            "Annotations Saved!", "Annotations have been saved to the disk."
        )
        self.save_button.config(state="disabled")


root = Tk()
my_gui = Annotator(root)
root.mainloop()
