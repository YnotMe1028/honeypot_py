# Libraries
import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko
import threading

# Constants
logging_format = logging.Formatter('%(message)s')
SSH_BANNER = "SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u4\r\n"

host_key = paramiko.RSAKey(filename='server.key')

# Loggers & Logging Files
funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler) 

creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmd_audits.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler) 

# Emulated Shell
def emulated_shell(channel, client_ip):
    channel.send(b'user28-jumpbox2$ ')
    command = b""
    while True:
        try:
            char = channel.recv(1)
            if not char:
                break
            channel.send(char)
            command += char

            if char == b'\r':
                command = command.strip()
                
                if command == b'exit':
                    channel.send(b'\nGoodbye!\n')
                    break
                elif command == b'pwd':
                    response = b'\n/usr/local\r\n'
                    creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
                elif command == b'whoami':
                    response = b'\nuser28\r\n'
                    creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
                elif command == b'ls':
                    response = b'\nmyConfig.conf\r\n'
                    creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
                elif command == b'cat myConfig.conf':
                    response = b'\nGo to myWebSite.com to get more information!\r\n'
                    creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
                else:
                    response = b'\n' + command + b'\r\n'
                    creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')

                channel.send(response)
                channel.send(b'corporate-jumpbox2$ ')
                command = b""
        except Exception as e:
            print(f"Error in shell: {e}")
            break


# SSH Server
class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.input_username = input_username
        self.input_password = input_password

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
    
    def get_allowed_auths(self, username: str) -> str:
        return "password"
    
    def check_auth_password(self, username, password):
        funnel_logger.info(f'Client {self.client_ip} attempted connection with ' + f'username: {username}, ' + f'password: {password}')
        creds_logger.info(f'{self.client_ip}, {username}, {password}')
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL
            
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def check_channel_exec_request(self, channel, command):
        return True

# Handle Client
def client_handle(client, addr, username, password):
    client_ip = addr[0]
    print(f"{client_ip} has connected to the server.")

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(host_key)
        transport.start_server(server=Server(client_ip=client_ip, input_username=username, input_password=password))

        channel = transport.accept(20)
        if channel is None:
            print("No channel was opened")
            return

        # Send standard banner
        standard_banner = "Welcome to Ubuntu 22.04 LTS (HIEU BT)!\r\n\r\n"
        channel.send(standard_banner.encode())

        emulated_shell(channel, client_ip)
        
    except Exception as error:
        print(f"Error: {error}")
    finally:
        try:
            transport.close()
        except:
            pass
        client.close()

# Start SSH Honeypot
def honeypot(address, port, username, password):
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))
    socks.listen(100)

    print(f"SSH server is listening on port {port}.")

    while True:
        try:
            client, addr = socks.accept()
            threading.Thread(target=client_handle, args=(client, addr, username, password)).start()
        except Exception as error:
            print(f"Socket error: {error}")

honeypot('127.0.0.1', 2810, 'username', 'password')
