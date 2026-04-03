"""
Synthetic Campaign Data Generator
Electronic Campaigns Efficiency Dashboard
Author: Abdelrahman Elmogy

Generates realistic synthetic campaign data that mirrors production structure.
No real customer or company data is used.
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker("ar_EG")
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
N_CAMPAIGNS = 200
N_CONTACTS  = 5000
OUTPUT_DIR  = os.path.dirname(os.path.abspath(__file__))

CHANNELS        = ["IVR", "WhatsApp", "Email", "SMS"]
SEGMENTS        = ["High Priority", "Medium Priority", "Low Priority"]
CAMPAIGN_STATUS = ["Completed", "Active", "Paused", "Cancelled"]

# Realistic KPI ranges per channel (based on industry benchmarks)
CHANNEL_PROFILES = {
    "IVR":       {"delivery": (0.70, 0.90), "response": (0.10, 0.25), "conversion": (0.05, 0.15), "cost_per_contact": (0.8,  1.5)},
    "WhatsApp":  {"delivery": (0.85, 0.98), "response": (0.25, 0.50), "conversion": (0.15, 0.35), "cost_per_contact": (0.3,  0.8)},
    "Email":     {"delivery": (0.80, 0.95), "response": (0.05, 0.15), "conversion": (0.03, 0.10), "cost_per_contact": (0.05, 0.2)},
    "SMS":       {"delivery": (0.88, 0.97), "response": (0.08, 0.20), "conversion": (0.04, 0.12), "cost_per_contact": (0.1,  0.4)},
}


def random_date(start_days_ago=365):
    start = datetime.now() - timedelta(days=start_days_ago)
    return start + timedelta(days=random.randint(0, start_days_ago))


# ─────────────────────────────────────────
# 1. CAMPAIGNS TABLE
# ─────────────────────────────────────────
def generate_campaigns():
    rows = []
    for i in range(1, N_CAMPAIGNS + 1):
        channel   = random.choice(CHANNELS)
        profile   = CHANNEL_PROFILES[channel]
        segment   = random.choice(SEGMENTS)
        start_dt  = random_date()
        end_dt    = start_dt + timedelta(days=random.randint(1, 14))
        contacts  = random.randint(100, 2000)

        delivery_rate    = round(random.uniform(*profile["delivery"]),    4)
        response_rate    = round(random.uniform(*profile["response"]),    4)
        conversion_rate  = round(random.uniform(*profile["conversion"]),  4)
        cost_per_contact = round(random.uniform(*profile["cost_per_contact"]), 2)

        delivered   = int(contacts * delivery_rate)
        responded   = int(delivered * response_rate)
        converted   = int(responded * conversion_rate)
        total_cost  = round(contacts * cost_per_contact, 2)

        avg_debt        = random.randint(500, 10000)
        recovery_amount = round(converted * avg_debt * random.uniform(0.3, 0.8), 2)
        roi             = round((recovery_amount - total_cost) / total_cost * 100, 2) if total_cost > 0 else 0

        rows.append({
            "campaign_id":       f"CAMP-{i:04d}",
            "campaign_name":     f"{channel} {segment} Campaign {i}",
            "channel":           channel,
            "segment":           segment,
            "status":            random.choice(CAMPAIGN_STATUS),
            "start_date":        start_dt.strftime("%Y-%m-%d"),
            "end_date":          end_dt.strftime("%Y-%m-%d"),
            "total_contacts":    contacts,
            "delivered":         delivered,
            "responded":         responded,
            "converted":         converted,
            "delivery_rate":     delivery_rate,
            "response_rate":     response_rate,
            "conversion_rate":   conversion_rate,
            "cost_per_contact":  cost_per_contact,
            "total_cost":        total_cost,
            "recovery_amount":   recovery_amount,
            "campaign_roi":      roi,
        })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────
# 2. CONTACTS TABLE
# ─────────────────────────────────────────
def generate_contacts(campaigns_df):
    rows = []
    for i in range(1, N_CONTACTS + 1):
        campaign = campaigns_df.sample(1).iloc[0]
        channel  = campaign["channel"]
        profile  = CHANNEL_PROFILES[channel]

        delivered  = random.random() < random.uniform(*profile["delivery"])
        responded  = delivered and (random.random() < random.uniform(*profile["response"]))
        converted  = responded and (random.random() < random.uniform(*profile["conversion"]))

        # Weight contact hours — peak around 10 AM–12 PM
        hours   = list(range(8, 22))   # 14 hours: 8,9,...,21
        weights = [1,2,5,6,5,3,2,2,3,4,3,2,1,1]
        contact_hour = random.choices(hours, weights=weights, k=1)[0]

        campaign_start = datetime.strptime(campaign["start_date"], "%Y-%m-%d")
        contact_dt = campaign_start + timedelta(
            days=random.randint(0, 7),
            hours=contact_hour,
            minutes=random.randint(0, 59)
        )

        rows.append({
            "contact_id":     f"CON-{i:06d}",
            "campaign_id":    campaign["campaign_id"],
            "channel":        channel,
            "segment":        campaign["segment"],
            "contact_time":   contact_dt.strftime("%Y-%m-%d %H:%M"),
            "delivered":      int(delivered),
            "responded":      int(responded),
            "converted":      int(converted),
            "debt_amount":    round(random.uniform(200, 15000), 2),
            "recovered_amount": round(random.uniform(100, 8000), 2) if converted else 0.0,
        })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("⚙️  Generating synthetic campaign data...")

    campaigns_df = generate_campaigns()
    contacts_df  = generate_contacts(campaigns_df)

    campaigns_path = os.path.join(OUTPUT_DIR, "sample_campaigns.csv")
    contacts_path  = os.path.join(OUTPUT_DIR, "sample_contacts.csv")

    campaigns_df.to_csv(campaigns_path, index=False, encoding="utf-8-sig")
    contacts_df.to_csv(contacts_path,   index=False, encoding="utf-8-sig")

    print(f"✅ Campaigns table: {len(campaigns_df)} rows → {campaigns_path}")
    print(f"✅ Contacts table:  {len(contacts_df)} rows → {contacts_path}")
    print("\n📊 Quick summary:")
    print(campaigns_df.groupby("channel")[["delivery_rate","response_rate","conversion_rate","campaign_roi"]].mean().round(3))
