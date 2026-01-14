from __future__ import annotations

import json
from copy import copy
from datetime import date
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from cloudscraper import CloudScraper

from dtos import Result, ResultList


def _to_int_list(nodes) -> list[int]:
    out: list[int] = []
    for n in nodes:
        t = (n.get_text() or "").strip()
        t = t.replace(".", "").replace(",", "").replace(" ", "")
        if t.isdigit():
            out.append(int(t))
    return out


class Lottery:
    def __init__(self) -> None:
        self._http = CloudScraper()
        self._data: Dict[date, Result] = {}

        self._raw_data: pd.DataFrame = pd.DataFrame()
        self._2_digits_data: pd.DataFrame = pd.DataFrame()
        self._sparse_data: pd.DataFrame = pd.DataFrame()

        self._last_date: date = date.today()

    def load(self, path: str = "data/xsmb.json") -> None:
        p = Path(path)
        if not p.exists():
            return
        data = ResultList.model_validate_json(p.read_text(encoding="utf-8"))
        for d in data.root:
            self._data[d.date] = d
        self.generate_dataframes()

    def save_json(self, path: str = "data/xsmb.json") -> None:
        Path("data").mkdir(parents=True, exist_ok=True)
        lst = sorted(self._data.values(), key=lambda r: r.date)
        payload = [r.model_dump(mode="json") for r in lst]
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def dump(self) -> None:
        Path("data").mkdir(parents=True, exist_ok=True)

        def _dump(df: pd.DataFrame, file_name: str) -> None:
            df.to_csv(f"data/{file_name}.csv", index=False)
            df.to_json(
                f"data/{file_name}.json",
                orient="records",
                date_format="iso",
                indent=2,
                index=False,
                force_ascii=False,
            )
            df.to_parquet(f"data/{file_name}.parquet", index=False)

        _dump(self._raw_data, "xsmb")
        _dump(self._2_digits_data, "xsmb-2-digits")
        _dump(self._sparse_data, "xsmb-sparse")

    def fetch(self, selected_date: date) -> Optional[Result]:
        url = f"https://xoso.com.vn/xsmb-{selected_date:%d-%m-%Y}.html"
        resp = self._http.get(url, timeout=30)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "lxml")

        special = _to_int_list(soup.find_all(attrs={"class": "special-prize"}))
        if not special:
            return None

        prize1 = _to_int_list(soup.find_all(attrs={"class": "prize1"}))
        prize2 = _to_int_list(soup.find_all(attrs={"class": "prize2"}))
        prize3 = _to_int_list(soup.find_all(attrs={"class": "prize3"}))
        prize4 = _to_int_list(soup.find_all(attrs={"class": "prize4"}))
        prize5 = _to_int_list(soup.find_all(attrs={"class": "prize5"}))
        prize6 = _to_int_list(soup.find_all(attrs={"class": "prize6"}))
        prize7 = _to_int_list(soup.find_all(attrs={"class": "prize7"}))

        if not (
            len(prize1) >= 1
            and len(prize2) >= 2
            and len(prize3) >= 6
            and len(prize4) >= 4
            and len(prize5) >= 6
            and len(prize6) >= 3
            and len(prize7) >= 4
        ):
            return None

        result = Result(
            date=selected_date,
            special=special[0],
            prize1=prize1[0],
            prize2_1=prize2[0],
            prize2_2=prize2[1],
            prize3_1=prize3[0],
            prize3_2=prize3[1],
            prize3_3=prize3[2],
            prize3_4=prize3[3],
            prize3_5=prize3[4],
            prize3_6=prize3[5],
            prize4_1=prize4[0],
            prize4_2=prize4[1],
            prize4_3=prize4[2],
            prize4_4=prize4[3],
            prize5_1=prize5[0],
            prize5_2=prize5[1],
            prize5_3=prize5[2],
            prize5_4=prize5[3],
            prize5_5=prize5[4],
            prize5_6=prize5[5],
            prize6_1=prize6[0],
            prize6_2=prize6[1],
            prize6_3=prize6[2],
            prize7_1=prize7[0],
            prize7_2=prize7[1],
            prize7_3=prize7[2],
            prize7_4=prize7[3],
        )

        self._data[result.date] = result
        return result

    def generate_dataframes(self) -> None:
        if not self._data:
            self._raw_data = pd.DataFrame()
            self._2_digits_data = pd.DataFrame()
            self._sparse_data = pd.DataFrame()
            return

        self._raw_data = pd.DataFrame([d.model_dump() for d in self._data.values()])
        self._raw_data["date"] = pd.to_datetime(self._raw_data["date"])
        self._raw_data.iloc[:, 1:] = self._raw_data.iloc[:, 1:].astype("int64")
        self._raw_data = self._raw_data.sort_values("date").reset_index(drop=True)

        self._2_digits_data = copy(self._raw_data)
        self._2_digits_data.iloc[:, 1:] = self._2_digits_data.iloc[:, 1:].apply(lambda x: x % 100)

        cols = [f"{i:02d}" for i in range(100)]
        zeros = pd.DataFrame(
            np.zeros((self._2_digits_data.shape[0], 100), dtype="int64"),
            columns=cols,
        )
        self._sparse_data = pd.concat([self._2_digits_data[["date"]], zeros], axis=1)

        for i in range(self._2_digits_data.shape[0]):
            counts = self._2_digits_data.iloc[i, 1:].value_counts()
            for k, v in counts.items():
                self._sparse_data.at[i, f"{int(k):02d}"] = int(v)

        self._last_date = self._raw_data["date"].max().to_pydatetime().date()

    def get_raw_data(self) -> pd.DataFrame:
        return self._raw_data

    def get_2_digits_data(self) -> pd.DataFrame:
        return self._2_digits_data

    def get_sparse_data(self) -> pd.DataFrame:
        return self._sparse_data

    def get_last_date(self) -> date:
        return self._last_date
