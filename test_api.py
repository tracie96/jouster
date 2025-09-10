#!/usr/bin/env python3
"""
Simple test script for the Jouster API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_analyze():
    """Test text analysis endpoint"""
    print("Testing analyze endpoint...")
    
    test_text = """
    Machine learning and artificial intelligence are transforming modern software development. 
    These technologies enable developers to build more intelligent applications that can 
    process natural language, recognize patterns, and make data-driven decisions. 
    The integration of AI into development workflows is creating new opportunities for 
    innovation while requiring developers to adapt to new tools and methodologies.
    """
    
    payload = {"text": test_text}
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    
    print(f"Analysis response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Summary: {result['summary']}")
        print(f"Title: {result['title']}")
        print(f"Topics: {result['topics']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Keywords: {result['keywords']}")
        return result['id']
    else:
        print(f"Error: {response.text}")
        return None
    print()

def test_search(analysis_id):
    """Test search endpoint"""
    print("Testing search endpoint...")
    
    # Search for "AI" topic
    response = requests.get(f"{BASE_URL}/search?topic=AI")
    print(f"Search response: {response.status_code}")
    if response.status_code == 200:
        results = response.json()
        print(f"Found {len(results)} results")
        for result in results:
            print(f"- ID: {result['id']}, Topics: {result['topics']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_empty_input():
    """Test edge case: empty input"""
    print("Testing empty input edge case...")
    payload = {"text": ""}
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    print(f"Empty input response: {response.status_code}")
    print(f"Error message: {response.json()}")
    print()

def test_get_all():
    """Test get all analyses endpoint"""
    print("Testing get all analyses...")
    response = requests.get(f"{BASE_URL}/analyses")
    print(f"Get all response: {response.status_code}")
    if response.status_code == 200:
        results = response.json()
        print(f"Total analyses: {len(results)}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("Starting Jouster API tests...")
    print("Make sure the API server is running on http://localhost:8000")
    print("=" * 50)
    
    try:
        test_health()
        analysis_id = test_analyze()
        if analysis_id:
            test_search(analysis_id)
        test_empty_input()
        test_get_all()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running with: python main.py")
    except Exception as e:
        print(f"Test error: {e}")
