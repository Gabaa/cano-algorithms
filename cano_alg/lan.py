import sys

class LAN:
    def __init__(self, addresses, switches):
        self.addresses = addresses
        self.switches = switches

    def find_node_with_name(self, name):
        for switch in self.switches:
            if switch.name == name:
                return switch

        for address in self.addresses:
            if address.name == name:
                return address
        
        return None

    @classmethod
    def setup(cls, filename):
        reading_from_stdin = filename is None
        if not reading_from_stdin:
            f = open(filename, 'r')
        else:
            f = sys.stdin
        
        try:
            if reading_from_stdin:
                print("Enter names of all the addresses (space separated):")
            addresses = {a: Address(a) for a in f.readline().split()}

            if reading_from_stdin:
                print("\nEnter names of all the switches (space separated):")
            switches = {s: Switch(s) for s in f.readline().split()}

            if reading_from_stdin:
                print("\nEnter all the connections.")
                print("Two space separated items, 1 connection per line, end with empty line.")
                print('> ', end='', flush=True)
            line = f.readline()
            while line.strip() != "":
                a, b = line.split()
                if a in addresses:
                    a = addresses[a]
                elif a in switches:
                    a = switches[a]
                else:
                    if reading_from_stdin:
                        print(f"Could not find any item matching {a}")
                    continue

                if b in addresses:
                    b = addresses[b]
                elif b in switches:
                    b = switches[b]
                else:
                    if reading_from_stdin:
                        print(f"Could not find any item matching {b}")
                    continue

                Interface(a, b)

                if reading_from_stdin:
                    print('> ', end='', flush=True)
                line = f.readline()
            
            l = cls(list(addresses.values()), list(switches.values()))
        except:
            print('Something went wrong.')
        finally:
            if f is not sys.stdin:
                f.close()
        
        return l

class Node:
    def receive(self, interface, src_name, dest_name):
        raise NotImplementedError

    def set_interface(self, interface):
        pass

class Interface:
    a: Node
    b: Node

    def __init__(self, a, b):
        self.a = a
        a.set_interface(self)
        self.b = b
        b.set_interface(self)

    def send_message(self, sender, src_name, dest_name):
        if sender == self.a:
            return self.b.receive(self, src_name, dest_name)
        elif sender == self.b:
            return self.a.receive(self, src_name, dest_name)
        else:
            raise ValueError("Sent from invalid source")

class Switch(Node):
    def __init__(self, name):
        self.name = name
        self.interfaces = []
        self.forwarding_table = {}

    def __repr__(self):
        return f'Switch {self.name}'

    def set_interface(self, interface):
        self.interfaces.append(interface)

    def receive(self, interface, src_name, dest_name):
        print(f"Switch {self.name}: {src_name} -> {dest_name}")

        self.forwarding_table[src_name] = interface

        if dest_name in self.forwarding_table:
            self.forwarding_table[dest_name].send_message(self, src_name, dest_name)
        else:
            for i in self.interfaces:
                if i == interface:
                    continue
                i.send_message(self, src_name, dest_name)

    def print_forwarding_table(self):
        print(f"Forwarding table of Switch {self.name}")

        for (src, interface) in self.forwarding_table.items():
            print(f"| {src} | {self.interfaces.index(interface)} |")

class Address(Node):
    def __init__(self, name):
        self.name = name
        self.interface = None

    def __repr__(self):
        return f'Address {self.name}'

    def set_interface(self, interface):
        self.interface = interface

    def send_message(self, dest_name):
        self.interface.send_message(self, self.name, dest_name)

    def receive(self, interface, src_name, dest_name):
        if dest_name == self.name:
            print(f"Message from {src_name} received at {self.name}")