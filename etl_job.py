import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Job initialization
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Define S3 paths
bucket_name = "surajb-bucket202506"
input_prefix = "files/input/"
output_prefix = "files/output/"

input_path = f"s3://{bucket_name}/{input_prefix}"
output_path = f"s3://{bucket_name}/{output_prefix}"

# Read data from S3
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_path]},
    format="csv"
)

# Write data back to another folder in the same bucket
glueContext.write_dynamic_frame.from_options(
    frame=df,
    connection_type="s3",
    connection_options={"path": output_path},
    format="csv"
)

# Commit the job
job.commit()

print("Data processed successfully!")
