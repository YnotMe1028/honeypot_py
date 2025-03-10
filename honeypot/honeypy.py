# Import library dependencies.
import argparse
from ssh_honeypot import *

if __name__ == "__main__":
    # Create parser and add arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, required=True, help="IP address to bind the honeypot.")
    parser.add_argument('-p', '--port', type=int, required=True, help="Port number to bind the honeypot.")
    parser.add_argument('-u', '--username', type=str, help="Username for SSH login simulation.")
    parser.add_argument('-pw', '--password', type=str, help="Password for SSH login simulation.")
    
    parser.add_argument('-s', '--ssh', action="store_true", help="Run SSH honeypot.")
    parser.add_argument('-w', '--http', action="store_true", help="Run HTTP honeypot (Not implemented).")
    
    args = parser.parse_args()
    
    # Check if either SSH or HTTP is selected
    if not (args.ssh or args.http):
        print("[!] Error: You must select at least one honeypot type: --ssh or --http.")
        exit(1)
    
    # Parse the arguments based on user-supplied argument.
    try:
        if args.ssh:
            print("[-] Running SSH Honeypot...")
            
            # Check if username and password are provided, otherwise set them to None
            username = args.username if args.username else None
            password = args.password if args.password else None
            
            # Start the SSH honeypot
            honeypot(args.address, args.port, username, password)

        elif args.http:
            print("[-] Running HTTP Wordpress Honeypot... (Not yet implemented)")
            pass

    except KeyboardInterrupt:
        print("\n[!] Program exited by user.")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
