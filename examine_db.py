#!/usr/bin/env python3
"""
Script to examine the cfg_validator.db database structure and contents
"""
import os
import sqlite3
import json
from datetime import datetime

def examine_database():
    # Check multiple possible locations for the database
    possible_db_paths = [
        'cfg_validator.db',
        'backend/cfg_validator.db',
        'backend/instance/cfg_validator.db',
        'instance/cfg_validator.db'
    ]
    
    db_path = None
    for path in possible_db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ Database file 'cfg_validator.db' not found in any expected location.")
        print("Expected locations:")
        for path in possible_db_paths:
            print(f"  - {path}")
        print("\n🔧 The database is created automatically when the Flask app starts.")
        print("🚀 Start the backend server with: cd backend && python app.py")
        return
    
    print(f"✅ Found database at: {db_path}")
    print(f"📁 Database size: {os.path.getsize(db_path)} bytes")
    print()
    
    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        print("📊 DATABASE STRUCTURE")
        print("=" * 50)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ No tables found in database")
            return
        
        print(f"📋 Tables found: {len(tables)}")
        for table in tables:
            print(f"  • {table[0]}")
        print()
        
        # Examine each table
        for table_name, in tables:
            print(f"🔍 TABLE: {table_name}")
            print("-" * 30)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("📝 Schema:")
            for col in columns:
                col_id, name, data_type, not_null, default, primary_key = col
                pk_indicator = " (PK)" if primary_key else ""
                null_indicator = " NOT NULL" if not_null else ""
                default_indicator = f" DEFAULT {default}" if default else ""
                print(f"  {name}: {data_type}{pk_indicator}{null_indicator}{default_indicator}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            print(f"📊 Row count: {row_count}")
            
            # Show sample data if available
            if row_count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_rows = cursor.fetchall()
                print("📄 Sample data (first 3 rows):")
                
                column_names = [desc[0] for desc in cursor.description]
                for i, row in enumerate(sample_rows, 1):
                    print(f"  Row {i}:")
                    for col_name, value in zip(column_names, row):
                        # Format JSON fields nicely
                        if col_name in ['tokens', 'parse_trees', 'errors'] and value:
                            try:
                                parsed_json = json.loads(value)
                                value = json.dumps(parsed_json, indent=2)[:100] + "..." if len(str(value)) > 100 else json.dumps(parsed_json, indent=2)
                            except:
                                pass
                        # Truncate long values
                        if isinstance(value, str) and len(value) > 50:
                            value = value[:47] + "..."
                        print(f"    {col_name}: {value}")
            print()
        
        # Show analytics summary
        print("📈 ANALYTICS SUMMARY")
        print("=" * 50)
        
        # Request logs analysis
        cursor.execute("SELECT COUNT(*) FROM request_logs WHERE is_valid = 1")
        valid_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM request_logs WHERE is_valid = 0")
        invalid_count = cursor.fetchone()[0]
        
        total_requests = valid_count + invalid_count
        
        if total_requests > 0:
            success_rate = (valid_count / total_requests) * 100
            print(f"✅ Valid requests: {valid_count}")
            print(f"❌ Invalid requests: {invalid_count}")
            print(f"📊 Total requests: {total_requests}")
            print(f"📈 Success rate: {success_rate:.1f}%")
            
            # Most recent requests
            cursor.execute("SELECT request_line, is_valid, timestamp FROM request_logs ORDER BY timestamp DESC LIMIT 5")
            recent_requests = cursor.fetchall()
            if recent_requests:
                print("\n🕐 Recent requests:")
                for req_line, is_valid, timestamp in recent_requests:
                    status = "✅" if is_valid else "❌"
                    print(f"  {status} {req_line} ({timestamp})")
            
            # Common errors
            cursor.execute("""
                SELECT errors, COUNT(*) as count 
                FROM request_logs 
                WHERE is_valid = 0 AND errors IS NOT NULL 
                GROUP BY errors 
                ORDER BY count DESC 
                LIMIT 5
            """)
            error_patterns = cursor.fetchall()
            if error_patterns:
                print("\n🚨 Common error patterns:")
                for errors_json, count in error_patterns:
                    try:
                        errors = json.loads(errors_json)
                        print(f"  • {errors[0] if errors else 'Unknown error'} ({count} times)")
                    except:
                        print(f"  • Error parsing: {count} times")
            
        else:
            print("📝 No request logs found")
            print("💡 Send some requests to /api/validate to see data here")
        
        # Error patterns table
        cursor.execute("SELECT COUNT(*) FROM error_patterns")
        error_pattern_count = cursor.fetchone()[0]
        print(f"\n🔧 Error patterns defined: {error_pattern_count}")
        
        # User sessions
        cursor.execute("SELECT COUNT(*) FROM user_sessions")
        session_count = cursor.fetchone()[0]
        print(f"👥 User sessions: {session_count}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("🔍 CFG QODER DATABASE EXAMINER")
    print("=" * 50)
    print()
    examine_database()