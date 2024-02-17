# run-as-admin

## Introduction
This script provides a simple way to execute a file as an administrator on Windows systems. It utilizes the `RunAsAdmin` class to handle the execution and logging of commands. By running a file as an administrator, it bypasses the usual User Account Control (UAC) prompts.

## Installation
You can install run-as-admin via pip:
```bash
pip install run-as-admin
```

## Example Usage
Install 


```python
import os
from run_as_admin import RunAsAdmin

# Define the file path of the executable
file_path = "C:\Windows\System32\cmd.exe"  # Replace this with the actual file path

# Define the path for the log file
log_file_path = os.path.join(os.getcwd(), "execution_log.log")

# Create a RunAsAdmin instance
runner = RunAsAdmin(file_path, True,log_file_path)

# Execute the file as administrator
runner.execute()
```


## Parameters
- `file_path` (str): The path to the executable file you want to run.
- `logging` (bool): Set to `True` if you want to keep log, `False` otherwise.
- `log_file_path` (str, optional): The path to the log file where execution details will be saved. If not specified, `execution_log.log` file will be created in current directory.

## Reminder
If you do not want the UAC prompt to appear when executing the file, you can adjust the User Account Control settings. However, it's important to note that disabling UAC entirely for administrators can pose security risks.

### Local Security Policy
In the Local Security Policy settings, navigate to:
```rust
Security Settings -> Local Policies -> Security Options
```

Adjust the behavior of the User Account Control: Run all administrators in Admin Approval Mode. Disabling this policy will effectively disable UAC for administrators, but it's not recommended for security reasons.

## Dependencies
- Python 3.x
- Windows operating system

## License
Copyright (c) 2024 Barno Chakraborty

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.