#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.24", "pandas>=2.0", "requests>=2.28"]
# ///
"""Forecast verification for Madeira: compare raw NWP models on daily
temperature and precipitation against a WMO station on the island.

Forecasts:    Open-Meteo Previous Runs API (archived lead-time offsets).
              `<var>_previous_dayN` is what the model predicted N*24 h before
              the valid time, i.e. a lead of N days. Hourly precipitation is
              the sum over the preceding hour.
Observations: NOAA/NCEI Integrated Surface Database (ISD), one CSV per
              station-year, fed by the WMO SYNOP/METAR stream from IPMA.
              Temperature comes from the hourly reports; precipitation from the
              SYNOP accumulation groups (1/3/6/12/24 h), tiled exactly onto
              06Z-06Z days so forecast and observation cover the same window.
              Station metadata (name, coordinates, elevation) is read from the
              ISD file itself and the forecast point is placed on the station.

Stations (--station, ISD id = WMO index + "0" + "99999"):
  08522099999  Funchal (city observatory, ~32.63N 16.90W, 58 m)   [default]
  08521099999  the other Funchal entry, believed to be the airport (LPMA)
  The script prints the station name/coordinates it actually got, so an
  unexpected mapping is visible immediately.

Usage:
    uv run wxverif_madeira.py                        # fetch (cached) + report
    uv run wxverif_madeira.py --station 08521099999
    uv run wxverif_madeira.py --season 10-01:11-15   # default window, every year
    uv run wxverif_madeira.py --models ecmwf_ifs025,ecmwf_aifs025_single
    uv run wxverif_madeira.py --selftest             # synthetic data, no network
"""

import argparse
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------- configuration

STATION = "08522099999"
TZ = "Atlantic/Madeira"            # local calendar days for temperature
START = "2024-01-01"               # Open-Meteo previous-runs archive start
SEASON = "10-01:11-15"             # MM-DD:MM-DD window, applied to every year

# Probed in this order; anything that errors or returns no data for the site
# is dropped (regional models that do not cover Madeira, unknown ids, ...).
CANDIDATE_MODELS = [
    "ecmwf_ifs025",                # ECMWF IFS 0.25 deg open data
    "ecmwf_aifs025_single",        # ECMWF AIFS (machine-learned), 0.25 deg
    "gfs_seamless",                # NOAA GFS
    "ncep_aigfs025",               # NOAA AIGFS (machine-learned), if archived
    "icon_seamless",               # DWD ICON-EU (7 km) over Madeira, else global
    "meteofrance_seamless",        # Meteo-France ARPEGE Europe (0.1 deg)
    "ukmo_seamless",               # UK Met Office global 10 km
    "gem_seamless",                # Environment Canada GEM global
    "jma_seamless",                # JMA GSM
    "kma_seamless",                # KMA GDPS
    "knmi_harmonie_arome_europe",  # probably out of domain -> dropped
    "dmi_harmonie_arome_europe",   # probably out of domain -> dropped
    "best_match",                  # Open-Meteo's own pick for the location
]
LEADS = range(1, 6)
RAIN_THRESHOLDS_MM = [0.1, 1.0, 5.0]   # daily totals
MIN_HOURS_PER_DAY = 22                 # completeness required to score a day
PRECIP_DAY_START_UTC = 6               # WMO climatological day: 06Z -> 06Z
MIN_FRAC = 0.8                         # model must cover this share of dates
N_BOOT = 2000
BAD_QC = {"2", "3", "6", "7"}          # ISD quality codes: suspect/erroneous

FORECAST_API = "https://previous-runs-api.open-meteo.com/v1/forecast"
ISD_URL = "https://www.ncei.noaa.gov/data/global-hourly/access/{year}/{station}.csv"

CACHE = Path("cache")
OUT = Path("out")


# ------------------------------------------------------------------- fetching

def _get(url, params=None, retries=5, ok_statuses=()):
    import requests
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=180,
                             headers={"User-Agent": "wxverif-madeira/1.0"})
        except requests.RequestException as e:   # transient network trouble
            last = e
            time.sleep(5 * (attempt + 1))
            continue
        if r.status_code in ok_statuses:
            return r
        if r.status_code == 429 or r.status_code >= 500:
            last = f"HTTP {r.status_code}"
            time.sleep(10 * (attempt + 1))
            continue
        r.raise_for_status()
        return r
    raise RuntimeError(f"gave up on {url}: {last}")


def _reason(r):
    try:
        return r.json().get("reason", f"HTTP {r.status_code}")
    except ValueError:
        return f"HTTP {r.status_code}"


def _date_chunks(start, end, months=4):
    edges = pd.date_range(start, end, freq=f"{months}MS").tolist()
    points = sorted({pd.Timestamp(start), *edges, pd.Timestamp(end)})
    for a, b in zip(points, points[1:]):
        yield a.date().isoformat(), b.date().isoformat()


def _fc_params(site, a, b, hourly, model):
    params = {
        "latitude": site["lat"], "longitude": site["lon"],
        "start_date": a, "end_date": b,
        "hourly": hourly, "models": model, "timezone": "UTC",
    }
    if site.get("elev") is not None and np.isfinite(site["elev"]):
        params["elevation"] = site["elev"]   # downscale to the station height
    return params


def probe_models(candidates, site, end):
    """Keep the candidates that return data for this site in the last days."""
    a = (pd.Timestamp(end) - pd.Timedelta(days=3)).date().isoformat()
    keep = []
    for m in candidates:
        r = _get(FORECAST_API, _fc_params(
            site, a, end, "temperature_2m_previous_day1", m), ok_statuses=(400,))
        if r.status_code == 400:
            print(f"  skip {m}: {_reason(r)}")
            continue
        vals = r.json()["hourly"]["temperature_2m_previous_day1"]
        if all(v is None for v in vals):
            print(f"  skip {m}: no data at this location")
            continue
        print(f"  ok   {m}")
        keep.append(m)
        time.sleep(0.3)
    return keep


def fetch_forecasts(models, site, start, end):
    """One request per model per ~6-month chunk. Returns long-format frame:
    columns time (UTC), model, lead, t2m, precip."""
    frames = []
    hourly = ",".join(f"{v}_previous_day{d}"
                      for v in ("temperature_2m", "precipitation") for d in LEADS)
    for model in models:
        cache_file = CACHE / f"fc_{model}_{site['station']}_{start}_{end}.csv.gz"
        if cache_file.exists():
            df = pd.read_csv(cache_file)
            df["time"] = pd.to_datetime(df["time"], utc=True)
            frames.append(df)
            continue
        parts = []
        for a, b in _date_chunks(start, end):
            print(f"  {model} {a}..{b}")
            r = _get(FORECAST_API, _fc_params(site, a, b, hourly, model),
                     ok_statuses=(400,))
            if r.status_code == 400:
                print(f"    {_reason(r)} -> chunk skipped")
                continue
            h = r.json()["hourly"]
            t = pd.to_datetime(h["time"], utc=True)
            for d in LEADS:
                parts.append(pd.DataFrame({
                    "time": t, "model": model, "lead": d,
                    "t2m": h.get(f"temperature_2m_previous_day{d}"),
                    "precip": h.get(f"precipitation_previous_day{d}"),
                }))
            time.sleep(1.0)
        if not parts:
            print(f"  {model}: nothing returned, dropped")
            continue
        df = pd.concat(parts, ignore_index=True)
        df = df.dropna(subset=["t2m", "precip"], how="all")
        df.to_csv(cache_file, index=False)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def fetch_isd_raw(station, start, end):
    """Download (cached) the ISD station-year CSVs covering start..end."""
    this_year = pd.Timestamp.now(tz="UTC").year
    frames = []
    for year in range(int(start[:4]), int(end[:4]) + 1):
        f = CACHE / f"isd_{station}_{year}.csv"
        stale = (f.exists() and year == this_year
                 and time.time() - f.stat().st_mtime > 86400)
        if not f.exists() or stale:
            print(f"  obs {station} {year}")
            r = _get(ISD_URL.format(year=year, station=station), ok_statuses=(404,))
            if r.status_code == 404:
                print(f"    no ISD file for {station} in {year}")
                continue
            f.write_bytes(r.content)
        frames.append(pd.read_csv(f, dtype=str, low_memory=False))
    if not frames:
        raise RuntimeError(f"no ISD data at all for station {station}; "
                           "check the id (WMO index + '0' + '99999')")
    return pd.concat(frames, ignore_index=True)


def station_metadata(raw):
    last = raw.dropna(subset=["LATITUDE", "LONGITUDE"]).iloc[-1]
    return dict(
        name=str(last.get("NAME", "?")).strip(),
        call_sign=str(last.get("CALL_SIGN", "")).strip(),
        lat=float(last["LATITUDE"]), lon=float(last["LONGITUDE"]),
        elev=float(last.get("ELEVATION", "nan")),
    )


# ------------------------------------------------------------ ISD parsing

def parse_isd(raw, start, end):
    """Returns (hourly temperature frame, precipitation reports, info dict).

    hourly:  time (UTC, on the hour), t2m_obs
    reports: end (UTC), period_h, mm   -- one row per accumulation report
    """
    t = pd.to_datetime(raw["DATE"], utc=True, errors="coerce",
                       format="%Y-%m-%dT%H:%M:%S")
    lo = pd.Timestamp(start, tz="UTC")
    hi = pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=2)
    in_range = (t >= lo) & (t <= hi)
    raw, t = raw[in_range].reset_index(drop=True), t[in_range].reset_index(drop=True)

    # --- temperature: "+0217,1" -> 21.7 degC, quality 1
    tmp = raw["TMP"].fillna("+9999,9").str.split(",", expand=True)
    val = pd.to_numeric(tmp[0], errors="coerce") / 10.0
    val[(tmp[0] == "+9999") | tmp[1].isin(BAD_QC)] = np.nan
    rtype = raw["REPORT_TYPE"].fillna("") if "REPORT_TYPE" in raw else \
        pd.Series("", index=raw.index)
    prio = rtype.map({"FM-12": 0, "SY-MT": 1, "SY-SY": 1}).fillna(2)  # SYNOP first
    rounded = t.dt.round("h")
    off = (t - rounded).abs()
    hourly = pd.DataFrame({"time": rounded, "t2m_obs": val, "prio": prio, "off": off})
    hourly = hourly[hourly["off"] <= pd.Timedelta(minutes=15)].dropna(subset=["t2m_obs"])
    hourly = (hourly.sort_values(["time", "prio", "off"])
              .drop_duplicates("time")[["time", "t2m_obs"]]
              .reset_index(drop=True))

    # --- precipitation: AA1..AA4 = "period_h,depth_tenths_mm,condition,quality"
    rows = []
    for col in [c for c in raw.columns if re.fullmatch(r"AA\d", c)]:
        parts = raw[col].fillna("99,9999,9,9").str.split(",", expand=True)
        if parts.shape[1] < 4:
            continue
        period = pd.to_numeric(parts[0], errors="coerce")
        depth = pd.to_numeric(parts[1], errors="coerce")
        ok = period.between(1, 48) & depth.between(0, 9998) & ~parts[3].isin(BAD_QC)
        rows.append(pd.DataFrame({"end": rounded[ok], "period_h": period[ok].astype(int),
                                  "mm": depth[ok] / 10.0}))
    reports = (pd.concat(rows, ignore_index=True) if rows
               else pd.DataFrame(columns=["end", "period_h", "mm"]))
    reports = (reports.sort_values(["end", "period_h", "mm"], ascending=[True, True, False])
               .drop_duplicates(["end", "period_h"]).reset_index(drop=True))

    hours_per_day = hourly.groupby(hourly["time"].dt.floor("D")).size()
    info = dict(
        rows=len(raw), temp_hours=len(hourly),
        median_hours_per_day=float(hours_per_day.median()) if len(hours_per_day) else 0.0,
        report_types=rtype.value_counts().head(6).to_dict(),
        precip_reports_by_period=reports["period_h"].value_counts().sort_index().to_dict(),
    )
    return hourly, reports, info


# ------------------------------------------------------------------ pipeline

def tile_windows(reports, start_hour=PRECIP_DAY_START_UTC):
    """Assemble daily totals from accumulation reports that exactly tile each
    24 h window starting at start_hour UTC (longest report first, no gaps,
    no overlaps). Days that cannot be tiled are dropped, not approximated.
    Returns date (UTC date of the window start), rr_obs, n_pieces."""
    if reports.empty:
        return pd.DataFrame(columns=["date", "rr_obs", "n_pieces"])
    rep = reports.copy()
    rep["start"] = rep["end"] - pd.to_timedelta(rep["period_h"], unit="h")
    by_start = {}
    for r in rep.itertuples(index=False):
        by_start.setdefault(r.start, []).append((int(r.period_h), float(r.mm)))
    rows = []
    days = pd.date_range(rep["end"].min().floor("D") - pd.Timedelta(days=1),
                         rep["end"].max().floor("D"), freq="D")
    for d in days:
        t0 = d + pd.Timedelta(hours=start_hour)
        t1 = t0 + pd.Timedelta(hours=24)
        t, total, pieces = t0, 0.0, 0
        while t < t1:
            opts = [(p, mm) for p, mm in by_start.get(t, [])
                    if t + pd.Timedelta(hours=p) <= t1]
            if not opts:
                break
            p, mm = max(opts)
            total += mm
            t += pd.Timedelta(hours=p)
            pieces += 1
        if t == t1:
            rows.append(dict(date=t0.date(), rr_obs=round(total, 2), n_pieces=pieces))
    return pd.DataFrame(rows, columns=["date", "rr_obs", "n_pieces"])


def make_daily_temp(fc, hourly):
    """Pair hourly forecast/obs temperature, aggregate to local calendar days.
    Daily min/max are derived from hourly values on both sides so forecasts
    and observations are aggregated identically."""
    df = fc.merge(hourly, on="time", how="inner").dropna(subset=["t2m", "t2m_obs"])
    df["date"] = df["time"].dt.tz_convert(TZ).dt.date
    daily = df.groupby(["date", "model", "lead"]).agg(
        n_hours=("t2m", "size"),
        tmin=("t2m", "min"), tmax=("t2m", "max"),
        tmin_obs=("t2m_obs", "min"), tmax_obs=("t2m_obs", "max"),
    ).reset_index()
    return daily[daily["n_hours"] >= MIN_HOURS_PER_DAY].drop(columns="n_hours")


def make_daily_precip(fc, reports):
    """Forecast totals over the same 06Z-06Z windows as the tiled observations.
    A forecast hour stamped T covers (T-1h, T], so the window (t0, t0+24h]
    is the 24 stamps t0+1h .. t0+24h."""
    obs_days = tile_windows(reports)
    f = fc.dropna(subset=["precip"]).copy()
    shift = pd.Timedelta(hours=PRECIP_DAY_START_UTC + 1)
    f["date"] = (f["time"] - shift).dt.floor("D").dt.date
    g = f.groupby(["date", "model", "lead"]).agg(
        n=("precip", "size"), rr=("precip", "sum")).reset_index()
    g = g[g["n"] == 24].drop(columns="n")
    return g.merge(obs_days, on="date", how="inner")


def complete_cases(daily, lead, min_frac=MIN_FRAC):
    """For one lead: drop models covering < min_frac of the dates (so a sparse
    model cannot shrink everyone's sample), then keep only dates present for
    every remaining model. Returns (frame, models, dropped coverage)."""
    d = daily[daily["lead"] == lead]
    n_dates = d["date"].nunique()
    if n_dates == 0:
        return d, [], pd.Series(dtype=float)
    cov = d.groupby("model")["date"].nunique() / n_dates
    keep = sorted(cov[cov >= min_frac].index)
    dropped = cov[cov < min_frac]
    d = d[d["model"].isin(keep)]
    counts = d.groupby("date")["model"].nunique()
    dates = counts[counts == len(keep)].index
    return d[d["date"].isin(dates)], keep, dropped


def contingency(fc_rr, obs_rr, thr):
    f, o = fc_rr >= thr, obs_rr >= thr
    a = int((f & o).sum());  b = int((f & ~o).sum())
    c = int((~f & o).sum()); d = int((~f & ~o).sum())
    n = a + b + c + d
    a_rand = (a + b) * (a + c) / n if n else np.nan
    pod = a / (a + c) if a + c else np.nan
    far = b / (a + b) if a + b else np.nan
    csi = a / (a + b + c) if a + b + c else np.nan
    ets = ((a - a_rand) / (a + b + c - a_rand)
           if (a + b + c - a_rand) else np.nan)
    return dict(hits=a, false_alarms=b, misses=c, correct_neg=d,
                pod=pod, far=far, csi=csi, ets=ets)


def summarize(daily_t, daily_p, min_frac=MIN_FRAC):
    temp_rows, precip_rows, dropped = [], [], []
    for lead in sorted(daily_t["lead"].unique()):
        d, models, drp = complete_cases(daily_t, lead, min_frac)
        dropped += [dict(table="temperature", lead=lead, model=m, coverage=round(c, 2))
                    for m, c in drp.items()]
        for m in models:
            s = d[d["model"] == m]
            e_min, e_max = s["tmin"] - s["tmin_obs"], s["tmax"] - s["tmax_obs"]
            temp_rows.append(dict(
                model=m, lead=lead, n_days=len(s),
                mae_tmin=e_min.abs().mean(), bias_tmin=e_min.mean(),
                mae_tmax=e_max.abs().mean(), bias_tmax=e_max.mean(),
            ))
    for lead in sorted(daily_p["lead"].unique()):
        d, models, drp = complete_cases(daily_p, lead, min_frac)
        dropped += [dict(table="precipitation", lead=lead, model=m, coverage=round(c, 2))
                    for m, c in drp.items()]
        for m in models:
            s = d[d["model"] == m]
            for thr in RAIN_THRESHOLDS_MM:
                precip_rows.append(dict(
                    model=m, lead=lead, threshold_mm=thr, n_days=len(s),
                    wet_days_obs=int((s["rr_obs"] >= thr).sum()),
                    mae_rr=(s["rr"] - s["rr_obs"]).abs().mean(),
                    bias_rr=(s["rr"] - s["rr_obs"]).mean(),
                    **contingency(s["rr"].to_numpy(), s["rr_obs"].to_numpy(), thr)))
    return (pd.DataFrame(temp_rows), pd.DataFrame(precip_rows),
            pd.DataFrame(dropped, columns=["table", "lead", "model", "coverage"]))


def _abs_error_matrix(d, var):
    return (d.pivot_table(index="date", columns="model", values=var)
            .sub(d.pivot_table(index="date", columns="model", values=f"{var}_obs"),
                 axis=0).abs().dropna())


def rank_vs_best(daily, var, n_boot=N_BOOT, min_frac=MIN_FRAC, seed=0):
    """Per lead: MAE of every model and a paired bootstrap of its MAE minus the
    best model's MAE on the same dates. worse_than_best: 95% CI excludes 0."""
    rng = np.random.default_rng(seed)
    rows = []
    for lead in sorted(daily["lead"].unique()):
        d, models, _ = complete_cases(daily, lead, min_frac)
        if len(models) < 2 or d.empty:
            continue
        err = _abs_error_matrix(d, var)
        if len(err) < 5:
            continue
        mae = err.mean()
        best = mae.idxmin()
        idx = rng.integers(0, len(err), size=(n_boot, len(err)))
        for m in mae.sort_values().index:
            diff = (err[m] - err[best]).to_numpy()
            boots = diff[idx].mean(axis=1)
            lo, hi = np.percentile(boots, [2.5, 97.5])
            rows.append(dict(lead=lead, model=m, n=len(err), mae=mae[m],
                             diff_vs_best=diff.mean(), ci_lo=lo, ci_hi=hi,
                             worse_than_best=bool(m != best and lo > 0)))
    return pd.DataFrame(rows)


def bootstrap_pairs(daily, var="tmax", n_boot=N_BOOT, min_frac=MIN_FRAC, seed=0):
    """Paired bootstrap of MAE differences on shared dates, all model pairs.
    diff < 0 means model_a beats model_b; significant if CI excludes 0."""
    rng = np.random.default_rng(seed)
    rows = []
    for lead in sorted(daily["lead"].unique()):
        d, models, _ = complete_cases(daily, lead, min_frac)
        if len(models) < 2 or d.empty:
            continue
        err = _abs_error_matrix(d, var)
        if len(err) < 5:
            continue
        idx = rng.integers(0, len(err), size=(n_boot, len(err)))
        for i, a in enumerate(models):
            for b in models[i + 1:]:
                diff = (err[a] - err[b]).to_numpy()
                boots = diff[idx].mean(axis=1)
                lo, hi = np.percentile(boots, [2.5, 97.5])
                rows.append(dict(lead=lead, model_a=a, model_b=b, n=len(err),
                                 mae_diff=diff.mean(), ci_lo=lo, ci_hi=hi,
                                 significant=bool(lo > 0 or hi < 0)))
    return pd.DataFrame(rows)


# -------------------------------------------------------------- reporting

def parse_season(spec):
    a, b = spec.split(":")
    m0, d0 = (int(x) for x in a.split("-"))
    m1, d1 = (int(x) for x in b.split("-"))
    return (m0, d0), (m1, d1)


def in_season(dates, spec):
    """Boolean mask for month-day window spec 'MM-DD:MM-DD' (may wrap the year)."""
    (m0, d0), (m1, d1) = parse_season(spec)
    md = pd.Series([(x.month, x.day) for x in dates], index=dates.index)
    lo, hi = (m0, d0), (m1, d1)
    if lo <= hi:
        return (md >= lo) & (md <= hi)
    return (md >= lo) | (md <= hi)


class Log:
    def __init__(self, path):
        self.f = open(path, "w", encoding="utf-8")

    def __call__(self, *parts):
        s = " ".join(str(p) for p in parts)
        print(s)
        self.f.write(s + "\n")

    def close(self):
        self.f.close()


def report(daily_t, daily_p, label, tag, n_boot, min_frac, log):
    log(f"\n{'=' * 78}\n{label}\n{'=' * 78}")
    temp, precip, dropped = summarize(daily_t, daily_p, min_frac)
    temp.to_csv(OUT / f"summary_temperature_{tag}.csv", index=False)
    precip.to_csv(OUT / f"summary_precip_{tag}.csv", index=False)
    if not dropped.empty:
        log("\nmodels excluded from the shared sample (coverage below "
            f"{min_frac:.0%} of dates):")
        log(dropped.to_string(index=False))

    if temp.empty:
        log("\n(no temperature days to score)")
    else:
        log("\n-- Temperature: daily Tmin/Tmax vs station, degC "
            "(MAE, bias = forecast - obs) --")
        log(temp.round(2).to_string(index=False))
        for var, name in (("tmax", "Tmax"), ("tmin", "Tmin")):
            rk = rank_vs_best(daily_t, var, n_boot, min_frac)
            rk.to_csv(OUT / f"rank_{var}_{tag}.csv", index=False)
            bootstrap_pairs(daily_t, var, n_boot, min_frac).to_csv(
                OUT / f"bootstrap_pairs_{var}_{tag}.csv", index=False)
            if not rk.empty:
                log(f"\n-- {name} MAE ranking per lead; diff_vs_best with 95% paired-"
                    "bootstrap CI; worse_than_best=True means the gap to the best "
                    "model is significant --")
                log(rk.round(2).to_string(index=False))

    if precip.empty:
        log("\n(no precipitation days to score)")
    else:
        log("\n-- Precipitation: 06Z-06Z daily totals vs station, mm "
            "(POD hit rate, FAR false-alarm ratio, CSI, ETS skill vs chance) --")
        log(precip.round(2).to_string(index=False))
        rk = rank_vs_best(daily_p, "rr", n_boot, min_frac)
        rk.to_csv(OUT / f"rank_rr_{tag}.csv", index=False)
        bootstrap_pairs(daily_p, "rr", n_boot, min_frac).to_csv(
            OUT / f"bootstrap_pairs_rr_{tag}.csv", index=False)
        if not rk.empty:
            log("\n-- Daily rainfall amount MAE ranking per lead (same bootstrap) --")
            log(rk.round(2).to_string(index=False))


# ------------------------------------------------------------------ selftest

def _selftest_isd_parsing():
    csv = (
        "STATION,DATE,SOURCE,LATITUDE,LONGITUDE,ELEVATION,NAME,REPORT_TYPE,"
        "CALL_SIGN,QUALITY_CONTROL,TMP,AA1,AA2\n"
        "08522099999,2025-10-01T06:00:00,4,32.63,-16.9,58,FUNCHAL,FM-12,,V020,"
        "\"+0183,1\",\"24,0052,9,1\",\"12,0030,9,1\"\n"
        "08522099999,2025-10-01T06:00:00,4,32.63,-16.9,58,FUNCHAL,FM-15,LPMA,V020,"
        "\"+0180,1\",,\n"
        "08522099999,2025-10-01T06:30:00,4,32.63,-16.9,58,FUNCHAL,FM-15,LPMA,V020,"
        "\"+0190,1\",,\n"
        "08522099999,2025-10-01T07:00:00,4,32.63,-16.9,58,FUNCHAL,FM-12,,V020,"
        "\"+9999,9\",\"99,9999,9,9\",\n"
        "08522099999,2025-10-01T08:00:00,4,32.63,-16.9,58,FUNCHAL,FM-12,,V020,"
        "\"+0201,3\",\"06,0000,9,1\",\n"
    )
    import io
    raw = pd.read_csv(io.StringIO(csv), dtype=str)
    hourly, reports, info = parse_isd(raw, "2025-10-01", "2025-10-02")
    assert len(hourly) == 1 and abs(hourly["t2m_obs"].iloc[0] - 18.3) < 1e-9, \
        "SYNOP row should win over METAR at 06Z; 07Z missing; 08Z QC=3 dropped"
    assert sorted(reports["period_h"].tolist()) == [6, 12, 24], reports
    meta = station_metadata(raw)
    assert meta["name"] == "FUNCHAL" and abs(meta["lat"] - 32.63) < 1e-9


def _selftest_tiling():
    def rep(end, period, mm):
        return dict(end=pd.Timestamp(end, tz="UTC"), period_h=period, mm=mm)
    reports = pd.DataFrame([
        rep("2025-10-02 06:00", 24, 5.0),                       # day 1: one 24h
        rep("2025-10-02 18:00", 12, 1.0), rep("2025-10-03 06:00", 12, 2.5),  # day 2
        rep("2025-10-03 12:00", 6, 0.1), rep("2025-10-03 18:00", 6, 0.0),
        rep("2025-10-04 00:00", 6, 3.0), rep("2025-10-04 06:00", 6, 0.4),  # day 3
        rep("2025-10-04 18:00", 12, 9.0),                       # day 4: gap -> drop
        rep("2025-10-05 06:00", 24, 7.0), rep("2025-10-05 06:00", 12, 4.0),  # day 4 also
    ])
    days = tile_windows(reports)
    got = {str(r.date): (r.rr_obs, r.n_pieces) for r in days.itertuples()}
    assert got["2025-10-01"] == (5.0, 1), got
    assert got["2025-10-02"] == (3.5, 2), got
    assert got["2025-10-03"] == (3.5, 4), got
    assert got["2025-10-04"] == (7.0, 1), "24h report must win over 12h+gap"
    assert len(got) == 4, got


def selftest():
    """Synthetic data with known error structure through the full pipeline."""
    _selftest_isd_parsing()
    _selftest_tiling()

    rng = np.random.default_rng(42)
    hours = pd.date_range("2024-01-01", periods=24 * 400, freq="h", tz="UTC")
    t_true = 18 + 4 * np.sin(2 * np.pi * hours.dayofyear / 365) \
        + 3 * np.sin(2 * np.pi * hours.hour / 24)
    wet = rng.random(len(hours)) < 0.10
    rr_true = np.where(wet, rng.gamma(1.2, 1.5, len(hours)), 0.0)
    hourly = pd.DataFrame({"time": hours, "t2m_obs": t_true})
    # station reports 12 h totals at 06Z and 18Z
    obs = pd.DataFrame({"time": hours, "rr": rr_true})
    obs["end"] = (obs["time"] - pd.Timedelta(hours=7)).dt.floor("12h") \
        + pd.Timedelta(hours=18)
    reports = obs.groupby("end")["rr"].sum().reset_index()
    reports["period_h"] = 12
    reports = reports.rename(columns={"rr": "mm"})

    sigma = {"good_model": 1.0, "bad_model": 1.8}
    parts = []
    for model, s in sigma.items():
        for lead in (1, 2):
            noise = rng.normal(0, s * lead, len(hours))
            flip = rng.random(len(hours)) < 0.05 * s
            parts.append(pd.DataFrame({
                "time": hours, "model": model, "lead": lead,
                "t2m": t_true + noise,
                "precip": np.where(flip, np.where(wet, 0.0, 1.0), rr_true),
            }))
    fc = pd.concat(parts, ignore_index=True)
    daily_t = make_daily_temp(fc, hourly)
    daily_p = make_daily_precip(fc, reports)
    assert len(daily_p) > 300 and daily_p["n_pieces"].eq(2).all(), \
        "12h reports should tile in pairs"

    temp, precip, dropped = summarize(daily_t, daily_p)
    assert dropped.empty
    t = temp.pivot_table(index="lead", columns="model", values="mae_tmax")
    assert (t["good_model"] < t["bad_model"]).all(), "MAE ordering wrong"
    assert (t.loc[2] > t.loc[1]).all(), "MAE should grow with lead"
    assert precip["ets"].between(-0.34, 1).all(), "ETS out of range"
    p = precip[precip["threshold_mm"] == 0.1].pivot_table(
        index="lead", columns="model", values="ets")
    assert (p["good_model"] > p["bad_model"]).all(), "ETS ordering wrong"
    rk = rank_vs_best(daily_t, "tmax", n_boot=300)
    assert rk[rk["model"] == "bad_model"]["worse_than_best"].all(), \
        "known 1.0-vs-1.8 sigma gap should be significant"
    assert in_season(pd.Series([pd.Timestamp("2025-10-20").date()]), "10-01:11-15").all()
    assert not in_season(pd.Series([pd.Timestamp("2025-09-30").date()]), "10-01:11-15").all()
    assert in_season(pd.Series([pd.Timestamp("2025-01-10").date()]), "12-01:02-28").all()
    print(temp.round(2).to_string(index=False))
    print("selftest PASS")


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--station", default=STATION, help="ISD station id")
    ap.add_argument("--lat", type=float, help="override forecast point latitude")
    ap.add_argument("--lon", type=float, help="override forecast point longitude")
    ap.add_argument("--elev", type=float, help="override forecast point elevation (m)")
    ap.add_argument("--start", default=START)
    ap.add_argument("--end", default=None, help="default: yesterday")
    ap.add_argument("--season", default=SEASON, help="MM-DD:MM-DD, every year")
    ap.add_argument("--models", default=None,
                    help="comma-separated Open-Meteo model ids (default: probe list)")
    ap.add_argument("--min-frac", type=float, default=MIN_FRAC)
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    end = args.end or (pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=1)).date().isoformat()
    CACHE.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    log = Log(OUT / "summary.txt")

    print("fetching observations")
    raw = fetch_isd_raw(args.station, args.start, end)
    meta = station_metadata(raw)
    site = dict(station=args.station,
                lat=args.lat if args.lat is not None else meta["lat"],
                lon=args.lon if args.lon is not None else meta["lon"],
                elev=args.elev if args.elev is not None else meta["elev"])
    hourly, reports, info = parse_isd(raw, args.start, end)
    daily_obs = tile_windows(reports)

    log(f"station {args.station}: {meta['name']} {meta['call_sign']} "
        f"lat {meta['lat']:.3f} lon {meta['lon']:.3f} elev {meta['elev']:.0f} m")
    log(f"forecast point: lat {site['lat']:.3f} lon {site['lon']:.3f} "
        f"elev {site['elev']:.0f} m; period {args.start}..{end}; season {args.season}")
    log(f"obs rows {info['rows']}, report types {info['report_types']}")
    log(f"hourly temperatures {info['temp_hours']} "
        f"(median {info['median_hours_per_day']:.0f} per day; "
        f"{MIN_HOURS_PER_DAY} needed to score a day)")
    log(f"precip reports by accumulation period (h): {info['precip_reports_by_period']}; "
        f"tiled 06Z-06Z days: {len(daily_obs)}")
    if info["median_hours_per_day"] < MIN_HOURS_PER_DAY:
        log("WARNING: station reports too sparsely for daily Tmin/Tmax from hourly "
            "values; try the other Funchal station id")
    if len(daily_obs) < 60:
        log("WARNING: few tileable precipitation days; check the accumulation "
            "periods above, or try the other station id")

    print("probing models")
    models = (args.models.split(",") if args.models
              else probe_models(CANDIDATE_MODELS, site, end))
    if not models:
        sys.exit("no model returned data for this site")
    print("fetching forecasts")
    fc = fetch_forecasts(models, site, args.start, end)

    daily_t = make_daily_temp(fc, hourly)
    daily_p = make_daily_precip(fc, reports)
    daily_t.to_csv(OUT / "paired_daily_temperature.csv", index=False)
    daily_p.to_csv(OUT / "paired_daily_precip.csv", index=False)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_rows", 500)

    mt, mp = in_season(daily_t["date"], args.season), in_season(daily_p["date"], args.season)
    years_t = sorted({d.year for d in daily_t.loc[mt, "date"]})
    report(daily_t[mt], daily_p[mp],
           f"SEASON WINDOW {args.season}, years {years_t} "
           f"({daily_t.loc[mt, 'date'].nunique()} temperature days, "
           f"{daily_p.loc[mp, 'date'].nunique()} precipitation days)",
           "season", args.n_boot, args.min_frac, log)
    report(daily_t, daily_p,
           f"ALL DAYS {args.start}..{end} "
           f"({daily_t['date'].nunique()} temperature days, "
           f"{daily_p['date'].nunique()} precipitation days)",
           "all", args.n_boot, args.min_frac, log)
    log(f"\nwrote {OUT}/summary.txt, paired_daily_*.csv, summary_*_{{season,all}}.csv, "
        "rank_*.csv, bootstrap_pairs_*.csv")
    log.close()


if __name__ == "__main__":
    main()
