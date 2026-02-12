import joblib
import pandas as pd

model = joblib.load("aws_cost_pred/aws_devops_cost_model.pkl")

new_project = pd.DataFrame([{
    "ec2_instance_type": "m5.large",
    "ec2_instance_count": 4,
    "ec2_hours": 720,
    "ec2_pricing_model": "on_demand",
    "codebuild_minutes": 1500,
    "pipeline_count": 3,
    "s3_storage_gb": 80,
    "ecr_storage_gb": 40,
    "rds_instance_type": "db.t3.medium",
    "rds_hours": 720,
    "rds_storage_gb": 150,
    "data_transfer_out_gb": 120,
    "cloudwatch_logs_gb": 30,
    "region": "us-east-1",
    "environment": "prod"
}])

predicted_cost = model.predict(new_project)
print(f"Estimated Monthly AWS Cost: ${predicted_cost[0]:.2f}")
