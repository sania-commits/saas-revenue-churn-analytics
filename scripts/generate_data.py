import numpy as np
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
SEED = 42
N_CUSTOMERS = 5000

START_DATE = pd.Timestamp("2023-01-01")
END_DATE = pd.Timestamp("2026-08-01")

OUTPUT_DIR = Path("data/raw")

rng = np.random.default_rng(SEED)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# REFERENCE DATA
# --------------------------------------------------
plans = pd.DataFrame(
    [
        ["P01", "Starter", 29.0, "Small Business"],
        ["P02", "Professional", 79.0, "SMB"],
        ["P03", "Business", 149.0, "Mid-Market"],
        ["P04", "Enterprise", 399.0, "Enterprise"],
    ],
    columns=["plan_id", "plan_name", "monthly_price", "target_segment"],
)

regions = pd.DataFrame(
    [
        ["R01", "North America", "United States"],
        ["R02", "North America", "Canada"],
        ["R03", "Europe", "United Kingdom"],
        ["R04", "Europe", "Germany"],
        ["R05", "Europe", "Ireland"],
        ["R06", "Asia Pacific", "India"],
        ["R07", "Asia Pacific", "Australia"],
        ["R08", "Asia Pacific", "Singapore"],
    ],
    columns=["region_id", "region", "country"],
)

plan_price = dict(zip(plans["plan_id"], plans["monthly_price"]))


# --------------------------------------------------
# CUSTOMERS
# --------------------------------------------------
customer_ids = [f"C{i:05d}" for i in range(1, N_CUSTOMERS + 1)]

signup_days = pd.date_range(
    START_DATE,
    END_DATE - pd.offsets.MonthBegin(2),
    freq="D",
)

customers = pd.DataFrame(
    {
        "customer_id": customer_ids,
        "company_name": [f"SaaS Customer {i:05d}" for i in range(1, N_CUSTOMERS + 1)],
        "signup_date": rng.choice(signup_days, N_CUSTOMERS),
        "region_id": rng.choice(
            regions["region_id"],
            N_CUSTOMERS,
            p=[0.24, 0.07, 0.13, 0.09, 0.06, 0.25, 0.09, 0.07],
        ),
        "acquisition_channel": rng.choice(
            ["Organic Search", "Paid Search", "Partner", "Referral", "Outbound"],
            N_CUSTOMERS,
            p=[0.28, 0.23, 0.15, 0.19, 0.15],
        ),
        "company_size": rng.choice(
            ["Small", "Medium", "Large", "Enterprise"],
            N_CUSTOMERS,
            p=[0.42, 0.31, 0.18, 0.09],
        ),
    }
)

customers["signup_date"] = pd.to_datetime(customers["signup_date"])
customers = customers.sort_values("customer_id").reset_index(drop=True)


# --------------------------------------------------
# SUBSCRIPTIONS + MONTHLY REVENUE
# --------------------------------------------------
subscription_rows = []
revenue_rows = []

plan_ids = plans["plan_id"].tolist()

for customer in customers.itertuples(index=False):

    subscription_id = f"S-{customer.customer_id}"

    start_month = pd.Timestamp(customer.signup_date).to_period("M").to_timestamp()

    initial_plan = rng.choice(
        plan_ids,
        p=[0.43, 0.32, 0.18, 0.07],
    )

    billing_cycle = rng.choice(
        ["Monthly", "Annual"],
        p=[0.72, 0.28],
    )

    current_plan_index = plan_ids.index(initial_plan)

    # Customer-specific churn tendency.
    churn_probability = rng.uniform(0.006, 0.025)

    active = True
    churn_date = pd.NaT

    months = pd.date_range(
        start_month,
        END_DATE,
        freq="MS",
    )

    for month_number, month in enumerate(months):

        if not active:
            break

        # Prevent immediate lifecycle changes for brand-new customers.
        if month_number >= 3:

            event_roll = rng.random()

            # Churn
            if event_roll < churn_probability:
                active = False
                churn_date = month

                revenue_rows.append(
                    [
                        month,
                        customer.customer_id,
                        subscription_id,
                        plan_ids[current_plan_index],
                        billing_cycle,
                        0.0,
                        "Churned",
                    ]
                )
                break

            # Upgrade
            elif event_roll < churn_probability + 0.018:
                if current_plan_index < len(plan_ids) - 1:
                    current_plan_index += 1

            # Downgrade
            elif event_roll < churn_probability + 0.030:
                if current_plan_index > 0:
                    current_plan_index -= 1

        current_plan = plan_ids[current_plan_index]
        base_mrr = plan_price[current_plan]

        # Annual contracts get a 10% effective monthly discount.
        mrr = base_mrr if billing_cycle == "Monthly" else base_mrr * 0.90

        revenue_rows.append(
            [
                month,
                customer.customer_id,
                subscription_id,
                current_plan,
                billing_cycle,
                round(mrr, 2),
                "Active",
            ]
        )

    subscription_rows.append(
        [
            subscription_id,
            customer.customer_id,
            start_month,
            initial_plan,
            billing_cycle,
            churn_date,
            "Churned" if pd.notna(churn_date) else "Active",
        ]
    )


subscriptions = pd.DataFrame(
    subscription_rows,
    columns=[
        "subscription_id",
        "customer_id",
        "subscription_start_date",
        "initial_plan_id",
        "billing_cycle",
        "churn_date",
        "subscription_status",
    ],
)

monthly_revenue = pd.DataFrame(
    revenue_rows,
    columns=[
        "month",
        "customer_id",
        "subscription_id",
        "plan_id",
        "billing_cycle",
        "mrr",
        "status",
    ],
)


# --------------------------------------------------
# SAVE RAW DATA
# --------------------------------------------------
customers.to_csv(OUTPUT_DIR / "customers.csv", index=False)
plans.to_csv(OUTPUT_DIR / "plans.csv", index=False)
regions.to_csv(OUTPUT_DIR / "regions.csv", index=False)
subscriptions.to_csv(OUTPUT_DIR / "subscriptions.csv", index=False)
monthly_revenue.to_csv(OUTPUT_DIR / "monthly_revenue.csv", index=False)


# --------------------------------------------------
# VALIDATION SUMMARY
# --------------------------------------------------
print("\n--- SaaS DATASET GENERATED ---")
print(f"Customers       : {len(customers):,}")
print(f"Plans           : {len(plans):,}")
print(f"Regions         : {len(regions):,}")
print(f"Subscriptions   : {len(subscriptions):,}")
print(f"Revenue rows    : {len(monthly_revenue):,}")

print(
    "Date range       :",
    monthly_revenue["month"].min().date(),
    "to",
    monthly_revenue["month"].max().date(),
)

print(
    "Active customers :",
    (subscriptions["subscription_status"] == "Active").sum(),
)

print(
    "Churned customers:",
    (subscriptions["subscription_status"] == "Churned").sum(),
)

print(
    "Total MRR rows >0:",
    (monthly_revenue["mrr"] > 0).sum(),
)

print("\nFiles created in:", OUTPUT_DIR.resolve())
