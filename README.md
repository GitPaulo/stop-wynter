# Stop Wynter

Small program to lock/unlock peripherals to prevent my cat (Wynter) from destroying my pc.

### Pre-reqs

Install based on OS:
- Windows 11: https://learn.microsoft.com/en-gb/windows-hardware/drivers/download-the-wdk#download-icon-for-wdk-step-3-install-wdk
  - Add `devcon` to `PATH` : `C:\Program Files (x86)\Windows Kits\10\Tools\10.0.22621.0\x86` (usually)
- Ubuntu: `sudo apt install xinput`
- MacOS: IDFK yet

> Only those are supported.

Setup,

```sh
python3 -m venv venv
source venv/bin/activate
pip install pynput
```

Step 1- Find out device id

```sh
python3 findid.py
```

Step 2- Edit `config.ini`

Step 3- Run program

```sh
python3 stop-wynter.py
```
