import math
import re
def cidr_to_mask(cidr_):
    cidr=int(cidr_)
    if not 0 <= cidr <= 32:
        raise ValueError("CIDR must be between 0 and 32")

    octets = [0, 0, 0, 0]
    for i in range(cidr // 8):
        octets[i] = 255
    if cidr % 8 != 0:
        octets[cidr // 8] = 256 - 2 ** (8 - (cidr % 8))

    return ".".join(map(str, octets))


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
    octets = [str_bits[i:i+8] for i in range(0, len(str_bits), 8)]
    return ".".join(str(int(octet, 2)) for octet in octets)


class Network:
    def __init__(self, net, cidr):
        self.net = net
        self.mask_cidr = int(cidr)
        self.mask = cidr_to_mask(cidr)
        self.mask_bits = net_to_bits(self.mask)
        self.net_bits = net_to_bits(net)
        self.nb_of_hosts = 2**(32-int(cidr))-2
        self.broadcast_bits = "".join([self.net_bits[i] if i < self.mask_cidr else '1' for i in range(32)])
        self.broadcast = bits_to_net(self.broadcast_bits)
        self.network_addr_bits = "".join([self.net_bits[i] if i < self.mask_cidr else '0' for i in range(32)])
        self.network_addr = bits_to_net(self.network_addr_bits)

    def is_valid_ipv4(ip):
        pattern = re.compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        return pattern.match(ip)

    def is_valid_cidr(cidr):
        pattern = re.compile(r'^(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$')
        return pattern.match(cidr) and int(cidr) <= 32 
    
    def subnet_in_x_net(self, x):
        if x <= 0:
            return []

        subnets = []
        new_cidr = self.mask_cidr + math.ceil(math.log2(x))
        if new_cidr > 32:
            return []

        subnet_size = 2 ** (32 - new_cidr)
        num_subnets = 2 ** (new_cidr - self.mask_cidr)

        # Generate subnets
        for i in range(num_subnets):
            subnet_addr_bits = self.network_addr_bits[:self.mask_cidr] + format(i * subnet_size, '0' + str(new_cidr - self.mask_cidr) + 'b')
            subnet = Network(bits_to_net(subnet_addr_bits), str(new_cidr))
            subnets.append(subnet)

        return subnets

