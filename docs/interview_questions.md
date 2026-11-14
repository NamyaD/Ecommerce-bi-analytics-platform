# Interview questions and concise answers

1. **What is ETL?** Extract source data, transform it into trusted structures, then load a target system.
2. **Why separate extract and transform?** It isolates I/O from business rules and makes each stage testable.
3. **What is idempotency?** Re-running a process yields the same target state without duplicate effects; replace loads help in this batch demo.
4. **How are duplicates handled?** Detect exact duplicate rows, report counts, then retain one copy.
5. **How are orphan keys handled?** Check child foreign keys against parent IDs, report and reject invalid rows.
6. **Why Pandas?** It offers practical tabular transformations, validation and CSV/database interoperability.
7. **What is a DataFrame?** A labelled two-dimensional in-memory tabular data structure.
8. **What is a star schema?** A central fact table surrounded by descriptive dimensions.
9. **Fact vs dimension?** Facts record measurable events; dimensions describe who/what/when/where.
10. **Fact order-items grain?** One row per product line within an order.
11. **What is AOV?** Recognized revenue divided by the defined eligible order count.
12. **Why document KPI formulas?** It prevents teams from using inconsistent business definitions.
13. **What is a CTE?** A named temporary result set scoped to a SQL statement.
14. **What is a window function?** It calculates across related rows without collapsing them like GROUP BY.
15. **RANK vs DENSE_RANK?** RANK leaves gaps after ties; DENSE_RANK does not.
16. **What does LAG do?** Reads a prior row value within a window partition/order.
17. **INNER vs LEFT JOIN?** INNER keeps matches; LEFT preserves all left-side rows.
18. **What is HAVING?** Filters grouped results after aggregation.
19. **Why index a column?** It can accelerate lookups/joins at storage and write-maintenance cost.
20. **What is a primary key?** A unique, non-null row identifier.
21. **What is a foreign key?** A constraint linking a child reference to a parent key.
22. **SQLite vs PostgreSQL?** SQLite is embedded and simple; PostgreSQL is a concurrent client-server RDBMS with richer operational features.
23. **Why SQLAlchemy?** It provides a database abstraction and configurable connection URLs.
24. **What is data quality?** Fitness of data across validity, completeness, consistency, uniqueness and integrity.
25. **Why staging tables?** They preserve cleaned source-shaped data before curated warehouse consumption.
26. **What is Power BI?** A BI platform for data modelling, DAX measures, visual analytics and sharing.
27. **What is DAX?** An expression language for calculations in tabular semantic models.
28. **Measure vs calculated column?** A measure is evaluated in filter context; a column is stored per row at refresh.
29. **What is Welch's t-test?** A two-sample mean test that does not assume equal population variances.
30. **What does p-value mean?** Under H0, the probability of data at least as extreme as observed; it is not the probability H0 is true.
31. **Correlation vs causation?** Correlation measures association; it alone cannot establish cause.
32. **What is Pearson correlation?** A measure of linear association between two numeric variables.
33. **What is regression R²?** The fraction of target variance explained by the fitted model on evaluated data.
34. **What is MAE?** Mean absolute prediction error in target units.
35. **What is RMSE?** Square root of mean squared error, penalizing larger errors more.
36. **Why chronological forecasting split?** It avoids training on future observations when evaluating past periods.
37. **Why is linear trend limited?** It cannot represent complex seasonality, promotions or structural shifts without extra features.
38. **How scale this pipeline?** Partition/incremental ingestion, database-side transforms, orchestration and distributed compute when justified.
39. **How monitor a pipeline?** Track freshness, row counts, schema drift, quality failures, duration and load status.
40. **Why synthetic data?** It enables reproducible demos without exposing real customer information.
