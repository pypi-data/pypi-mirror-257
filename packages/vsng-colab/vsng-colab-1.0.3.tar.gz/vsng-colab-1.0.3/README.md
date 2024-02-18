# vsng-colab


## Installation

```bash
pip install vsng-colab
```

## Example

```python
from vscolabi import configure

configure()
# configure(install = True, port  = 5000 ,folder = "/content" ,kill = True ) : 
#   install : True to install vscode 
#   port    : 5000 , prot to forward vs code server
#   folder  : /content ,folder to open vs code in 
#   kill    : True , call ngrok kill .
```

Steps  : 
*   create secret in colab secrets called NGROK_TOKEN and set its value .
