import customtkinter as ctk
from core import Network

class NetworkApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Network Subnet Calculator")
        self.geometry("600x400")

        # Create a tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Configure Network tab
        self.configure_network_tab = self.tabview.add("Configure Network")
        self.configure_network_frame = ctk.CTkFrame(self.configure_network_tab)
        self.net_label = ctk.CTkLabel(self.configure_network_frame, text="Network Address:")
        self.net_label.grid(row=0, column=0, padx=10, pady=5)
        self.net_entry = ctk.CTkEntry(self.configure_network_frame)
        self.net_entry.grid(row=0, column=1, padx=10, pady=5)

        self.cidr_label = ctk.CTkLabel(self.configure_network_frame, text="CIDR:")
        self.cidr_label.grid(row=1, column=0, padx=10, pady=5)
        self.cidr_entry = ctk.CTkEntry(self.configure_network_frame)
        self.cidr_entry.grid(row=1, column=1, padx=10, pady=5)

        self.configure_button = ctk.CTkButton(self.configure_network_frame, text="Configure", command=self.show_network_info)
        self.configure_button.grid(row=2, columnspan=2, pady=10)

        self.network_info_label = ctk.CTkLabel(self.configure_network_frame, text="", wraplength=400)
        self.network_info_label.grid(row=3, columnspan=2, padx=10, pady=5)

        self.configure_network_frame.pack()

        # Show Subnets tab
        self.show_subnets_tab = self.tabview.add("Show Subnets")
        self.show_subnets_frame = ctk.CTkFrame(self.show_subnets_tab)
        self.subnets_label = ctk.CTkLabel(self.show_subnets_frame, text="Subnets:", wraplength=400)
        self.subnets_label.pack(pady=10)

        self.subnets_info_label = ctk.CTkLabel(self.show_subnets_frame, text="", wraplength=400)
        self.subnets_info_label.pack(pady=10)

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
        else:
            ctk.messagebox.showerror("Error", "Please enter network address and CIDR.")

    def calculate(self):
        net_address = self.net_entry.get()
        cidr = self.cidr_entry.get()

        if net_address and cidr:
            network = Network(net_address, cidr)

            subnets = network.subnet_in_x_net(16)
            subnets_info = ""
            for subnet in subnets:
                subnets_info += f"{subnet.network_addr} - {subnet.broadcast}   {subnet.mask}\n"
            self.subnets_info_label.configure(text=subnets_info)
        else:
            ctk.messagebox.showerror("Error", "Please enter network address and CIDR.")

if __name__ == "__main__":
    app = NetworkApp()
    app.mainloop()
