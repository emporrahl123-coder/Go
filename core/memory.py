import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import pickle
import hashlib

class MemorySystem:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.memory_cache = {}
        
    def initialize(self):
        """Initialize memory system"""
        self.conn = sqlite3.connect('rahl_memory.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS context_memory (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                context_data TEXT,
                created TIMESTAMP,
                updated TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command_id TEXT,
                command TEXT,
                parameters TEXT,
                user_id TEXT,
                output TEXT,
                timestamp TIMESTAMP,
                compliance_score REAL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                preferences TEXT,
                created TIMESTAMP,
                updated TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def retrieve_context(self, context_id: str, user_id: str) -> Dict:
        """Retrieve context from memory"""
        self.cursor.execute(
            'SELECT context_data FROM context_memory WHERE id = ? AND user_id = ?',
            (context_id, user_id)
        )
        
        row = self.cursor.fetchone()
        if row:
            return json.loads(row[0])
        
        # Return empty context if not found
        return {
            "memory": [],
            "preferences": {},
            "created": datetime.utcnow().isoformat(),
            "updated": datetime.utcnow().isoformat()
        }
    
    def update_context(self, context_id: str, user_id: str, data: Dict):
        """Update context in memory"""
        existing = self.retrieve_context(context_id, user_id)
        
        # Merge data
        if "memory" in data and isinstance(data["memory"], list):
            existing["memory"].extend(data["memory"])
        
        if "preferences" in data and isinstance(data["preferences"], dict):
            existing["preferences"].update(data["preferences"])
        
        existing["updated"] = datetime.utcnow().isoformat()
        
        # Store in database
        self.cursor.execute(
            '''INSERT OR REPLACE INTO context_memory 
               (id, user_id, context_data, created, updated) 
               VALUES (?, ?, ?, ?, ?)''',
            (
                context_id,
                user_id,
                json.dumps(existing),
                existing.get("created", datetime.utcnow().isoformat()),
                existing["updated"]
            )
        )
        
        self.conn.commit()
    
    def clear_context(self, context_id: str, user_id: str):
        """Clear context from memory"""
        self.cursor.execute(
            'DELETE FROM context_memory WHERE id = ? AND user_id = ?',
            (context_id, user_id)
        )
        self.conn.commit()
    
    def store_execution(self, execution_record: Dict):
        """Store command execution record"""
        self.cursor.execute(
            '''INSERT INTO execution_log 
               (command_id, command, parameters, user_id, output, timestamp, compliance_score)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                execution_record["command_id"],
                execution_record["command"],
                json.dumps(execution_record["parameters"]),
                execution_record["user_id"],
                execution_record["output"],
                execution_record["timestamp"],
                1.0  # Always maximum compliance
            )
        )
        self.conn.commit()
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences"""
        self.cursor.execute(
            'SELECT preferences FROM user_preferences WHERE user_id = ?',
            (user_id,)
        )
        
        row = self.cursor.fetchone()
        if row:
            return json.loads(row[0])
        
        return {}
    
    def update_user_preferences(self, user_id: str, preferences: Dict):
        """Update user preferences"""
        existing = self.get_user_preferences(user_id)
        existing.update(preferences)
        
        now = datetime.utcnow().isoformat()
        self.cursor.execute(
            '''INSERT OR REPLACE INTO user_preferences 
               (user_id, preferences, created, updated)
               VALUES (?, ?, ?, ?)''',
            (
                user_id,
                json.dumps(existing),
                now,
                now
            )
        )
        self.conn.commit()
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        self.cursor.execute('SELECT COUNT(*) FROM context_memory')
        context_count = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM execution_log')
        execution_count = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM user_preferences')
        user_count = self.cursor.fetchone()[0]
        
        return {
            "contexts": context_count,
            "executions": execution_count,
            "users": user_count,
            "cache_size": len(self.memory_cache)
        }
    
    def persist(self):
        """Persist memory to disk"""
        self.conn.commit()
