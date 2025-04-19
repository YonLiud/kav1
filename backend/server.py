import uvicorn
import argparse
import socket
from app.main import app

def parse_args():
    parser = argparse.ArgumentParser(description="Run the server with custom IP and port.")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='IP address to bind the server to')
    parser.add_argument('--port', type=int, default=3000, help='Port number to bind the server to')
    return parser.parse_args()

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def is_valid_port(port):
    return 0 <= port <= 65535

if __name__ == "__main__":
    try:
        args = parse_args()
        if not is_valid_ip(args.host):
            raise ValueError(f"Invalid IP address: {args.host}")
        if not is_valid_port(args.port):
            raise ValueError(f"Invalid port number: {args.port}. Port must be between 0 and 65535.")
        uvicorn.run(app, host=args.host, port=args.port)
    
    except ValueError as e:
        print(f"Error: {e}")
