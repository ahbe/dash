import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(num_rows=5000):
    np.random.seed(42)
    
    # Dates for the past 12 weeks
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=12)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    brands = ["Brand A", "Brand B", "Brand C", "Brand D", "Brand E"]
    segments = ["Retail", "Corporate", "SME", "Institutional"]
    purposes = ["Home Loan", "Auto Loan", "Personal Loan", "Business Loan"]
    
    data = {
        "date": [pd.to_datetime(np.random.choice(dates)).strftime("%Y-%m-%d") for _ in range(num_rows)],
        "brand": [np.random.choice(brands) for _ in range(num_rows)],
        "segment": [np.random.choice(segments) for _ in range(num_rows)],
        "purpose": [np.random.choice(purposes) for _ in range(num_rows)],
        "derogation_flag": np.random.binomial(1, 0.15, num_rows),
        "derogation_bps": np.random.uniform(0, 500, num_rows),
        "usage_count": np.random.randint(1, 10, num_rows),
        "failed_calls": np.random.randint(0, 5, num_rows),
        "margin": np.random.uniform(50, 300, num_rows),
        "conversion_flag": np.random.binomial(1, 0.3, num_rows),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate converted_margin
    df["converted_margin"] = df["conversion_flag"] * df["margin"] * df["usage_count"]
    
    # Add derogation_pct column for callbacks
    df["derogation_pct"] = df["derogation_flag"] * 100
    
    df.to_csv("data/sample/sample_data.csv", index=False)
    print(f"Generated {num_rows} rows of sample data.")

if __name__ == "__main__":
    generate_sample_data()
