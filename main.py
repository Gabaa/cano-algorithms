import sys
from abc import ABC

from cano_alg.lan import LAN, Address, Switch


class Command(ABC):
    def __init__(self, lan: LAN):
        self.lan: LAN = lan

    def perform(self, *args):
        raise NotImplementedError


class Send(Command):
    def perform(self, *args):
        if len(args) != 2:
            print('Need 2 arguments.')
            return

        src_name = args[0]
        src_node = self.lan.find_node_with_name(src_name)

        if src_node is None:
            print(f"Cannot find any nodes named {src_name}")
            return

        if not isinstance(src_node, Address):
            print(f'{src_node} is not an address')
            return

        src_node.send_message(args[1])


class View(Command):
    def perform(self, *args):
        if len(args) != 1:
            print('Need 1 argument.')
            return

        node = self.lan.find_node_with_name(args[0])

        if node is None:
            print(f"Cannot find any nodes named {args[0]}")
            return

        if not isinstance(node, Switch):
            print(f"{node} is not a switch")
            return

        node.print_forwarding_table()


class Reset(Command):
    def perform(self, *args):
        for switch in self.lan.switches:
            switch.forwarding_table.clear()

        print('Cleared all forwarding tables.')


def main():
    filename = None
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    lan = LAN.setup(filename=filename)

    commands = {
        "send": Send(lan),
        "view": View(lan),
        "reset": Reset(lan)
    }

    print('Enter commands now.')

    running = True
    while running:
        line = input("> ").strip()

        if line == "":
            continue

        args = line.split()
        command = args.pop(0).lower()

        if command == 'help':
            print('You can use the following commands:')
            print(', '.join(list(commands.keys()) + ['help', 'exit']))
        elif command == 'exit':
            running = False
        elif command in commands.keys():
            commands[command].perform(*args)
        else:
            print(f"Unknown command '{command}', please try again.")


if __name__ == "__main__":
    main()
