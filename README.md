# Basic Scraper

This is a basic scraper utility to extract title meta_description and content_length.

# How to Run

```
docker build -t scraper .
docker run scraper python scraper/scraper.py http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/
```

# Basic Architecture Diagram

[![Basic Architecture Diagram](https://lucid.app/publicSegments/view/5657f17a-81d6-4a41-b3e6-ad2ae4a2348a/image.jpeg)](https://lucid.app/)

- There could be multiple flaws in the diagram as this is based on certain assumptions and initial understanding
- Open to update as per the requirements

```
We wish to store the data in BigQuery. Provide design documentation and implementation for data injection when we collect billions rows of
data daily. Propose the next steps, how to further optimize for cost, reliability, performance, and scale. Provide design on storage schema.
Input:
List of billions of URLs send in via a text file, or streaming, or via sql statements
e.g. billions of URLs for amazon.com for July
Output: Design storage of the metadata and content. Design for data governance. Design for unified data schema. Design for disaster
recovery.
```

**1. Data Ingestion Strategy**

- Batch Ingestion: For data provided in text files, tools like Cloud Storage and Dataflow can be used to batch load data into BigQuery.
- Streaming Ingestion: For real-time data, Cloud Pub/Sub can be used for streaming data into BigQuery
- SQL Statements: BigQuery's support for SQL statements can be used for data insertion.

**2. Data Transformation and Preprocessing**
Before ingesting data into BigQuery, perform any necessary data transformation and preprocessing to ensure data quality, structure, and consistency. This step may involve data cleansing, normalization, and enrichment.

**3. Unified Data Schema:**

```json
{
  "url": STRING,
  "timestamp": TIMESTAMP,
  "metadata": STRUCT<...>,
  "content": STRING
}
```
This schema includes URL, timestamp, metadata, and content. You can adapt it based on your specific use case.
Note: This schema can be further optimized as per the query requirements

**4. Data Governance**

Implement data governance practices, including access control, data encryption, and auditing. Utilize BigQuery's built-in security features and IAM policies to control who can access the data and what they can do with it. BigQuery Views can also be used to allow limited read access on certain dataset.

**5. Disaster Recovery:**

Ensure data backup and disaster recovery capabilities by enabling BigQuery's table snapshots and export options. Consider using multi-regional storage for your Cloud Storage buckets to increase data resilience.

**6. Performance Optimization:**

To optimize performance:

   **6.1 Use Partitioned and Clustered Tables:**

      - Partitioned tables: Organize your data into date or timestamp-based partitions. This helps prune unnecessary data during query execution, reducing the amount of data scanned.
      - Clustered tables: Cluster your data by one or more columns that are frequently used in filtering or joining. Clustering improves query performance by physically organizing related data together.- Use appropriate indexing for metadata fields that are frequently queried.

   **6.2 Optimize Data Storage:**

      - Compress your data: Use appropriate compression codecs (e.g., Snappy or Zstandard) to reduce storage costs and improve query performance.
      - Use the appropriate data types: Choose the most efficient data types for your columns to minimize storage space.

   **6.3 Minimize Data Scanning:**

      - Use the WHERE clause: Apply filtering conditions in your queries to reduce the amount of data scanned. Use filters that leverage partitioning and clustering columns for maximum efficiency.
      - Use LIMIT and SAMPLE: Limit the number of rows returned in your queries to reduce data scanning for ad-hoc analysis.
      - Avoid using wildcards in SELECT statements: Select only the necessary columns instead of using wildcard SELECT *.

   **6.4 Optimize Aggregations:**

      - Use aggregation functions like SUM, COUNT, and AVG judiciously to aggregate data efficiently.
      - Combine multiple aggregations into a single query when possible to reduce the number of passes over the data.

   **6.5 Use Cached Results:**

      - Utilize query caching to avoid recomputing the same results if the underlying data hasn't changed.
      - Enable query results caching when applicable.

   **6.6 Monitor Query Performance:**

      - Use the Query History and Query Insights in the BigQuery Console to monitor query performance and identify slow-running queries.
      - Set up monitoring and alerting to detect and respond to performance issues.

   **6.7 Review Query Execution Plans:**

      - Use the EXPLAIN statement to understand the query execution plan and identify potential bottlenecks.
      - Modify queries based on the execution plan to optimize performance.

   **6.8 Optimize for Parallelism:**

      - Use appropriate table and query settings to control parallelism and resources allocated to queries, such as controlling the number of slots for a query.

   **6.9 Consider Data Modeling:**

      - Depending on your use case, consider using materialized views or summary tables to precompute and store frequently queried data.

**7. Cost Optimization:**

    To optimize costs:

    - Implement data lifecycle management policies to automatically delete or archive older data.
    - Use slot reservations for predictable workloads to reduce query costs.
    - Monitor and optimize storage costs by regularly reviewing and optimizing your data storage strategies.
**8. Scaling:**
    - Utilize BigQuery's automatic scaling for query processing.
    - Consider sharding or partitioning data to distribute the load evenly.
    - Continuously monitor system performance and scale resources as needed.
**9. Storage Schema:**

    - Use partitioned tables by date or another logical partition key to minimize query cost and improve performance.
    - Use clustered tables to group related data together, reducing the amount of data scanned during queries.
    - Use appropriate column data types to optimize storage size.
    - Leverage the native capabilities of BigQuery for handling nested and repeated fields as needed.
**10. Monitoring and Logging:**

    - Implement robust monitoring and logging to keep track of system health, data ingestion rates, query performance, and any potential issues. Utilize Google Cloud's monitoring and logging tools for this purpose.

```
Part 3:
Provide documentation on operationalize the query of billions of URLs using the service created on Part 2. Propose the next steps, how to
further optimize for cost, reliability, performance, and scale.
Input:
    A query to get metadata of a given URL
        e.g return the title of http://www.walmart.com
    A query to get list of URLs that matches metadata pattern
        e.g return URLs with title like ‘%xyz%’ or title = ‘.*xyz.*’
    A query to get related URLs for a given URL
        e.g. return URLs that’s similar to URL1
    A query to get historical info for a given URL
        e.g return size of content of a given URL over time
Output: BigQuery schema. Sample BigQuery Queries. Design data framework allow fast query performance. Optimize for cost. Design for
scale from 100 concurrent sessions to 50000 concurrent sessions. Evaluations of the design and alternatives. Define SLOs and SLAs.
Example of query performance
```

**3.1 BigQuery Schema for Metadata Storage:**

Before operationalizing queries, you need to define a schema that stores metadata for URLs. Below is a sample schema:

```json
{
  "url": STRING,
  "timestamp": TIMESTAMP,
  "title": STRING,
  "content_size": INT64,
  "other_metadata": STRUCT<...>
}
```
This schema includes URL, timestamp, title, content size, and other metadata fields. You can adapt it based on your specific metadata requirements.
This schema can be changed as per the requirements.

**3.2 Sample BigQuery Queries:**

Query to Get Metadata of a Given URL:

```sql
SELECT title, other_metadata
FROM your_dataset.your_table
WHERE url = 'http://www.walmart.com'
```
Query to Get URLs Matching Metadata Pattern:

```sql
SELECT url
FROM your_dataset.your_table
WHERE title LIKE '%xyz%' OR title = '.*xyz.*'
```

Query to Get Related URLs for a Given URL:

```sql
SELECT url
FROM your_dataset.your_table
WHERE LEVENSHTEIN(url, 'URL1') <= 0.2 * LENGTH('URL1')
```

Note: Similarity is a very open playground to work on, I used LEVENSHTEIN distance, but they are more possibilities here as per our requirement

Query to Get Historical Info for a Given URL:

```sql
SELECT timestamp, content_size
FROM your_dataset.your_table
WHERE url = 'http://www.walmart.com'
ORDER BY timestamp
```

**3.3. Design for Query Performance:**

    To achieve fast query performance:

    - Partition your BigQuery table by a date or timestamp field to reduce the amount of data scanned during queries.
    - Use clustered tables to group related data together and optimize query performance.
    - Create appropriate indexes on frequently queried fields like "title" for pattern matching queries.
    - Utilize materialized views for complex and often used queries to precompute results.
    - Use streaming ingestion for real-time updates to maintain up-to-date metadata.
**3.4. Cost Optimization:**
    To optimize costs:

    - Implement data lifecycle management policies to automatically delete or archive old data.
    - Monitor and optimize query costs by analyzing query execution plans and using query caching.
    - Consider using on-demand pricing for low-frequency queries and reserved capacity for high-frequency ones.
    - Use Batch query instead of Interactive in case you can wait for results or scheduled queries
**3.5. Design for Scale:**

    To handle a wide range of concurrent sessions:

    - Use BigQuery's automatic query scaling to handle increased query loads.
    - Consider load balancing query traffic if necessary.
    - Monitor query and system performance, and scale resources as needed.
    - Implement query prioritization to ensure critical queries are not affected by high concurrent loads.
**3.6. Service Level Objectives (SLOs) and Service Level Agreements (SLAs):**

    Define SLOs and SLAs to ensure system reliability and performance meet business requirements. For example:

    - SLO: 99% of queries for metadata retrieval must complete within 5 seconds.
    - SLA: Ensure system uptime of 99.9% with planned maintenance windows.

**3.7. Evaluation and Alternatives:**

    - Regularly evaluate the performance and cost-effectiveness of your system. Consider alternative solutions or optimizations when needed. Benchmark queries to assess their performance against SLOs.
    - Use Proper Alerting and monitoring to check if the SLO / SLA is not breached
