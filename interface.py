import customtkinter as ctk
from tkinter import ttk
from core import Network
from CTkMessagebox import CTkMessagebox

class NetworkApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Diluvio Subnet Calculator")
        self.geometry("600x600")  # Larger window size

        # Create a tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=40, pady=40, fill="both", expand=True)  # Increase padx and pady

        self.cool = ctk.CTkFont(family='roboto', size=20)

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

        # Frame to hold the main subnet table and scrollbar
        self.table_frame = ctk.CTkFrame(self.show_subnets_frame)
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))  # Increase padx and pady

        # Main Table to display subnets
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

        # Scrollbar for the main subnet table
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.subnets_table.yview)
        self.subnets_table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.subnets_table.pack(side="left", fill="both", expand=True)

        self.show_subnets_frame.pack()

        # Frame to hold the detailed subnet information
        self.detail_frame = ctk.CTkFrame(self.show_subnets_frame)
        self.detail_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))  # Increase padx and pady

        # Label for the detailed subnet information
        self.detail_label = ctk.CTkLabel(self.detail_frame, text="Selected Subnet Details:", wraplength=800)
        self.detail_label.pack(pady=(20, 0))  # Increase pady

        # Detailed Subnet Table
        self.detail_table = ttk.Treeview(self.detail_frame, columns=("Attribute", "Value"))
        self.detail_table.heading("#0", text="Attribute", anchor="center")
        self.detail_table.heading("Attribute", text="Attribute")
        self.detail_table.heading("Value", text="Value")

        # Resize columns
        self.detail_table.column("#0", width=200)
        self.detail_table.column("Attribute", width=200)
        self.detail_table.column("Value", width=200)

        self.detail_table.pack(side="left", fill="both", expand=True)

        # Scrollbar for the detailed subnet table
        self.detail_scrollbar = ttk.Scrollbar(self.detail_frame, orient="vertical", command=self.detail_table.yview)
        self.detail_table.configure(yscrollcommand=self.detail_scrollbar.set)
        self.detail_scrollbar.pack(side="right", fill="y")

        # Handle event when item is selected in the main subnet table
        self.subnets_table.bind("<ButtonRelease-1>", self.show_subnet_details)

    def show_network_info(self):
        net_address = self.net_entry.get()
        cidr = self.cidr_entry.get()

        if net_address and cidr:
            if(Network.is_valid_cidr(cidr) and Network.is_valid_ipv4(net_address)):
                try:
                    network = Network(net_address, cidr)
                    info = f"Network Address: {network.network_addr}\n"
                    info += f"Broadcast Address: {network.broadcast}\n"
                    info += f"Subnet Mask: {network.mask}\n"
                    info += f"Number of Hosts: {network.nb_of_hosts}\n"
                    initialIP=f"Initial inputed IP @: {network.net}"
                    self.network_info_label.configure(text=info)
                    self.clear_subnets_table()  # Clear subnets table when showing network info
                except ValueError as e:
                    CTkMessagebox(title="Error", message=str(e), icon="warning")
            else:
                CTkMessagebox(title="Error", message="Please enter a valid network address and CIDR.", icon="cancel")
        else:
            CTkMessagebox(title="Error", message="Please enter network address and CIDR.", icon="warning")


    def generate_subnets(self):
        num_subnets = self.num_subnets_entry.get()
        if num_subnets.isdigit():
            num_subnets = int(num_subnets)
            if num_subnets > 0:
                self.clear_subnets_table()
                network = Network(self.net_entry.get(), self.cidr_entry.get())
                if(num_subnets>network.nb_of_hosts):
                    CTkMessagebox(title="Error", message="Please enter a littler amount of hosts",icon="cancel")
                else:
                    subnets = network.subnet_in_x_net(num_subnets)

                    # Populate table with subnet information
                    for i, subnet in enumerate(subnets):
                        self.subnets_table.insert("", "end", text=f"{i+1}", values=(subnet.network_addr, subnet.broadcast, subnet.mask))
            else:
                CTkMessagebox(title="Error", message="Please enter a positive number of subnets.",icon="cancel")
        else:
            CTkMessagebox(title="Error", message="Please enter a valid number.",icon="cancel")

    def clear_subnets_table(self):
        # Delete all items in the treeview
        for item in self.subnets_table.get_children():
            self.subnets_table.delete(item)

    def show_subnet_details(self, event):
        item = self.subnets_table.selection()[0]
        subnet = self.subnets_table.item(item)

        # Clear existing details
        for child in self.detail_table.get_children():
            self.detail_table.delete(child)

        # Add new details
        details = [
            ("Subnet Address", subnet["values"][0]),
            ("Broadcast Address", subnet["values"][1]),
            ("Subnet Mask", subnet["values"][2])
        ]

        for attr, value in details:
            self.detail_table.insert("", "end", text=attr, values=(attr, value))


if __name__ == "__main__":
    app = NetworkApp()
    app.mainloop()
