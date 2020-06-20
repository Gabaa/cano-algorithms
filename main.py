import sys

from cano_alg import lan


def send_command(l, *args):
    if len(args) != 2:
        print('Need 2 arguments.')
        return

    src_node = l.find_node_with_name(args[0])

    if src_node is None:
        print(f"Cannot find any nodes named {src_node}")
        return

    if not isinstance(src_node, lan.Address):
        print(f'{src_node} is not an address')
        return

    src_node.send_message(args[1])

def view_command(l, *args):
    if len(args) != 1:
        print('Need 1 argument.')
        return
    
    node = l.find_node_with_name(args[0])

    if node is None:
        print(f"Cannot find any nodes named {node}")
        return

    if not isinstance(node, lan.Switch):
        print(f"{node} is not a switch")
        return

    node.print_forwarding_table()

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        l = lan.LAN.setup(filename=filename)
    else:
        l = lan.LAN.setup()

    print('Enter commands now.')

    running = True
    while running:
        line = input("> ").strip()
        
        if line == "":
            continue

        args = line.split()
        command = args.pop(0).lower()

        if command == 'send':
            send_command(l, *args)
        elif command == 'view':
            view_command(l, *args)
        elif command == 'exit':
            running = False
        else:
            print(f"Unknown command '{command}', please try again.")
            

if __name__ == "__main__":
    main()