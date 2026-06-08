#!/usr/bin/env python3
"""Cron scheduler example"""
from pyre.cron import CronScheduler, CronSchedule

def cleanup_temp():
    print("Cleaning temp files...")

def backup_data():
    print("Backing up data...")

def main():
    cron = CronScheduler()
    
    cron.add_job("cleanup", cleanup_temp, 
                 CronSchedule(minute="0", hour="*/6"))
    
    cron.add_job("backup", backup_data,
                 CronSchedule(minute="0", hour="2"))
    
    print("Starting cron scheduler...")
    cron.start_all()

if __name__ == "__main__":
    main()
