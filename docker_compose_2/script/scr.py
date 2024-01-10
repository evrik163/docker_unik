from pyspark.sql import SparkSession


spark = (SparkSession
         .builder
         .master("spark://spark-master:7077")
         .appName("spark_in_compose")
         .config("spark.jars", "/driver/postgresql-9.4.1207.jar")
         .config("spark.driver.extraClassPath", "/driver/postgresql-9.4.1207.jar")
         .getOrCreate())


sc = spark.sparkContext


df_prices = (
    spark.read
    .format("jdbc")
    .option("url", "jdbc:postgresql://postgres/spark")
    .option("dbtable", "public.prices")
    .option("user", "postgres")
    .option("driver", "org.postgresql.Driver")
    .option("password", "postgres")
    .load()
)


df_prices.createOrReplaceTempView("df")


spark.sql("""SELECT property_type, location, bedrooms, CEILING(AVG(price)) as average_price FROM df GROUP BY property_type, location, bedrooms""").show()
