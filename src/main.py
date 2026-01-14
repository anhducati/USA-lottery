from __future__ import annotations

import json
import os
import time
from pathlib import Path
import datetime as dt
from zoneinfo import ZoneInfo

import pandas as pd

from lottery import Lottery
from analysis import render_images

TZ_VN = ZoneInfo("Asia/Ho_Chi_Minh")


def vn_today() -> dt.date:
    return dt.datetime.now(tz=TZ_VN).date()


def write_json(path: str, obj) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def write_site_meta(note: str = "") -> None:
    meta = {
        "updated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "updated_at_vn": dt.datetime.now(tz=TZ_VN).isoformat(),
        "run_id": os.getenv("GITHUB_RUN_ID", ""),
        "sha": (os.getenv("GITHUB_SHA", "") or "")[:7],
        "source": "https://xoso.com.vn",
        "note": note,
    }
    write_json("data/site_meta.json", meta)


def make_last7(raw_df: pd.DataFrame) -> list[dict]:
    df = raw_df.copy().sort_values("date").tail(7).reset_index(drop=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    # convert int columns to int for clean JSON
    for c in df.columns:
        if c != "date":
            df[c] = df[c].astype(int)
    return df.to_dict(orient="records")


def main() -> None:
    lot = Lottery()
    lot.load("data/xsmb.json")

    today = vn_today()

    MAX_RETRY = 5       # ~5 phút
    SLEEP_SEC = 60

    fetched_today = False
    for attempt in range(1, MAX_RETRY + 1):
        print(f"[{attempt}/{MAX_RETRY}] Fetch XSMB {today} ...")
        res = lot.fetch(today)
        if res is not None:
            fetched_today = True
            print("✅ Có kết quả hôm nay")
            break
        if attempt < MAX_RETRY:
            print("⏳ Chưa có kết quả, chờ 60s thử lại...")
            time.sleep(SLEEP_SEC)

    lot.generate_dataframes()
    if lot.get_raw_data().empty:
        write_site_meta("Chưa có dữ liệu")
        print("❌ No data")
        return

    # lưu data
    lot.save_json("data/xsmb.json")
    lot.dump()

    # charts + stats (top10)
    stats = render_images(lot.get_raw_data(), lot.get_2_digits_data())

    # top10 dạng text
    write_json("data/top10_delta.json", stats.get("top10_delta", []))
    write_json("data/top10_30d.json", stats.get("top10_30d", []))

    # last 7 ngày full giải (cho web)
    write_json("data/last7.json", make_last7(lot.get_raw_data()))

    # meta: note để web bật LED warn
    if fetched_today:
        write_site_meta("Đã cập nhật kết quả hôm nay")
    else:
        write_site_meta("Chưa có kết quả hôm nay…")

    print("✅ DONE")


if __name__ == "__main__":
    main()
