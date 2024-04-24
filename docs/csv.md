# usage of csv

## write or read csv
```python
from lambkid import CSV
csv=CSV()
head=["类型","价格","数量"]
datas=[
    ["desk",100,10],
    ["table",200,5]
]
csv.write_csv("example.csv",head,datas)
```