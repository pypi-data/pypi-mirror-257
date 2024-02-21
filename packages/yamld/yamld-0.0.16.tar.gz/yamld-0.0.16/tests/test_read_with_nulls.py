import pytest
import pandas as pd
from yamld.read import read_onelist_dataframe


yaml_content_with_null = """
config1:
  key1: 'value1'
  key2: 'value2'
  key3: 'value3'

config2:
  keyA: 'valueA'
  keyB: 'valueB'
  keyC: 'valueC'

data:
  - name: 'John Doe'
    age: 30
    city: null
  - name: 'Jane Smith'
    age: null
    city: 'San Francisco'
  - name: null
    age: 35
    city: 'Chicago'
  - name: 'Test'
    age: null
    city: null
"""

def test_read_yaml_to_dataframe_with_null_values():
    # Test case 1: Check if the function returns a DataFrame
    df = read_onelist_dataframe(yaml_content_with_null.splitlines())
    assert isinstance(df, pd.DataFrame)

    # Test case 2: Check if the DataFrame has the correct number of rows
    assert len(df) == 4

    # Test case 3: Check if the DataFrame columns are correct
    expected_columns = ['name', 'age', 'city']
    assert all(col in df.columns for col in expected_columns)

    # Test case 4: Check if the values in the DataFrame are correct, considering pandas NaN values
    expected_values = [
        ['John Doe', 30, None],
        ['Jane Smith', None, 'San Francisco'],
        [None, 35, 'Chicago'],
        ['Test', None, None]
    ]
    for i, row in enumerate(df.itertuples(index=False)):
        assert all(not bool(expected_values[i][j]) or  val == expected_values[i][j] for j, val in enumerate(row))

