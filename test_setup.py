#!/usr/bin/env python3
"""
Quick test script to verify your Groq + Supabase setup
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test if all required environment variables are set"""
    print("🧪 Testing Environment Configuration...")
    
    required_vars = {
        'LLM_PROVIDER': os.getenv('LLM_PROVIDER'),
        'LLM_API_KEY': os.getenv('LLM_API_KEY'),
        'LLM_BASE_URL': os.getenv('LLM_BASE_URL'),
        'LLM_CHOICE': os.getenv('LLM_CHOICE'),
        'DATABASE_URL': os.getenv('DATABASE_URL')
    }
    
    all_good = True
    for var, value in required_vars.items():
        if value:
            if 'API_KEY' in var:
                print(f"✅ {var}: {value[:10]}...")
            elif 'DATABASE_URL' in var:
                print(f"✅ {var}: postgresql://...")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set!")
            all_good = False
    
    return all_good

def test_groq_connection():
    """Test Groq API connection"""
    print("\n🚀 Testing Groq API Connection...")
    
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {os.getenv('LLM_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        # Simple test request to Groq
        with httpx.Client() as client:
            response = client.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                models = response.json()
                print(f"✅ Groq API connected! Available models: {len(models.get('data', []))}")
                return True
            else:
                print(f"❌ Groq API error: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Groq connection failed: {e}")
        return False

def test_google_embeddings():
    """Test Google Gemini embeddings API"""
    print("\n🔮 Testing Google Gemini Embeddings...")
    
    try:
        import httpx
        
        api_key = os.getenv('EMBEDDING_API_KEY')
        if not api_key:
            print("❌ No Google API key found")
            return False
        
        # Test embedding request
        url = f"https://generativelanguage.googleapis.com/v1/models/embedding-001:embedContent?key={api_key}"
        
        payload = {
            "content": {
                "parts": [{"text": "Hello world test"}]
            }
        }
        
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'embedding' in result:
                    embedding_size = len(result['embedding']['values'])
                    print(f"✅ Google Gemini embeddings working! Dimension: {embedding_size}")
                    return True
                else:
                    print(f"❌ Unexpected response format: {result}")
                    return False
            else:
                print(f"❌ Google API error: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Google embeddings test failed: {e}")
        return False

def test_database_connection():
    """Test Supabase database connection"""
    print("\n🗄️  Testing Supabase Database Connection...")
    
    try:
        import psycopg2
        
        # Test database connection
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Database connected! PostgreSQL version: {version[0][:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧠 MCP-Mem0 Setup Test\n" + "="*50)
    
    env_ok = test_environment()
    groq_ok = test_groq_connection()
    google_ok = test_google_embeddings()
    db_ok = test_database_connection()
    
    print("\n" + "="*50)
    if env_ok and groq_ok and google_ok and db_ok:
        print("🎉 ALL TESTS PASSED! Your setup is ready!")
        print("\nYour powerful combo:")
        print("⚡ Groq: Lightning-fast LLM inference")
        print("🔮 Google Gemini: State-of-the-art embeddings")
        print("🗄️  Supabase: Persistent vector storage")
        print("\nNext steps:")
        print("1. Run: uv run src/main.py")
        print("2. Connect Claude Desktop to: http://localhost:8050/sse")
    else:
        print("❌ Some tests failed. Check the errors above.")
        
        if not env_ok:
            print("- Fix your .env file configuration")
        if not groq_ok:
            print("- Check your Groq API key")
        if not google_ok:
            print("- Check your Google API key")
        if not db_ok:
            print("- Verify your Supabase connection string")