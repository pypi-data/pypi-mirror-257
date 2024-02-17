import io
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from fastapi import FastAPI, Response

app = FastAPI()


def generate_balance_graph():
    # Connect to the SQLite database
    conn = sqlite3.connect("../cashu-testnut/data/mint/mint.sqlite3")

    # Load data from the tables
    df_promises = pd.read_sql_query("SELECT created, amount FROM promises", conn)
    df_proofs_used = pd.read_sql_query("SELECT created, amount FROM proofs_used", conn)

    # Convert 'created' columns from Unix timestamp to datetime
    df_promises["created"] = pd.to_datetime(df_promises["created"], unit="s")
    df_proofs_used["created"] = pd.to_datetime(df_proofs_used["created"], unit="s")

    # Resample and accumulate amounts over time for each table
    resample_period = "s"  # D = day, M = month, Y = year
    df_promises_accumulated = (
        df_promises.resample(resample_period, on="created").amount.sum().cumsum()
    )
    df_proofs_used_accumulated = (
        df_proofs_used.resample(resample_period, on="created").amount.sum().cumsum()
    )

    # Calculate the balance
    balance = df_promises_accumulated - df_proofs_used_accumulated

    # Plotting the balance over time
    plt.figure(figsize=(10, 6))
    balance.plot()
    plt.title("Balance Over Time (mint proofs - burn proofs)")
    plt.xlabel("Time")
    plt.ylabel("Accumulated Balance [sat]")
    plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Close the database connection
    conn.close()

    return buf


@app.get("/balance_graph")
async def balance_graph():
    buf = generate_balance_graph()
    return Response(content=buf.getvalue(), media_type="image/png")


# Run the application using a command like: uvicorn your_script_name:app --reload
