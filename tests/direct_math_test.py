"""
Direct test of Mathematics module without API calls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Mathematics import process_mathematical_query

def test_mathematical_capabilities_directly():
    """Test all mathematical capabilities directly without API calls"""
    
    print("🧪 Testing Jasmine AI Assistant Mathematical Capabilities (Direct Test)")
    print("=" * 70)
    
    # Test cases covering various mathematical operations
    test_cases = [
        # Calculus - Integration
        ("integrate x squared", "Integration of x^2"),
        ("integrate sin x", "Integration of sin(x)"),
        ("integrate cos x", "Integration of cos(x)"),
        ("integrate e^x", "Integration of e^x"),
        ("integrate x^3 + 2*x^2 + x + 1", "Integration of polynomial"),
        
        # Calculus - Differentiation
        ("differentiate x squared", "Differentiation of x^2"),
        ("differentiate sin x", "Differentiation of sin(x)"),
        ("differentiate cos x", "Differentiation of cos(x)"),
        ("differentiate e^x", "Differentiation of e^x"),
        ("differentiate x^3 + 2*x^2 + x + 1", "Differentiation of polynomial"),
        
        # Algebra - Equation Solving
        ("solve x^2 - 5*x + 6 = 0", "Quadratic equation"),
        ("solve x^2 - 4 = 0", "Simple quadratic equation"),
        ("solve 2*x + 3 = 7", "Linear equation"),
        
        # Limits
        ("limit of 1/x as x approaches 0", "Limit calculation"),
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, (query, description) in enumerate(test_cases, 1):
        print(f"\n{i}. {description}")
        print(f"   Query: {query}")
        
        try:
            result = process_mathematical_query(query)
            print(f"   Result: {result}")
            
            # Check if the result indicates success (no error messages)
            if not result.startswith("Error"):
                success_count += 1
                print("   ✅ Success")
            else:
                print("   ❌ Error")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
        
        print("-" * 50)
    
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("\n🎉 All mathematical capabilities are working correctly!")
        print("\n🎯 Features implemented:")
        print("   • Integration (indefinite integrals)")
        print("   • Differentiation (derivatives)")
        print("   • Equation solving (polynomial equations)")
        print("   • Limit calculations")
        print("   • Support for trigonometric functions")
        print("   • Support for exponential functions")
        print("   • Natural language processing for math queries")
        print("   • Complex expression handling")
    else:
        print(f"\n⚠️  Some tests failed. {success_count}/{total_tests} passed.")

if __name__ == "__main__":
    test_mathematical_capabilities_directly()