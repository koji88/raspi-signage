#!/usr/bin/env python
# -*- coding:utf-8



import sys
import time
import argparse
import json
import requests

def sendCommand(args):
    server = "http://{0}:{1}".format(args.remote,args.port)
    data = {}
    
    if "exit" == args.command:
        data["command"] = "exit"
    elif "func" == args.command:
        data["command"] = "func"
        data["num"] = args.num
    else:
        print("unrecognized command")
        return False

    response = requests.post(server,json.dumps(data),headers={'Content-Type': 'application/json'})
    return response.json().get("result",False)

def main():
    p = argparse.ArgumentParser(description='Raspberry pi Digital Signage Remote Controller')
    p.add_argument("-r","--remote",default="localhost", help="remote server address")
    p.add_argument("--command",help="command for control remote server")
    p.add_argument("--num",help="func num for control remote server")
    p.add_argument("-p","--port", default=8888, type=int,help="listen http port")
    args = p.parse_args()

    return 0 if sendCommand(args) else 1

if __name__ == "__main__":
    sys.exit(main())
    
