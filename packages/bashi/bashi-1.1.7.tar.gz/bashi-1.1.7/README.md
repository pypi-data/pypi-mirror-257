# ibash


## Installation : 
```bash 
pip install bashi
```
## Quick start : 
```python 
from bashi import bash

result = bash("ls")
if result.code == 0 : 
    stdout = result.stdout 
    stderr = result.stderr

result2 = bash("not working command ")
```

<pre><span style="background-color:#26A269"><b> $ ls          </b></span>
main.py

<span style="background-color:#26A269"><b> $ not working command           </b></span><font color="#C01C28"><b> ==&gt; code 127</b></font>
<font color="#C01C28">/bin/sh: 1: not: not found)</font>
</pre>