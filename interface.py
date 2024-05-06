import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from core import Network
import math

class NetworkApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Diluvio Subnet Calculator")
        self.geometry("1000x600")  # Larger window size

        # Create a tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=40, pady=40, fill="both", expand=True)  # Increase padx and pady

        # Configure Network tab
        self.configure_network_tab = self.tabview.add("Configure Network")
        self.configure_network_frame = ctk.CTkFrame(self.configure_network_tab)
        self.net_label = ctk.CTkLabel(self.configure_network_frame, text="Network Address:")
        self.net_label.grid(row=0, column=0, padx=10, pady=10)  # Increase padx and pady
        self.net_entry = ctk.CTkEntry(self.configure_network_frame)
        self.net_entry.grid(row=0, column=1, padx=10, pady=10)  # Increase padx and pady

        self.cidr_label = ctk.CTkLabel(self.configure_network_frame, text="CIDR:")
        self.cidr_label.grid(row=1, column=0, padx=10, pady=10)  # Increase padx and pady
        self.cidr_entry = ctk.CTkEntry(self.configure_network_frame)
        self.cidr_entry.grid(row=1, column=1, padx=10, pady=10)  # Increase padx and pady

        self.configure_button = ctk.CTkButton(self.configure_network_frame, text="Configure", command=self.show_network_info)
        self.configure_button.grid(row=2, columnspan=2, pady=20)  # Increase pady

        self.network_info_label = ctk.CTkLabel(self.configure_network_frame, text="", wraplength=800)  # Increase wraplength
        self.network_info_label.grid(row=3, columnspan=2, padx=10, pady=20)  # Increase padx and pady

        self.configure_network_frame.pack()

        # Show Subnets tab
        self.show_subnets_tab = self.tabview.add("Show Subnets")
        self.show_subnets_frame = ctk.CTkFrame(self.show_subnets_tab)
        self.subnets_label = ctk.CTkLabel(self.show_subnets_frame, text="Subnets:", wraplength=800)  # Increase wraplength
        self.subnets_label.pack(pady=20)  # Increase pady

        # Entry field for number of subnets
        self.num_subnets_label = ctk.CTkLabel(self.show_subnets_frame, text="Number of Subnets:")
        self.num_subnets_label.pack(pady=(20, 0))  # Increase pady

        self.num_subnets_entry = ctk.CTkEntry(self.show_subnets_frame)
        self.num_subnets_entry.pack()

        # Button to generate subnets
        self.generate_button = ctk.CTkButton(self.show_subnets_frame, text="Generate Subnets", command=self.generate_subnets)
        self.generate_button.pack(pady=20)  # Increase pady

        # Frame to hold the table and scrollbar
        self.table_frame = ctk.CTkFrame(self.show_subnets_frame)
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))  # Increase padx and pady

        # Table to display subnets
        self.subnets_table = ttk.Treeview(self.table_frame, columns=("Subnet Address", "Broadcast Address", "Subnet Mask"))
        self.subnets_table.heading("#0", text="Index", anchor="center")  # Center the index column
        self.subnets_table.heading("Subnet Address", text="Subnet Address")
        self.subnets_table.heading("Broadcast Address", text="Broadcast Address")
        self.subnets_table.heading("Subnet Mask", text="Subnet Mask")

        # Resize columns
        self.subnets_table.column("#0", width=50)  # Adjust the width of the index column
        self.subnets_table.column("Subnet Address", width=200)  # Increase the width of Subnet Address column
        self.subnets_table.column("Broadcast Address", width=200)  # Increase the width of Broadcast Address column
        self.subnets_table.column("Subnet Mask", width=200)  # Increase the width of Subnet Mask column

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.subnets_table.yview)
        self.subnets_table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.subnets_table.pack(side="left", fill="both", expand=True)

        self.show_subnets_frame.pack()

    def show_network_info(self):
        net_address = self.net_entry.get()
        cidr = self.cidr_entry.get()

        if net_address and cidr:
            network = Network(net_address, cidr)

            info = f"Network Address: {network.network_addr}\n"
            info += f"Broadcast Address: {network.broadcast}\n"
            info += f"Subnet Mask: {network.mask}\n"
            info += f"Number of Hosts: {network.nb_of_hosts}\n"
            self.network_info_label.configure(text=info)
            self.clear_subnets_table()  # Clear subnets table when showing network info
        else:
            ctk.messagebox.showerror("Error", "Please enter network address and CIDR.")

    def generate_subnets(self):
        num_subnets = self.num_subnets_entry.get()

        if num_subnets.isdigit():
            num_subnets = int(num_subnets)
            if num_subnets > 0:
                self.clear_subnets_table()
                network = Network(self.net_entry.get(), self.cidr_entry.get())
                subnets = network.subnet_in_x_net(num_subnets)

                # Populate table with subnet information
                for i, subnet in enumerate(subnets):
                    self.subnets_table.insert("", "end", text=f"{i+1}", values=(subnet.network_addr, subnet.broadcast, subnet.mask))
            else:
                ctk.messagebox.showerror("Error", "Please enter a positive number of subnets.")
        else:
            ctk.messagebox.showerror("Error", "Please enter a valid number.")

    def clear_subnets_table(self):
        # Delete all items in the treeview
        for item in self.subnets_table.get_children():
            self.subnets_table.delete(item)


if __name__ == "__main__":
    app = NetworkApp()
    app.mainloop()
