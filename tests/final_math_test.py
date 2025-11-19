"""
Final comprehensive test for all mathematical query formats
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Model import FirstLayerDMM
from Backend.Mathematics import process_mathematical_query

def test_all_math_formats():
    """Test all mathematical query formats"""
    
    print("🧪 Final Comprehensive Mathematical Query Format Test")
    print("=" * 60)
    
    # Test various query formats that users might use
    test_queries = [
        # Traditional formats
        "integrate x squared",
        "differentiate x squared",
        "solve x^2 - 5*x + 6 = 0",
        
        # Natural language formats
        "What is the derivative of tan x?",
        "What is the integration of sin x?",
        "Differentiation of tan x with respect to x.",
        "Integration of cos x with respect to x",
        
        # Command formats
        "differentiate sin x with respect to x",
        "integrate cos x",
        
        # Question formats
        "what is the derivative of e^x?",
        "what is the integral of x^2?"
    ]
    
    success_count = 0
    total_tests = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        
        try:
            # Test decision making
            decision = FirstLayerDMM(query)
            print(f"   Decision: {decision}")
            
            # Process mathematical queries
            if any('mathematics' in d for d in decision):
                for d in decision:
                    if 'mathematics' in d:
                        math_query = d.replace('mathematics', '').strip()
                        result = process_mathematical_query(math_query)
                        print(f"   Result: {result}")
                        
                        # Check if successful (no error messages)
                        if not result.startswith("Error"):
                            success_count += 1
                            print("   ✅ Success")
                        else:
                            print("   ❌ Error")
            else:
                print("   ❌ Not recognized as mathematics query")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
        
        print("-" * 50)
    
    print(f"\n📊 Final Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("\n🎉 All mathematical query formats are working correctly!")
        print("\n🎯 Supported Query Formats:")
        print("   • integrate x squared")
        print("   • differentiate x squared") 
        print("   • solve x^2 - 5*x + 6 = 0")
        print("   • What is the derivative of tan x?")
        print("   • Differentiation of tan x with respect to x.")
        print("   • differentiate sin x with respect to x")
        print("   • And many more natural language formats!")
    else:
        print(f"\n⚠️  Some tests failed. {success_count}/{total_tests} passed.")

if __name__ == "__main__":
    test_all_math_formats()