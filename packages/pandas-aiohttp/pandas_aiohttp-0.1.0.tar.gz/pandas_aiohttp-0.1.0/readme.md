# pandas aiohttp plugin <!-- omit in toc -->

Adds the functions `Series.aiohttp.get_text()` and `Series.aiohttp.get_json()`
to pandas Series objects.

- [1. Usage Notes](#1-usage-notes)
- [2. Examples](#2-examples)
  - [2.1. `Series.aiohttp.get_text()`](#21-seriesaiohttpget_text)
  - [2.2. `Series.aiohttp.get_json()`](#22-seriesaiohttpget_json)
  - [2.3. Manual Async Runtime](#23-manual-async-runtime)


## 1. Usage Notes

Both `get_text()` and `get_json()` support the parameters `limit:int=100` and
`ssl:bool=True` which limit concurrent connections and enable or disable SSL
verification, respectively. More features may be supported in the future.

## 2. Examples

>The following examples assume that you are running in a Jupyter notebook.
>
> If you are running in a regular python environment, you will need to use the
>`asyncio.run()` function to run the code. See the last example.

### 2.1. `Series.aiohttp.get_text()`

```python
import pandas as pd
import pandas_aiohttp
# The next line is only needed if you want to prevent your IDE from highlighting as "unused import"
assert pandas_aiohttp

post_urls = pd.Series([
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
])

data = await post_urls.aiohttp.get_text()
```

```text
0    {\n  "userId": 1,\n  "id": 1,\n  "title": "sun...
1    {\n  "userId": 1,\n  "id": 2,\n  "title": "qui...
dtype: object
```

### 2.2. `Series.aiohttp.get_json()`

A more common usage pattern;

```python
import pandas as pd
import pandas_aiohttp

# create an example data frame:
frame = pd.DataFrame(
    columns=["A", "B"],
    data =[
        ["XY",23],
        ["YZ", 34],
        ["ZX", 45]
    ]
)

# Build a series of urls from the dataframe columns,
# and assign to a new column named "data":
frame["data"] = await (
    "https://httpbin.org/get"
    +"?A="+frame["A"]
    +"&B="+frame["B"].astype(str)
).aiohttp.get_json()

result
```

```text
0    {'args': {'A': 'XY', 'B': '23'}, 'headers': {'...
1    {'args': {'A': 'YZ', 'B': '34'}, 'headers': {'...
2    {'args': {'A': 'ZX', 'B': '45'}, 'headers': {'...
dtype: object
```

### 2.3. Manual Async Runtime

If you are running in a regular python environment, you will need to use the
`asyncio.run()` function to run the code.

```python
import pandas as pd
import pandas_aiohttp
import asyncio

post_urls = pd.Series([
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
])

async def main():
    data = await post_urls.aiohttp.get_text()
    print(data)

asyncio.run(main())
```
