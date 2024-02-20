from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from polars_api_compat.spec import DataFrame
    from polars_api_compat.spec import LazyFrame
    from polars_api_compat.spec import Namespace


def to_polars_api(df: Any, version: str) -> tuple[LazyFrame, Namespace]:
    if hasattr(df, "__polars_api_compat__"):
        return df.__polars_api_compat__()
    try:
        import polars as pl
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(df, pl.DataFrame):
            return df.lazy(), pl  # type: ignore[return-value]
        if isinstance(df, pl.LazyFrame):
            return df, pl  # type: ignore[return-value]
    try:
        import pandas as pd
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(df, pd.DataFrame):
            from polars_api_compat.pandas_like import translate

            return translate(df, api_version=version, implementation="pandas")
    try:
        import cudf
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(df, cudf.DataFrame):
            from polars_api_compat.pandas_like import translate

            return translate(df, api_version=version, implementation="cudf")
    msg = f"Could not translate DataFrame {type(df)}, please open a feature request."
    raise TypeError(msg)


def quick_translate(df: Any, version: str, implementation: str) -> DataFrame:
    """Translate to Polars API, if implementation is already known."""
    if implementation in ("pandas", "cudf"):
        from polars_api_compat.pandas_like import translate

        df, _pl = translate(df, api_version=version, implementation=implementation)
        return df
    msg = f"Unknown implementation: {implementation}"
    raise TypeError(msg)


def to_original_object(df: DataFrame | LazyFrame) -> Any:
    try:
        import polars as pl
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(df, (pl.DataFrame, pl.LazyFrame)):
            return df
    return df.dataframe  # type: ignore[union-attr]


def get_namespace(obj: Any, implementation: str | None = None) -> Namespace:
    if implementation == "polars":
        import polars as pl

        return pl  # type: ignore[return-value]
    try:
        import polars as pl
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(obj, (pl.DataFrame, pl.LazyFrame, pl.Series)):
            return pl  # type: ignore[return-value]
    if hasattr(obj, "__dataframe_namespace__"):
        return obj.__dataframe_namespace__()
    if hasattr(obj, "__series_namespace__"):
        return obj.__series_namespace__()
    if hasattr(obj, "__lazyframe_namespace__"):
        return obj.__lazyframe_namespace__()
    if hasattr(obj, "__expr_namespace__"):
        return obj.__expr_namespace__()
    msg = f"Could not find namespace for object {obj}"
    raise TypeError(msg)
