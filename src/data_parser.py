import pandas as pd
from typing import List

def get_dataframe_from_csv(filepath: str) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame.
    Args:
        filepath (str): Path of the CSV file.
    Returns:
        pd.DataFrame: DataFrame containing the CSV data.
    """
    return pd.read_csv(filepath)

def generate_header_from_dataframe(data_frame: pd.DataFrame) -> List[str]:
    """Generate SQL-compatible column definitions from a DataFrame.
    Args:
        data_frame (pd.DataFrame): The DataFrame from which to generate column definitions.
    Returns:
        List[str]: A list of SQL column definitions for each column in the DataFrame.
    """
    columns = []
    for col in data_frame.columns:
        if pd.api.types.is_integer_dtype(data_frame[col]):
            if data_frame[col].min() < -2147483648 or data_frame[col].max() > 2147483647:
                columns.append(f'"{col}" BIGINT')
            else:
                columns.append(f'"{col}" INT')
        elif pd.api.types.is_float_dtype(data_frame[col]):
            columns.append(f'"{col}" FLOAT')
        else:
            columns.append(f'"{col}" VARCHAR(255)')

    return columns

def generate_header_from_csv(filepath: str) -> List[str]:
    """Generate SQL-compatible headers from a CSV file.
    Args:
        filepath (str): Path of the CSV file.
    Returns:
        List[str]: List of column definitions suitable for SQL table creation.
    """
    df = get_dataframe_from_csv(filepath)

    return generate_header_from_dataframe(df)
