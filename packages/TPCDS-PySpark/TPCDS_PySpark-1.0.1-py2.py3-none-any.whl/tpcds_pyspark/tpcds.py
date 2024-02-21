#!/usr/bin/env python3

import sys
import time
import pandas as pd
from importlib.resources import files
from pyspark.sql import SparkSession
from sparkmeasure import StageMetrics

class TPCDS:
    """This implements the TPCDS workload generator with Apache Spark and sparkMeasure
    using PySpark"""

    tpcds_queries = [
        'q1.sql', 'q2.sql', 'q3.sql', 'q4.sql', 'q5.sql', 'q5a.sql', 'q6.sql', 'q7.sql', 'q8.sql', 'q9.sql',
        'q10.sql', 'q10a.sql', 'q11.sql', 'q12.sql', 'q13.sql', 'q14a.sql', 'q14b.sql', 'q14.sql', 'q15.sql',
        'q16.sql', 'q17.sql', 'q18.sql', 'q18a.sql', 'q19.sql', 'q20.sql', 'q21.sql', 'q22.sql', 'q22a.sql',
        'q23a.sql', 'q23b.sql', 'q24.sql', 'q24a.sql', 'q24b.sql', 'q25.sql', 'q26.sql', 'q27.sql', 'q27a.sql',
        'q28.sql', 'q29.sql', 'q30.sql', 'q31.sql', 'q32.sql', 'q33.sql', 'q34.sql', 'q35.sql', 'q35a.sql',
        'q36.sql', 'q36a.sql', 'q37.sql', 'q38.sql', 'q39a.sql', 'q39b.sql', 'q40.sql', 'q41.sql', 'q42.sql',
        'q43.sql', 'q44.sql', 'q45.sql', 'q46.sql', 'q47.sql', 'q48.sql', 'q49.sql', 'q50.sql', 'q51.sql',
        'q51a.sql', 'q52.sql', 'q53.sql', 'q54.sql', 'q55.sql', 'q56.sql', 'q57.sql', 'q58.sql', 'q59.sql',
        'q60.sql', 'q61.sql', 'q62.sql', 'q63.sql', 'q64.sql', 'q65.sql', 'q66.sql', 'q67.sql', 'q67a.sql',
        'q68.sql', 'q69.sql', 'q70.sql', 'q70a.sql', 'q71.sql',  'q72.sql', 'q73.sql', 'q74.sql', 'q75.sql',
        'q76.sql', 'q77.sql', 'q77a.sql', 'q78.sql', 'q79.sql', 'q80.sql', 'q80a.sql', 'q81.sql', 'q82.sql',
        'q83.sql', 'q84.sql', 'q85.sql', 'q86.sql', 'q86a.sql', 'q87.sql', 'q88.sql', 'q89.sql', 'q90.sql',
        'q91.sql', 'q92.sql', 'q93.sql', 'q94.sql', 'q95.sql', 'q96.sql', 'q97.sql', 'q98.sql', 'q99.sql'
    ]

    # List of table names for the TPCDS benchmark
    tpcds_tables = [
        "catalog_returns", "catalog_sales", "inventory", "store_returns",
        "store_sales", "web_returns", "web_sales", "call_center",
        "catalog_page", "customer", "customer_address",
        "customer_demographics", "date_dim", "household_demographics",
        "income_band", "item", "promotion", "reason", "ship_mode",
        "store", "time_dim", "warehouse", "web_page", "web_site"
    ]

    def __init__(self, data_path="./tpcds_10", data_format="parquet",
                 num_runs=2, queries_repeat_times=3, queries=tpcds_queries, sleep_time=1):
        self.data_path = data_path
        self.data_format = data_format
        self.queries = queries
        self.queries_repeat_times = queries_repeat_times
        self.num_runs = num_runs
        self.sleep_time = sleep_time

        # Path to the TPCDS queries on the filesystem
        tpcds_pyspark_files = files('tpcds_pyspark')
        self.queries_path = tpcds_pyspark_files.joinpath('Queries')
        # Path to sparkMeasure bundled jar
        # TODO: handle the embedded sparkMeasure jar for scala 2.12 and 2.13 in the same code
        sparkMeasure_jar = tpcds_pyspark_files.joinpath('spark-measure_2.12-0.23.jar')

        print(f"sparkMeasure jar path: {sparkMeasure_jar}")
        print(f"TPCDS queries path: {self.queries_path}")

        # This configures the SparkSession
        # The recommended way is to use spark-submit to launch tpcds_pyspark.py
        # When run directly instead, the SparkSession will be created here using default config.
        self.spark = (
            SparkSession.builder
                .appName("TPCDS PySpark - Run TPCDS queries in PySpark instrumented with sparkMeasure")
                .config("spark.driver.extraClassPath", sparkMeasure_jar)
                .getOrCreate()
             )

    def map_tables(self, define_temporary_views=True, define_catalog_tables=False):
        """Map table data on the filesystem to Spark tables.
        This supports both creating temporary views or metastore catalog tables
        for the tables used in the TPCDS queries.
        This supports all data formats supported by Spark."""

        data_path = self.data_path
        data_format = self.data_format
        spark = self.spark
        tables = self.tpcds_tables

        # Loop through each table name and create a temporary view for it
        if define_temporary_views:
            for table in tables:
                print(f"Creating temporary view {table}")
                table_full_path = data_path + "/" + table
                spark.read.format(data_format).load(table_full_path).createOrReplaceTempView(table)

        # Loop through each table name and create a catalog table for it
        # This will use the default database for the Spark session
        # defined in spark.sql.catalog.spark_catalog.defaultDatabase
        if define_catalog_tables:
            for table in tables:
                # Construct the full path for the table data
                table_full_path = f"{data_path}/{table}"

                # Log the creation of the catalog table
                print(f"Creating catalog table {table}")

                # Drop the table if it already exists to avoid conflicts
                spark.sql(f"DROP TABLE IF EXISTS {table}")

                # Create an external table pointing to the data path
                create_table_sql = f"""
                CREATE EXTERNAL TABLE IF NOT EXISTS {table}
                USING {data_format}
                OPTIONS (path '{table_full_path}')
                """
                spark.sql(create_table_sql)
                #
                # Fix for partitioned tables, this picks up the partitioning schema from the data's folder structure
                try:
                    # Attempt to repair the table
                    repair_command = f"MSCK REPAIR TABLE {table}"
                    spark.sql(repair_command)
                    print("...partitioned table repaired to map the data folder structure")
                except Exception as e:
                    # Handle exceptions, likely due to the table not being partitioned
                    None

    def compute_table_statistics(self, collect_column_statistics=True):
        # Compute statistics on the tables/views
        spark = self.spark
        tables = self.tpcds_tables
        for table in tables:
            print("Enabling Cost Based Optimization (CBO) and computing statistics")
            spark.sql("SET spark.sql.cbo.enabled=true")
            if collect_column_statistics:
                spark.sql("SET spark.sql.statistics.histogram.enabled=true")
                print(f"Computing table and column statistics for {table}")
                spark.sql(f"ANALYZE TABLE {table} COMPUTE STATISTICS FOR ALL COLUMNS")
            else:
                print(f"Computing table statistics for {table}")
                spark.sql(f"ANALYZE TABLE {table} COMPUTE STATISTICS")

    def run_TPCDS(self):
        """Run the TPCDS queries and return the instrumentation data.
        Requires the Spark session to be already created and configured.
        Requires the TPCDS data to be mapped to Spark tables ot temporary views,
        See map_tables() method.
        """

        spark = self.spark
        queries_path = str(self.queries_path)
        queries = self.queries
        queries_repeat_times = self.queries_repeat_times
        num_runs = self.num_runs
        sleep_time = self.sleep_time

        # List to store the job timing and metrics measurements
        instrumentation = []
        stagemetrics = StageMetrics(spark)
        self.start_time = time.ctime()

        # External loop to run the query set multiple times (configurable)
        for run_id in range(num_runs):
            # Read and run the queries from the queries_path
            for query in queries:
                with open(queries_path + "/" + query, 'r') as f:
                    # Read the query text from the file
                    query_text = f.read()

                    # Internal loop to run the same query multiple times (configurable)
                    for i in range(queries_repeat_times):

                        print(f"\nRun {run_id} - query {query} - attempt {i} - starting...")

                        # Add a configurable sleep time (default 1 sec) before each query execution
                        time.sleep(sleep_time)
                        # Set the job group and description to the query name
                        spark.sparkContext.setJobGroup("TPCDS", query)
                        # Start the stage metrics collection
                        stagemetrics.begin()

                        # Run the query and send the output to a noop sink
                        spark.sql(query_text).write.format("noop").mode("overwrite").save()

                        # End the stage metrics collection
                        stagemetrics.end()
                        # Clear the job group after the query execution
                        spark.sparkContext.setJobGroup("", "")

                        # Collect metrics and timing measurements
                        metrics = stagemetrics.aggregate_stagemetrics()
                        executorRunTime = round(metrics.get('executorRunTime') / 1000, 2)
                        executorCpuTime = round(metrics.get('executorCpuTime') / 1000, 2)
                        jvmGCTime = round(metrics.get('jvmGCTime') / 1000, 2)
                        elapsedTime = round(metrics.get('elapsedTime') / 1000, 2)

                        # print the timing measurements
                        print("Job finished")
                        print(f"...Elapsed Time = {elapsedTime} sec")
                        print(f"...Executors Run Time = {executorRunTime} sec")
                        print(f"...Executors CPU Time = {executorCpuTime} sec")
                        print(f"...Executors JVM GC Time = {jvmGCTime} sec")

                        # append the timing measurements to the list
                        runinfo = {'run_id': run_id, 'query': query, 'query_rerun_id': i}
                        instrumentation.append({**runinfo, **metrics})

        self.end_time = time.ctime()
        return instrumentation

    def print_test_results(self, test_results, file_csv=sys.stdout, file_metadata=sys.stdout,
                           file_grouped=sys.stdout, file_aggregated=sys.stdout):
        """Print the test results to the specified file (default is stdout)"""

        # 1. Print test configuration to a metadata text file (default is stdout)
        print("", file=file_metadata)
        print("****************************************************************************************", file=file_metadata)
        print("TPCDS with PySpark - workload configuration and metadata summary", file=file_metadata)
        print("****************************************************************************************", file=file_metadata)
        print("", file=file_metadata)

        print(f"Queries list = {', '.join(self.queries)}", file=file_metadata)
        print(f"Number of runs = {self.num_runs}", file=file_metadata)
        print(f"Query execution repeat times = {self.queries_repeat_times}", file=file_metadata)
        print(f"Total number of executed queries = {len(test_results)}", file=file_metadata)
        print(f"Sleep time (sec) between queries = {self.sleep_time}", file=file_metadata)
        print(f"Queries path = {self.queries_path}", file=file_metadata)
        print(f"Data path = {self.data_path}", file=file_metadata)
        print(f"Start time = {self.start_time}", file=file_metadata)
        print(f"End time = {self.end_time}", file=file_metadata)

        print("", file=file_metadata)
        spark = self.spark
        print(f"Spark version = {spark.version}", file=file_metadata)
        spark_master = spark.conf.get("spark.master")
        print(f"Spark master = {spark_master}", file=file_metadata)
        executor_memory = spark.conf.get("spark.executor.memory", "")
        print(f"Executor memory: {executor_memory}", file=file_metadata)
        executor_cores = spark.conf.get("spark.executor.cores", "")
        print(f"Executor cores: {executor_cores}", file=file_metadata)
        dynamic_allocation = spark.conf.get("spark.dynamicAllocation.enabled", "")
        print(f"Dynamic allocation: {dynamic_allocation}", file=file_metadata)
        if dynamic_allocation == "false":
            num_executors = spark.conf.get("spark.executor.instances")
            print(f"Number of executors: {num_executors}", file=file_metadata)
        elif dynamic_allocation == "true":
            num_min_executors = spark.conf.get("spark.dynamicAllocation.minExecutors")
            print(f"Minimum Number of executors: {num_min_executors}", file=file_metadata)
            num_max_executors = spark.conf.get("spark.dynamicAllocation.maxExecutors")
            print(f"Maximum Number of executors: {num_max_executors}", file=file_metadata)
        cbo = spark.conf.get("spark.sql.cbo.enabled")
        print(f"Cost Based Optimization (CBO): {cbo}", file=file_metadata)
        hist = spark.conf.get("spark.sql.statistics.histogram.enabled")
        print(f"Histogram statistics: {hist}", file=file_metadata)
        print("", file=file_metadata)

        # 2. Print the test results, consisting of a line for each query executed, with details on
        # the collected execution metrics.
        # the output is in csv format, printed to file_csv (default is stdout)
        #
        # Convert results to a pandas DataFrame
        results_pdf = pd.DataFrame(test_results)
        # Name the index column ID
        results_pdf.index.name = 'ID'
        # Add column avg_active_tasks
        results_pdf['avg_active_tasks'] = results_pdf['executorRunTime'] / results_pdf['elapsedTime']
        # add computed column elapsed time in seconds
        results_pdf['elapsed_time_seconds'] = results_pdf['elapsedTime'] / 1000
        # Removing the '.sql' suffix from the 'query' column
        results_pdf['query'] = results_pdf['query'].str.replace('.sql', '', regex=False)

        # Print the DataFrame to the specified file (default is stdout)
        if file_csv == sys.stdout:
            print("****************************************************************************************")
            print("Queries execution metrics")
            print("****************************************************************************************")
            print()
        results_pdf.to_csv(file_csv)
        self.results_pdf = results_pdf # save the results to the object

        # 3. Compute and print summary metrics values grouped by query
        grouped_results_pdf = (results_pdf.drop(columns=['query_rerun_id', 'run_id', 'avg_active_tasks', 'elapsed_time_seconds'])
                          .groupby('query')
                          .median()).astype(int)
        # Add the computer values for avg_active_tasks and elapsed_time_seconds columns
        grouped_results_pdf['avg_active_tasks'] = round(grouped_results_pdf['executorRunTime'] / grouped_results_pdf['elapsedTime'], 2)
        grouped_results_pdf['elapsed_time_seconds'] = round(grouped_results_pdf['elapsedTime'] / 1000, 2)
        self.grouped_results_pdf = grouped_results_pdf # save the grouped results to the object

        # Print the grouped result to the specified file (default is stdout)
        if file_grouped == sys.stdout:
            print()
            print("****************************************************************************************")
            print("Median metrics values grouped by query")
            print("****************************************************************************************")
            print()
        grouped_results_pdf.to_csv(file_grouped, index=True)

        # 3. Compute and print aggregated metrics values, cumulative over all queries
        aggregated_results_pdf = (results_pdf.drop(columns=['query_rerun_id', 'run_id', 'query', 'avg_active_tasks', 'elapsed_time_seconds'])
                        .sum())
        # Add the computer values for avg_active_tasks and elapsed_time_seconds columns
        aggregated_results_pdf['avg_active_tasks'] = round(aggregated_results_pdf['executorRunTime'] / aggregated_results_pdf['elapsedTime'], 2)
        aggregated_results_pdf['elapsed_time_seconds'] = round(aggregated_results_pdf['elapsedTime'] / 1000, 2)

        # Print the aggregated result to the specified file (default is stdout)
        # Transpose the result to have a single line with the aggregated values
        # Round off metrics to the nearest integer
        if file_grouped == sys.stdout:
            print("\n****************************************************************************************")
            print("Aggregated metrics values summed over all executions")
            print("****************************************************************************************")
            print()
        aggregated_results_pdf.astype(int).to_csv(file_aggregated, header=False)
        self.aggregated_results_pdf = aggregated_results_pdf.astype(int) # save the aggregated results to the object

    def save_with_spark(self, test_results, filename):
        """Save the test results to a file using Spark"""
        spark = self.spark
        # Create a DataFrame from the list of dictionaries
        df = spark.createDataFrame(test_results)
        # Save the DataFrame to a CSV file
        df.coalesce(1).write.option("header", "true").mode('overwrite').csv(filename)
