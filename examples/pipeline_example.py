#!/usr/bin/env python3
"""Pipeline example"""
from pyre import Scheduler
from pyre.pipeline import Pipeline

def extract_data(source):
    return {"data": [1, 2, 3, 4, 5]}

def transform_data(data, factor=2):
    return [x * factor for x in data["data"]]

def load_data(data):
    print(f"Loaded {len(data)} records")
    return data

def main():
    scheduler = Scheduler()
    
    pipeline = Pipeline("etl", scheduler)
    pipeline.add_stage("extract", extract_data)
    pipeline.add_stage("transform", transform_data, factor=3)
    pipeline.add_stage("load", load_data)
    
    result = pipeline.execute()
    print(f"Pipeline result: {result}")

if __name__ == "__main__":
    main()
