import pandas as pd
import pandas_aiohttp
assert pandas_aiohttp # Prevents unused import warning
import pytest

@pytest.mark.asyncio
async def test_queries():
    frame = pd.DataFrame(
        columns=["A", "B"],
        data =[
            ["XY",23],
            ["YZ", 34],
            ["ZX", 45]
        ]
    )

    result = await (
        "https://httpbin.org/get"
        +"?A="+frame["A"]
        +"&B="+frame["B"].astype(str)
    ).aiohttp.get_json()

    assert result.iloc[1]["args"] == {"A": "YZ", "B": "34"}
