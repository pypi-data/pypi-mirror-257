# Install
``` sh
cd cocotbext-plotData
pip3 install . --user --break-system-packages
or 
pip3 install -e . --user --break-system-packages
```
加了 -e 的话, 相当于在 site-packages 加个软链接, 这样只要原始仓库修改了, 就可以立即生效
# Usage
``` python
import plotData
...
```

