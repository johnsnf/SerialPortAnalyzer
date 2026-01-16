Quick usage notes:

1. Initializing virtual environment and activate:

```bash
python3 -m venv SerialPortAnalyzer
source SerialPortAnalyzer/bin/activate 
```

or for windows

```powershell
./SerialPortAnalyzer/bin/Activate.sh
```

2. Download required packages;

```bash
pip install -r requirements.txt
```

3. Scan available serial ports 

```bash
python3 ListPorts.py
```

4. Select port from list, and scan for baud rate (note messages should be actively transmitting from source

```bash
python3 ScanSerialBaud.py <portName> --timeOut 2 --printResponse True
```

5. Further interrogate the message

```bash
python3 -i GetSerialData.py <portName> --baudRate <baudRateFromStep4> --timeout 2 
```

6. Data returned from connection is then stored in the "response" variable (decoded 'utf-8' and stripped

```python
print(response)
```
