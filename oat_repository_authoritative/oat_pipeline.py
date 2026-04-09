#!/usr/bin/env python3
"""
Reference-aware feature engineering pipeline for semi-structured clinical laboratory reports.

This public reproduction script rebuilds deposited outputs from the deposited audit table.
It validates interval parsing, recomputes flags, rebuilds feature matrices, runs PCA,
and regenerates repository output files.

Usage:
  python oat_pipeline.py

Inputs:
  audit_table_long.csv

Outputs:
  output/feature_matrix_75.csv
  output/feature_matrix_73_no_ketones.csv
  output/pca_scores_75.csv
  output/pca_loadings_75.csv
  output/Table_1_threshold_counts.csv
  output/Table_2_twosided_top.csv
  output/Table_3_onesided_top.csv
  output/Figure_1_PCA.png
  output/pca_scores_rank_based.csv
  output/pca_loadings_rank_based.csv
  output/rank_based_pca_sensitivity_metrics.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

KETONE_ANALYTES = ["Acetoacetic", "3-Hydroxybutyric"]
PARTICIPANT_ORDER = [f"R{i:02d}" for i in range(1, 11)]


def z_approx(value, lower, upper):
    mu = (lower + upper) / 2.0
    sigma = (upper - lower) / 3.92
    return (value - mu) / sigma if sigma != 0 else 0.0


def frac_upper(value, upper):
    return value / upper if upper != 0 else 0.0


def recompute_flags(df):
    flags = []
    for _, row in df.iterrows():
        v = row["value"]
        if row["interval_type"] == "two-sided":
            if v < row["lower_bound"]:
                flags.append("L")
            elif v > row["upper_bound"]:
                flags.append("H")
            else:
                flags.append(None)
        else:
            flags.append("H" if v > row["upper_bound"] else None)
    return flags


def run_pca(matrix, n_components=2):
    X = StandardScaler().fit_transform(matrix.values)
    pca = PCA(n_components=n_components)
    scores = pca.fit_transform(X)
    scores_df = pd.DataFrame(scores, index=matrix.index, columns=[f"PC{i+1}" for i in range(n_components)])
    loadings_df = pd.DataFrame(pca.components_.T, index=matrix.columns, columns=[f"PC{i+1}" for i in range(n_components)])
    return scores_df, pca.explained_variance_ratio_ * 100, loadings_df




def run_rank_based_pca(df_values, n_components=2):
    ranked = df_values.rank(axis=0, method="average")
    X = StandardScaler().fit_transform(ranked.values)
    pca = PCA(n_components=n_components)
    scores = pca.fit_transform(X)
    scores_df = pd.DataFrame(scores, index=df_values.index, columns=[f"PC{i+1}" for i in range(n_components)])
    loadings_df = pd.DataFrame(pca.components_.T, index=df_values.columns, columns=[f"PC{i+1}" for i in range(n_components)])
    return scores_df, pca.explained_variance_ratio_ * 100, loadings_df


def rank_based_sensitivity_metrics(reference_scores, rank_scores):
    rows = []
    for i in range(reference_scores.shape[1]):
        for j in range(rank_scores.shape[1]):
            ref = reference_scores.iloc[:, i]
            alt = rank_scores.iloc[:, j]
            rho = float(pd.Series(ref).corr(pd.Series(alt), method="spearman"))
            rho_flipped = float(pd.Series(ref).corr(pd.Series(-alt), method="spearman"))
            pearson = float(pd.Series(ref).corr(pd.Series(alt), method="pearson"))
            pearson_flipped = float(pd.Series(ref).corr(pd.Series(-alt), method="pearson"))
            use_flip = abs(rho_flipped) > abs(rho)
            rows.append({
                "reference_component": f"PC{i+1}",
                "rank_component": f"PC{j+1}",
                "sign_applied_to_rank_component": "-" if use_flip else "+",
                "spearman_rho": round(rho_flipped if use_flip else rho, 3),
                "pearson_r": round(pearson_flipped if use_flip else pearson, 3),
            })
    return pd.DataFrame(rows)

def table_threshold_counts(df):
    rows = []
    for pid in PARTICIPANT_ORDER:
        p = df[df["participant"] == pid]
        oor = int(p["flag"].notna().sum())
        lenient = int(sum(
            (abs(r["transformed_score"]) >= 1 if r["interval_type"] == "two-sided"
             else r["transformed_score"] >= 0.75)
            for _, r in p.iterrows()
        ))
        stringent = int(sum(
            (abs(r["transformed_score"]) >= 2 if r["interval_type"] == "two-sided"
             else r["transformed_score"] >= 1.0)
            for _, r in p.iterrows()
        ))
        rows.append({
            "participant": pid,
            "out_of_range_flags": oor,
            "lenient_threshold_count": lenient,
            "stringent_threshold_count": stringent,
        })
    return pd.DataFrame(rows)


def table_twosided_top(df, n=10):
    rows = []
    ts = df[df["interval_type"] == "two-sided"]
    for analyte, ad in ts.groupby("analyte"):
        s = ad["transformed_score"]
        rows.append({
            "analyte": analyte,
            "n_two_sided": len(ad),
            "mean_z_approx": round(float(s.mean()), 2),
            "mean_abs_z": round(float(s.abs().mean()), 2),
            "pct_abs_z_ge_1": round(float(100 * (s.abs() >= 1).mean()), 1),
            "pct_abs_z_ge_2": round(float(100 * (s.abs() >= 2).mean()), 1),
            "pct_out_of_range": round(float(100 * ad["flag"].notna().mean()), 1),
        })
    return pd.DataFrame(rows).sort_values(
        ["pct_abs_z_ge_1", "mean_abs_z", "analyte"],
        ascending=[False, False, True]
    ).head(n)


def table_onesided_top(df, n=10):
    rows = []
    os_df = df[df["interval_type"] == "one-sided"]
    for analyte, ad in os_df.groupby("analyte"):
        s = ad["transformed_score"]
        rows.append({
            "analyte": analyte,
            "n_one_sided": len(ad),
            "mean_f_x_over_u": round(float(s.mean()), 2),
            "max_f_x_over_u": round(float(s.max()), 2),
            "pct_f_ge_0_75": round(float(100 * (s >= 0.75).mean()), 1),
            "pct_f_ge_1_0": round(float(100 * (s >= 1.0).mean()), 1),
            "pct_out_of_range": round(float(100 * ad["flag"].notna().mean()), 1),
        })
    return pd.DataFrame(rows).sort_values(
        ["mean_f_x_over_u", "max_f_x_over_u", "analyte"],
        ascending=[False, False, True]
    ).head(n)


def plot_pca_dual(scores_full, var_full, scores_reduced, var_reduced, path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    for ax, sc, ve, title in [
        (ax1, scores_full, var_full, "Full feature matrix (75 analytes)"),
        (ax2, scores_reduced, var_reduced, "Ketone-body analytes excluded (73 analytes)"),
    ]:
        ax.scatter(sc["PC1"], sc["PC2"], s=81)
        for pid in sc.index:
            ax.annotate(pid, (sc.loc[pid, "PC1"], sc.loc[pid, "PC2"]),
                        textcoords="offset points", xytext=(6, 6), fontsize=9)
        ax.set_xlabel(f"PC1 ({ve[0]:.1f}% variance)")
        ax.set_ylabel(f"PC2 ({ve[1]:.1f}% variance)")
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.axhline(0, color="gray", lw=0.5, ls="--")
        ax.axvline(0, color="gray", lw=0.5, ls="--")
        ax.grid(True, alpha=0.3)
    ax1.text(-0.08, 1.05, "A.", transform=ax1.transAxes, fontsize=14, fontweight="bold")
    ax2.text(-0.08, 1.05, "B.", transform=ax2.transAxes, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    df = pd.read_csv("audit_table_long.csv")
    df["flag_recomputed_check"] = recompute_flags(df)

    feature_matrix = df.pivot_table(index="participant", columns="analyte", values="transformed_score", aggfunc="first")
    feature_matrix = feature_matrix.loc[PARTICIPANT_ORDER]
    raw_value_matrix = df.pivot_table(index="participant", columns="analyte", values="value", aggfunc="first")
    raw_value_matrix = raw_value_matrix.loc[PARTICIPANT_ORDER]

    scores_full, var_full, loadings_full = run_pca(feature_matrix)
    rank_scores, rank_var, rank_loadings = run_rank_based_pca(raw_value_matrix)
    rank_metrics = rank_based_sensitivity_metrics(scores_full, rank_scores)

    reduced_matrix = feature_matrix.drop(columns=[c for c in KETONE_ANALYTES if c in feature_matrix.columns], errors="ignore")
    reduced_matrix = reduced_matrix.loc[PARTICIPANT_ORDER]
    scores_reduced, var_reduced, _ = run_pca(reduced_matrix)

    table1 = table_threshold_counts(df)
    table2 = table_twosided_top(df)
    table3 = table_onesided_top(df)

    feature_matrix.to_csv(OUTPUT_DIR / "feature_matrix_75.csv", index_label="participant")
    reduced_matrix.to_csv(OUTPUT_DIR / "feature_matrix_73_no_ketones.csv", index_label="participant")
    scores_full.to_csv(OUTPUT_DIR / "pca_scores_75.csv", index_label="participant")
    loadings_full.to_csv(OUTPUT_DIR / "pca_loadings_75.csv", index_label="analyte")
    table1.to_csv(OUTPUT_DIR / "Table_1_threshold_counts.csv", index=False)
    table2.to_csv(OUTPUT_DIR / "Table_2_twosided_top.csv", index=False)
    table3.to_csv(OUTPUT_DIR / "Table_3_onesided_top.csv", index=False)
    plot_pca_dual(scores_full, var_full, scores_reduced, var_reduced, OUTPUT_DIR / "Figure_1_PCA.png")
    rank_scores.to_csv(OUTPUT_DIR / "pca_scores_rank_based.csv", index_label="participant")
    rank_loadings.to_csv(OUTPUT_DIR / "pca_loadings_rank_based.csv", index_label="analyte")
    rank_metrics.to_csv(OUTPUT_DIR / "rank_based_pca_sensitivity_metrics.csv", index=False)

    flagged = df["flag"].notna().sum()
    concordant = (df.loc[df["flag"].notna(), "flag"] == df.loc[df["flag"].notna(), "flag_recomputed_check"]).sum()

    print("Repository outputs regenerated.")
    print(f"Participants: {feature_matrix.shape[0]}")
    print(f"Features: {feature_matrix.shape[1]}")
    print(f"Flag concordance: {concordant}/{flagged}")
    print(f"Full PCA variance: PC1={var_full[0]:.1f}%, PC2={var_full[1]:.1f}%")
    print(f"Ketone-excluded PCA variance: PC1={var_reduced[0]:.1f}%, PC2={var_reduced[1]:.1f}%")
    print(f"Rank-based PCA variance: PC1={rank_var[0]:.1f}%, PC2={rank_var[1]:.1f}%")


if __name__ == "__main__":
    main()
