def repr_list_as_pd_dataframe(list_arg: list):  # type: ignore
    try:
        import pandas as pd
    except Exception as err:
        raise ModuleNotFoundError("To use this method, please install pandas first") from err
    return pd.DataFrame(list_arg)
