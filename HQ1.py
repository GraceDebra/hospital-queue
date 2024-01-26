import tkinter as tk
from tkinter import ttk
from collections import deque

class Patient:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __lt__(self, other):
        # Compare patients based on age (larger age is higher priority)
        return self.age > other.age

class HospitalQueue:
    def __init__(self):
        self.queue = deque()

        #methods for the queue ADT operations
    def enqueue(self, patient):
        # Add patient to the queue and sort based on age
        self.queue.append(patient)
        self.queue = deque(sorted(self.queue))

    def dequeue(self):
        # Remove and return the patient at the front of the queue
        if not self.is_empty():
            return self.queue.popleft()
        else:
            return None

        #method for making the queue adaptible
    def move_patient(self, current_position, new_position):
        # Move patient from current position to new position
        if 0 <= current_position < len(self.queue) and 0 <= new_position < len(self.queue):
            patient = self.queue[current_position]
            self.queue.remove(patient)
            self.queue.insert(new_position, patient)

    def remove_patient(self, position):
        # Remove patient at the specified position
        if 0 <= position < len(self.queue):
            self.queue = deque(list(self.queue)[:position] + list(self.queue)[position+1:])

    def is_empty(self):
        # Check if the queue is empty
        return len(self.queue) == 0

    def length(self):
        # Return the length of the queue
        return len(self.queue)

class HospitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Queue System")

        self.hospital_queue = HospitalQueue()

        self.label_name = tk.Label(root, text="Patient Name:")
        self.label_name.grid(row=0, column=0, padx=10, pady=10)

        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_age = tk.Label(root, text="Patient Age:")
        self.label_age.grid(row=1, column=0, padx=10, pady=10)

        self.entry_age = tk.Entry(root)
        self.entry_age.grid(row=1, column=1, padx=10, pady=10)

        self.register_button = tk.Button(root, text="Register Patient", command=self.register_patient)
        self.register_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.label_current_position = tk.Label(root, text="Current Position:")
        self.label_current_position.grid(row=3, column=0, padx=10, pady=10)

        self.entry_current_position = tk.Entry(root)
        self.entry_current_position.grid(row=3, column=1, padx=10, pady=10)

        self.label_new_position = tk.Label(root, text="New Position:")
        self.label_new_position.grid(row=4, column=0, padx=10, pady=10)

        self.entry_new_position = tk.Entry(root)
        self.entry_new_position.grid(row=4, column=1, padx=10, pady=10)

        self.move_button = tk.Button(root, text="Move Patient", command=self.move_patient)
        self.move_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.remove_button = tk.Button(root, text="Remove Patient", command=self.remove_patient)
        self.remove_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.queue_length_label = tk.Label(root, text="Queue Length:")
        self.queue_length_label.grid(row=7, column=0, columnspan=2, pady=10)

        self.queue_length_text = tk.Label(root, text="0")
        self.queue_length_text.grid(row=8, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(root, columns=("Priority", "Name", "Age"), show="headings")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.grid(row=9, column=0, columnspan=2, pady=10)

    #methods for how the buttons work
    def register_patient(self):
        name = self.entry_name.get()
        age = int(self.entry_age.get())

        patient = Patient(name, age)
        self.hospital_queue.enqueue(patient)
        self.update_queue_display()

    def move_patient(self):
        current_position = int(self.entry_current_position.get())
        new_position = int(self.entry_new_position.get())

        self.hospital_queue.move_patient(current_position - 1, new_position - 1)
        self.update_queue_display()

    def remove_patient(self):
        position_str = self.entry_current_position.get()
        if position_str.isdigit():
            position = int(position_str)
            self.hospital_queue.remove_patient(position - 1)
            self.update_queue_display()

    def update_queue_display(self):
        self.tree.delete(*self.tree.get_children())
        priority = 1
        for patient in self.hospital_queue.queue:
            self.tree.insert("", "end", values=(priority, patient.name, patient.age))
            priority += 1

        self.queue_length_text.config(text=str(self.hospital_queue.length()))

if __name__ == "__main__":
    root = tk.Tk()
    gui = HospitalGUI(root)
    root.mainloop()
