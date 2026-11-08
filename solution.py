import pandas as pd
import re

def add_virtual_column(
    df: pd.DataFrame,
    role: str,
    new_column: str
) -> pd.DataFrame:

    # checking if df exists and is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame([])

    # checking for the supported operators
    operators = ["+", "-", "*"]

    found_operator = None

    for operator in operators:
        if operator in role:
            found_operator = operator
            break

    if found_operator is None:
        return pd.DataFrame([])


    # finding the column names and making sure there are just 2 columns listed
    parts = role.split(found_operator)

    if len(parts) != 2:
        return pd.DataFrame([])

    column_a = parts[0].strip()
    column_b = parts[1].strip()


    # checking whether all provided column names are correct and whether they exist in provided df
    if not re.fullmatch(r"[A-Za-z_]+", column_a):
        return pd.DataFrame([])
 
    if not re.fullmatch(r"[A-Za-z_]+", column_b):
        return pd.DataFrame([])
    
    if not re.fullmatch(r"[A-Za-z_]+", new_column):
        return pd.DataFrame([])

    if column_a not in df.columns or column_b not in df.columns:
        return pd.DataFrame([])


    ### additional checks I decided to add to handle potential edge cases
    ### since undesirable scenarios in task are suppose to return empty df, I decided to follow the logic
    ### edge cases already covered by pandas: not even length of columns a and b (cannot actually occur), missing numerical values (None), different numerical types

    # checking whether both columns contains only numerical values
    if not pd.api.types.is_numeric_dtype(df[column_a]):
        return pd.DataFrame([])

    if not pd.api.types.is_numeric_dtype(df[column_b]):
        return pd.DataFrame([])

    # checking whether new column doesn't have the same name as an existing one, so it wouldn't be overwritten
    if new_column in df.columns:
        return pd.DataFrame([])


    result_df = df.copy()

    # performing calculations if every condition is met
    if found_operator == "+":
        result_df[new_column] = result_df[column_a] + result_df[column_b]
    elif found_operator == "-":
        result_df[new_column] = result_df[column_a] - result_df[column_b]
    elif found_operator == "*":
        result_df[new_column] = result_df[column_a] * result_df[column_b]

    return result_df
