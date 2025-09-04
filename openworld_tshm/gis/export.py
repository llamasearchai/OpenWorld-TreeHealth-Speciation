from __future__ import annotations
import pandas as pd
try:
    import sqlite_utils  # type: ignore
except Exception:  # pragma: no cover
    sqlite_utils = None  # type: ignore


def export_trees_sqlite(df: pd.DataFrame, db_path: str = "forest.db", table: str = "trees") -> None:
    if sqlite_utils is None:
        # Lightweight fallback: write CSV next to DB path to avoid hard dependency in tests
        csv_path = db_path + ".csv"
        df.to_csv(csv_path, index=False)
        return
    db = sqlite_utils.Database(db_path)
    db[table].insert_all(df.to_dict(orient="records"), pk="label", replace=True)


