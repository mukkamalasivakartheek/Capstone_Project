import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib

# Load data
df = pd.read_csv("aws_devops_cost_dataset_10k.csv")

X = df.drop("monthly_cost_usd", axis=1)
y = df["monthly_cost_usd"]

# Feature types
categorical_features = [
    "ec2_instance_type",
    "ec2_pricing_model",
    "rds_instance_type",
    "region",
    "environment"
]

numeric_features = [
    "ec2_instance_count",
    "ec2_hours",
    "codebuild_minutes",
    "pipeline_count",
    "s3_storage_gb",
    "ecr_storage_gb",
    "rds_hours",
    "rds_storage_gb",
    "data_transfer_out_gb",
    "cloudwatch_logs_gb"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

# Model
model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
print("MAE:", mean_absolute_error(y_test, preds))
print("R2:", r2_score(y_test, preds))

# Save model
joblib.dump(pipeline, "aws_cost_pred/aws_devops_cost_model.pkl")
