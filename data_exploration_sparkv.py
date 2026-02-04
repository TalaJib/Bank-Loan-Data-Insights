from pyspark.sql import SparkSession
from pyspark.sql.functions import col


spark = SparkSession.builder \
    .appName("BankLoanBigData") \
    .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
    .getOrCreate()



df = spark.read.csv("loan_data.csv", header=True, inferSchema=True)


#remplir les valeurs manquantes
df_clean = df.na.fill({"ApplicantIncome": 5000})

df_clean.show()
print("Data processing complete.")

df_final = df_clean.withColumn("Total_Income", col("ApplicantIncome") + col("CoapplicantIncome"))

df_final.select("Total_Income", "Education").show(10)

spark.stop() 