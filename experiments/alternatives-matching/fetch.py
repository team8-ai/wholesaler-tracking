#!/usr/bin/env python3
"""
Script to fetch all unique samples from both wholesaler tracking tables:
1. wholesaler_tracking.parmed - based on description, manufacturer, strength, packQuantity
2. wholesaler_tracking.blupax - based on description, product_size, manufacturer_name, brand, strength, branding_type, generic_name

Saves results to two separate CSV files in the same directory as this script.
"""

import os
import sys
import csv
import dotenv
import psycopg2
from typing import List, Optional

dotenv.load_dotenv()


def fetch_unique_parmed_samples() -> Optional[List[tuple]]:
    """
    Fetch all unique samples from the wholesaler_tracking.parmed table
    based on description, manufacturer, strength, and packQuantity, with minimum price.
    
    Returns:
        List of unique tuples (description, manufacturer, brandName, strength, labelSize, packQuantity, min_price), or None if an error occurs.
    """
    # Get Postgres connection string from environment
    pg_conn_str = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not pg_conn_str:
        print("Error: POSTGRES_CONNECTION_STRING is not set in environment variables.")
        print("Please set this environment variable and try again.")
        return None
    
    # SQL query to fetch unique combinations with minimum price
    sql_query = """
    SELECT description, manufacturer, brandName, strength, labelSize, packQuantity, MIN(price) as min_price
    FROM wholesaler_tracking.parmed 
    WHERE description IS NOT NULL 
    AND description != '' 
    GROUP BY description, manufacturer, brandName, strength, labelSize, packQuantity
    ORDER BY description, manufacturer, brandName, strength, labelSize, packQuantity;
    """

    try:
        # Connect to database
        print("Connecting to database for parmed...")
        conn = psycopg2.connect(dsn=pg_conn_str)
        
        with conn:
            with conn.cursor() as cur:
                # Execute the query
                print("Executing query to fetch unique parmed samples...")
                cur.execute(sql_query)
                
                # Fetch all results
                results = cur.fetchall()
                
                # Return the tuples as-is (description, manufacturer, brandName, strength, labelSize, packQuantity)
                print(f"Found {len(results)} unique combinations.")
                return results

    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

def fetch_unique_blupax_samples() -> Optional[List[tuple]]:
    """
    Fetch all unique samples from the wholesaler_tracking.blupax table
    based on description, product_size, manufacturer_name, brand, strength, branding_type, generic_name, with minimum price.
    
    Returns:
        List of unique tuples (description, product_size, manufacturer_name, brand, strength, branding_type, generic_name, min_price), or None if an error occurs.
    """
    # Get Postgres connection string from environment
    pg_conn_str = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not pg_conn_str:
        print("Error: POSTGRES_CONNECTION_STRING is not set in environment variables.")
        print("Please set this environment variable and try again.")
        return None
    
    # SQL query to fetch unique combinations for blupax with minimum price
    sql_query = """
    SELECT description, product_size, manufacturer_name, brand, strength, branding_type, generic_name, MIN(unit_price) as min_price
    FROM wholesaler_tracking.blupax 
    WHERE description IS NOT NULL 
    AND description != '' 
    GROUP BY description, product_size, manufacturer_name, brand, strength, branding_type, generic_name
    ORDER BY description, product_size, manufacturer_name, brand, strength, branding_type, generic_name;
    """
    print(sql_query)
    try:
        # Connect to database
        print("Connecting to database for blupax...")
        conn = psycopg2.connect(dsn=pg_conn_str)
        
        with conn:
            with conn.cursor() as cur:
                # Execute the query
                print("Executing query to fetch unique blupax samples...")
                cur.execute(sql_query)
                
                # Fetch all results
                results = cur.fetchall()
                
                # Return the tuples as-is
                print(f"Found {len(results)} unique blupax combinations.")
                return results
                
    except psycopg2.Error as e:
        print(f"Database error occurred for blupax: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for blupax: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

def save_to_file(samples: List[tuple], filename: str, headers: List[str]) -> None:
    """
    Save the unique samples to a CSV file.
    
    Args:
        samples: List of unique tuples 
        filename: Output filename
        headers: List of column headers
    """
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(headers)
            
            # Write data rows
            for row in samples:
                writer.writerow(row)
                
        print(f"Results saved to '{filename}'")
    except Exception as e:
        print(f"Error saving to file: {e}")

def main():
    """Main function to run the script."""
    print("Fetching unique samples from both wholesaler tracking tables...")
    print("=" * 70)
    
    # Get script directory for file saving
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Fetch ParMed samples
    print("\n1. PARMED TABLE")
    print("Based on: description, manufacturer, strength, packQuantity")
    print("-" * 60)
    
    parmed_samples = fetch_unique_parmed_samples()
    
    if parmed_samples is None:
        print("Failed to fetch parmed samples.")
    else:
        print(f"Total unique parmed samples found: {len(parmed_samples)}")

        # Save parmed samples
        parmed_filename = os.path.join(script_dir, "unique_parmed_samples.csv")
        parmed_headers = ["Description", "Manufacturer", "Brand Name", "Strength", "Label Size", "Pack Quantity", "Min Price"]
        save_to_file(parmed_samples, parmed_filename, parmed_headers)
    
    # Fetch BluPax samples
    print("\n2. BLUPAX TABLE")
    print("Based on: description, product_size, manufacturer_name, brand, strength, branding_type, generic_name")
    print("-" * 90)
    
    blupax_samples = fetch_unique_blupax_samples()
    
    if blupax_samples is None:
        print("Failed to fetch blupax samples.")
    else:
        print(f"Total unique blupax samples found: {len(blupax_samples)}")
        
        # Save blupax samples
        blupax_filename = os.path.join(script_dir, "unique_blupax_samples.csv")
        blupax_headers = ["Description", "Product Size", "Manufacturer Name", "Brand", "Strength", "Branding Type", "Generic Name", "Min Price"]
        save_to_file(blupax_samples, blupax_filename, blupax_headers)
    
    print("\n" + "=" * 70)
    print("Script completed!")
    
    # Show summary
    if parmed_samples is not None and blupax_samples is not None:
        print(f"Summary: {len(parmed_samples)} parmed samples, {len(blupax_samples)} blupax samples")
    elif parmed_samples is not None:
        print(f"Summary: {len(parmed_samples)} parmed samples (blupax failed)")
    elif blupax_samples is not None:
        print(f"Summary: {len(blupax_samples)} blupax samples (parmed failed)")
    else:
        print("Summary: Both tables failed to fetch")


if __name__ == "__main__":
    main()
