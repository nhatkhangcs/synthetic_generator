from synthetic_generator.quick import fit

model = fit("student-mat.csv")
df2 = model.sample(5, seed=123)  # Generate just 5 rows for testing
print("Generated data shape:", df2.shape)
print("Columns:", df2.columns.tolist())
print("\nFirst few rows:")
print(df2.head())
print("\nData types:")
print(df2.dtypes)
