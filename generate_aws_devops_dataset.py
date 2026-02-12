import random
import pandas as pd

# -----------------------------
# AWS PRICE MAPS (approx realistic)
# -----------------------------
EC2_PRICES = {
    "t3.micro": 0.0104,
    "t3.small": 0.0208,
    "t3.medium": 0.0416,
    "t3.large": 0.0832,
    "m5.large": 0.096,
    "m5.xlarge": 0.192,
    "c5.large": 0.085,
    "c5.xlarge": 0.17
}

RDS_PRICES = {
    "db.t3.micro": 0.017,
    "db.t3.medium": 0.067,
    "db.m5.large": 0.192
}

PRICING_MODEL_MULTIPLIER = {
    "on_demand": 1.0,
    "reserved": 0.65,
    "spot": 0.4
}

REGIONS = ["us-east-1", "us-west-2", "eu-west-1"]
ENVIRONMENTS = ["dev", "stage", "prod"]

ROWS = 10000
DATA = []

for _ in range(ROWS):
    ec2_type = random.choice(list(EC2_PRICES.keys()))
    rds_type = random.choice(list(RDS_PRICES.keys()))
    pricing_model = random.choice(list(PRICING_MODEL_MULTIPLIER.keys()))

    ec2_count = random.randint(1, 6)
    ec2_hours = random.choice([360, 720])

    codebuild_minutes = random.randint(200, 2500)
    pipeline_count = random.randint(1, 5)

    s3_storage = random.randint(10, 200)
    ecr_storage = random.randint(5, 100)

    rds_hours = 720
    rds_storage = random.randint(20, 300)

    data_out = random.randint(5, 200)
    logs_gb = random.randint(1, 50)

    region = random.choice(REGIONS)
    env = random.choice(ENVIRONMENTS)

    # -----------------------------
    # COST CALCULATION (AWS LOGIC)
    # -----------------------------
    ec2_cost = (
        EC2_PRICES[ec2_type]
        * ec2_count
        * ec2_hours
        * PRICING_MODEL_MULTIPLIER[pricing_model]
    )

    rds_cost = RDS_PRICES[rds_type] * rds_hours
    s3_cost = s3_storage * 0.023
    ecr_cost = ecr_storage * 0.10
    codebuild_cost = codebuild_minutes * 0.005
    data_transfer_cost = data_out * 0.09
    logs_cost = logs_gb * 0.50

    total_cost = round(
        ec2_cost
        + rds_cost
        + s3_cost
        + ecr_cost
        + codebuild_cost
        + data_transfer_cost
        + logs_cost,
        2
    )

    DATA.append([
        ec2_type, ec2_count, ec2_hours, pricing_model,
        codebuild_minutes, pipeline_count,
        s3_storage, ecr_storage,
        rds_type, rds_hours, rds_storage,
        data_out, logs_gb,
        region, env, total_cost
    ])

# -----------------------------
# CREATE CSV
# -----------------------------
columns = [
    "ec2_instance_type",
    "ec2_instance_count",
    "ec2_hours",
    "ec2_pricing_model",
    "codebuild_minutes",
    "pipeline_count",
    "s3_storage_gb",
    "ecr_storage_gb",
    "rds_instance_type",
    "rds_hours",
    "rds_storage_gb",
    "data_transfer_out_gb",
    "cloudwatch_logs_gb",
    "region",
    "environment",
    "monthly_cost_usd"
]

df = pd.DataFrame(DATA, columns=columns)
df.to_csv("aws_devops_cost_dataset_10k.csv", index=False)

print("✅ Generated aws_devops_cost_dataset_10k.csv with", len(df), "rows")
