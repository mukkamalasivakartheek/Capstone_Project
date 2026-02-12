import streamlit as st
import pandas as pd
import joblib

model = joblib.load("aws_devops_cost_model.pkl")

st.set_page_config(
    page_title="AWS DevOps Cost Predictor",
    layout="centered"
)

st.title("💰 AWS DevOps Monthly Cost Predictor")
st.markdown("Predict AWS cost **before deployment** using ML")

st.divider()


with st.form("cost_form"):

    st.subheader("🖥️ Compute (EC2)")
    ec2_instance_type = st.selectbox(
        "EC2 Instance Type",
        ["t3.micro", "t3.small", "t3.medium", "t3.large",
         "m5.large", "m5.xlarge", "c5.large", "c5.xlarge"]
    )

    ec2_instance_count = st.number_input(
        "Number of EC2 Instances", min_value=1, max_value=20, value=2
    )

    ec2_hours = st.selectbox(
        "EC2 Hours per Month",
        [360, 720]
    )

    ec2_pricing_model = st.selectbox(
        "Pricing Model",
        ["on_demand", "reserved", "spot"]
    )

    st.subheader("🔁 CI/CD")
    codebuild_minutes = st.number_input(
        "CodeBuild Minutes / Month", min_value=0, value=1000
    )

    pipeline_count = st.number_input(
        "Number of Pipelines", min_value=1, max_value=10, value=2
    )

    st.subheader("📦 Storage")
    s3_storage_gb = st.number_input(
        "S3 Storage (GB)", min_value=0, value=50
    )

    ecr_storage_gb = st.number_input(
        "ECR Storage (GB)", min_value=0, value=20
    )

    st.subheader("🗄️ Database (RDS)")
    rds_instance_type = st.selectbox(
        "RDS Instance Type",
        ["db.t3.micro", "db.t3.medium", "db.m5.large"]
    )

    rds_hours = st.selectbox(
        "RDS Hours per Month",
        [360, 720]
    )

    rds_storage_gb = st.number_input(
        "RDS Storage (GB)", min_value=20, value=100
    )

    st.subheader("🌐 Network & Monitoring")
    data_transfer_out_gb = st.number_input(
        "Data Transfer Out (GB)", min_value=0, value=50
    )

    cloudwatch_logs_gb = st.number_input(
        "CloudWatch Logs (GB)", min_value=0, value=10
    )

    st.subheader("🌍 Environment")
    region = st.selectbox(
        "AWS Region",
        ["us-east-1", "us-west-2", "eu-west-1"]
    )

    environment = st.selectbox(
        "Environment",
        ["dev", "stage", "prod"]
    )

    submitted = st.form_submit_button("🚀 Predict Monthly Cost")

if submitted:
    input_df = pd.DataFrame([{
        "ec2_instance_type": ec2_instance_type,
        "ec2_instance_count": ec2_instance_count,
        "ec2_hours": ec2_hours,
        "ec2_pricing_model": ec2_pricing_model,
        "codebuild_minutes": codebuild_minutes,
        "pipeline_count": pipeline_count,
        "s3_storage_gb": s3_storage_gb,
        "ecr_storage_gb": ecr_storage_gb,
        "rds_instance_type": rds_instance_type,
        "rds_hours": rds_hours,
        "rds_storage_gb": rds_storage_gb,
        "data_transfer_out_gb": data_transfer_out_gb,
        "cloudwatch_logs_gb": cloudwatch_logs_gb,
        "region": region,
        "environment": environment
    }])

    predicted_cost = model.predict(input_df)[0]

    st.divider()
    st.success(f"💵 **Estimated Monthly AWS Cost: ${predicted_cost:,.2f}**")

    st.caption("Prediction powered by ML (XGBoost)")

