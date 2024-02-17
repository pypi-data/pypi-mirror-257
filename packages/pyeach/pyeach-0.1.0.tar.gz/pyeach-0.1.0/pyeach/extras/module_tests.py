"""
tests is a collection of unit tests.
"""


def check_df_one_to_one(df, target):
    """Check that a dataframe is one row per unique value of the target.

    Args:
        df (pd.DataFrame): Pandas dataframe for evaluation.
        target (_type_): Column name to compare rows to unique values.

    Raises:
        ValueError: Raise an error when rows and unique values of target are not equal.
    """
    rows = df.shape[0]
    check = df[target].nunique()
    if rows != check:
        raise ValueError(f"Rows of dataframe do not equal the number of unique values of {target}.")
