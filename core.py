import math

def cidr_to_mask(cidr):
    liste = []
    sortie = ""
    cidr = int(cidr)
    if cidr == 32:
        return "255.255.255.255"
    while cidr >= 8:
        cidr -= 8
        liste.append(8)
    liste.append(cidr)
    for i in liste:
        sortie += str(256 - 2**(8 - i)) + "."
    sortie = sortie[:-1]
    return sortie

def mask_to_cidr(mask):
    numbers = mask.split(".")
    sum = 0
    for i in numbers:
        sum += math.log2(int(i) + 1)
    return int(sum)

def net_to_bits(net):
    octet = net.split(".")
    salida = []
    for i in octet:
        # Convert the octet to binary and remove the '0b' prefix, then pad it to 8 digits
        salida.append(bin(int(i))[2:].zfill(8))
    return "".join(salida)

def bits_to_net(str_bits):
    list=[]
    for i in range(0,4):
            list.append(str_bits[:7])
            str_bits=str_bits[8:]
    return "".join(list)

class Network:
    def __init__(self, net, cidr):
        self.net = net
        self.mask_cidr = int(cidr)
        self.mask = cidr_to_mask(cidr)
        self.mask_bits = net_to_bits(self.mask)
        self.net_bits = net_to_bits(net)
        self.nb_of_hosts = 2**(32-int(cidr))
        self.broadcast_bits = "".join([self.net_bits[i] if i < self.mask_cidr else '1' for i in range(32)])
        self.broadcast = bits_to_net(self.broadcast_bits)
        self.network_addr_bits = "".join([self.net_bits[i] if i < self.mask_cidr else '0' for i in range(32)])
        self.network_addr = bits_to_net(self.network_addr_bits)

    def subnet_in_x_net(self, x):
        if x <= 0:
            return []

        subnets = []
        new_cidr = self.mask_cidr + math.ceil(math.log2(x))
        if new_cidr > 32:
            return []

        subnet_mask = cidr_to_mask(new_cidr)
        subnet_size = 2 ** (32 - new_cidr)

        # Generate subnets
        for i in range(x):
            subnet_addr = self.network_addr_bits + format(i * subnet_size, '032b')[self.mask_cidr:new_cidr]
            subnet = Network(bits_to_net(subnet_addr), str(new_cidr))
            subnets.append(subnet)

        return subnets