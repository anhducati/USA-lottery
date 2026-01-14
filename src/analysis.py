from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _ensure_images():
    Path("images").mkdir(parents=True, exist_ok=True)


def loto_delta(two_df: pd.DataFrame) -> pd.DataFrame:
    df = two_df.copy().sort_values("date").reset_index(drop=True)
    last_date = df["date"].max().date()

    last_seen: dict[int, pd.Timestamp | None] = {i: None for i in range(100)}
    for _, row in df.iterrows():
        d = row["date"].date()
        vals = row.iloc[1:].astype(int).tolist()
        for v in vals:
            last_seen[int(v)] = pd.Timestamp(d)

    out = []
    for k, v in last_seen.items():
        if v is None:
            continue
        out.append({"num": int(k), "delta": int((pd.Timestamp(last_date) - v).days)})
    return pd.DataFrame(out).sort_values("delta", ascending=False).reset_index(drop=True)


def loto_one_year_counts(two_df: pd.DataFrame) -> pd.Series:
    df = two_df.copy().sort_values("date").reset_index(drop=True)
    last_date = df["date"].max().date()
    begin = last_date - timedelta(days=365)

    df = df[df["date"].dt.date >= begin]
    values = df.iloc[:, 1:].to_numpy().reshape(-1)
    return pd.Series(values).value_counts().reindex(range(100), fill_value=0).sort_index()


def loto_30d_daily_counts(two_df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    df = two_df.copy().sort_values("date").reset_index(drop=True)
    last_dt = df["date"].max()
    begin_dt = last_dt - pd.Timedelta(days=days - 1)

    df = df[df["date"] >= begin_dt].copy()
    df["daily_total_hits"] = df.iloc[:, 1:].count(axis=1).astype(int)
    df["daily_unique_hits"] = df.iloc[:, 1:].apply(lambda r: len(set(map(int, r.values))), axis=1).astype(int)
    return df[["date", "daily_total_hits", "daily_unique_hits"]]


def loto_30d_top10(two_df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    df = two_df.copy().sort_values("date").reset_index(drop=True)
    last_date = df["date"].max()
    begin = last_date - pd.Timedelta(days=days)
    df = df[df["date"] > begin]

    values = df.iloc[:, 1:].to_numpy().reshape(-1)
    vc = pd.Series(values).value_counts().head(10)
    out = pd.DataFrame({"num": vc.index.astype(int), "count": vc.values.astype(int)})
    return out.sort_values("count", ascending=False).reset_index(drop=True)


def render_images(raw_df: pd.DataFrame, two_df: pd.DataFrame) -> dict:
    _ensure_images()

    ddf = loto_delta(two_df)

    plt.figure()
    plt.bar(ddf["num"].astype(str), ddf["delta"])
    plt.xticks(rotation=90, fontsize=6)
    plt.title("Loto - Days since last appearing")
    plt.tight_layout()
    plt.savefig("images/delta.jpg", dpi=200)
    plt.close()

    dtop10 = ddf.head(10)
    plt.figure()
    plt.bar(dtop10["num"].astype(str), dtop10["delta"])
    plt.title("Top 10 loto - Days since last appearing")
    plt.tight_layout()
    plt.savefig("images/delta_top_10.jpg", dpi=200)
    plt.close()

    counts = loto_one_year_counts(two_df)
    stats = {
        "max": int(counts.max()),
        "min": int(counts.min()),
        "mean": float(counts.mean()),
        "std": float(counts.std(ddof=0)),
    }

    grid = counts.values.reshape(10, 10)
    plt.figure()
    sns.heatmap(grid, annot=False)
    plt.title("One-year loto counts heatmap (00-99)")
    plt.tight_layout()
    plt.savefig("images/heatmap.jpg", dpi=200)
    plt.close()

    top10c = counts.sort_values(ascending=False).head(10)
    plt.figure()
    plt.bar(top10c.index.astype(str), top10c.values)
    plt.title("Top 10 loto (last 1 year)")
    plt.tight_layout()
    plt.savefig("images/top-10.jpg", dpi=200)
    plt.close()

    plt.figure()
    plt.hist(counts.values, bins=20)
    plt.title("Distribution of loto counts (last 1 year)")
    plt.tight_layout()
    plt.savefig("images/distribution.jpg", dpi=200)
    plt.close()

    df30 = loto_30d_daily_counts(two_df, days=30)

    plt.figure()
    plt.plot(df30["date"], df30["daily_total_hits"])
    plt.xticks(rotation=45, fontsize=7)
    plt.title("Last 30 days - Total loto hits per day")
    plt.tight_layout()
    plt.savefig("images/line_30d_total.jpg", dpi=200)
    plt.close()

    plt.figure()
    plt.plot(df30["date"], df30["daily_unique_hits"])
    plt.xticks(rotation=45, fontsize=7)
    plt.title("Last 30 days - Unique loto numbers per day")
    plt.tight_layout()
    plt.savefig("images/line_30d_unique.jpg", dpi=200)
    plt.close()

    top10_30 = loto_30d_top10(two_df, days=30)
    plt.figure()
    plt.bar(top10_30["num"].astype(str), top10_30["count"])
    plt.title("Top 10 loto by frequency (last 30 days)")
    plt.tight_layout()
    plt.savefig("images/top10_30d.jpg", dpi=200)
    plt.close()

    stats["last30_summary"] = {
        "total_hits_mean": float(df30["daily_total_hits"].mean()),
        "unique_hits_mean": float(df30["daily_unique_hits"].mean()),
    }

    stats["top10_delta"] = dtop10.to_dict(orient="records")  # [{num, delta}]
    stats["top10_30d"] = top10_30.to_dict(orient="records")  # [{num, count}]
    return stats
