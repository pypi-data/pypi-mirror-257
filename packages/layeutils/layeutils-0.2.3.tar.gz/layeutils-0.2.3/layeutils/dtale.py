import pandas as pd


def dtale_start(df: pd.DataFrame, precision=None) -> str:
    """利用Vscode端口映射启动dtale

    Args:
        df (pd.DataFrame): 目标DF

    Returns:
        str: dtale内部地址
    """
    import dtale
    d = dtale.show(df, precision=precision)
    return f"http://localhost:{d._main_url.split(':')[-1]}"
