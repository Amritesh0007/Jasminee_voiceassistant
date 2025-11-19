"""
Mathematics Module for Jasmine AI Assistant
Handles calculus, algebra, and higher-order mathematical operations
"""

import re
import sympy as sp
from sympy import symbols, diff, integrate, limit, series, solve, simplify
import numpy as np

def is_mathematical_query(query):
    """Check if a query is related to mathematics"""
    math_keywords = [
        'integrate', 'integration', 'integral', 'differentiate', 'derivative', 'differentiation',
        'calculus', 'limit', 'series', 'taylor', 'derivative of', 'integral of',
        'd/dx', '∫', 'lim', 'solve', 'equation', 'polynomial', 'function',
        'derivative', 'antiderivative', 'indefinite integral', 'definite integral',
        'partial derivative', 'multiple integral', 'differential equation'
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in math_keywords)

def extract_mathematical_expression(query):
    """Extract mathematical expression from query"""
    query_lower = query.lower().strip().rstrip('?').rstrip('.')
    
    # Handle "what is the derivative of ..." format
    if 'what is the derivative of' in query_lower:
        expr_start = query_lower.find('what is the derivative of') + len('what is the derivative of')
        expression = query[expr_start:].strip().rstrip('?').rstrip('.')
        # Remove "with respect to" part if it exists
        if 'with respect to' in expression.lower():
            with_respect_pos = expression.lower().find('with respect to')
            expression = expression[:with_respect_pos].strip()
        return expression
    
    # Handle "what is the integration of ..." format
    if 'what is the integration of' in query_lower or 'what is the integral of' in query_lower:
        if 'what is the integration of' in query_lower:
            expr_start = query_lower.find('what is the integration of') + len('what is the integration of')
        else:
            expr_start = query_lower.find('what is the integral of') + len('what is the integral of')
        expression = query[expr_start:].strip().rstrip('?').rstrip('.')
        return expression
    
    # Handle "integration of ..." format
    if 'integration of' in query_lower:
        expr_start = query_lower.find('integration of') + len('integration of')
        expression = query[expr_start:].strip().rstrip('?').rstrip('.')
        return expression
    
    # Handle "integral of ..." format
    if 'integral of' in query_lower:
        expr_start = query_lower.find('integral of') + len('integral of')
        expression = query[expr_start:].strip().rstrip('?').rstrip('.')
        return expression
    
    # Handle "differentiation of ... with respect to ..." format
    if 'differentiation of' in query_lower or 'differentiate' in query_lower:
        # Extract expression between "differentiat" and "with respect to"
        if 'with respect to' in query_lower:
            # Find the expression part
            if 'differentiation of' in query_lower:
                expr_start = query_lower.find('differentiation of') + len('differentiation of')
            else:  # 'differentiate'
                expr_start = query_lower.find('differentiate') + len('differentiate')
            
            expr_end = query_lower.find('with respect to')
            if expr_start < expr_end:
                expression = query[expr_start:expr_end].strip()
                # Remove trailing period if present
                expression = expression.rstrip('.')
                return expression
        else:
            # Simple differentiate format
            patterns = [
                r'differentiat.*?\s+(.+)',
                r'differentiate\s+(.+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, query_lower)
                if match:
                    return match.group(1).strip().rstrip('.')
    
    # Handle "integration of ... with respect to ..." format
    if 'integration of' in query_lower or 'integrate' in query_lower:
        if 'with respect to' in query_lower:
            if 'integration of' in query_lower:
                expr_start = query_lower.find('integration of') + len('integration of')
            else:  # 'integrate'
                expr_start = query_lower.find('integrate') + len('integrate')
            
            expr_end = query_lower.find('with respect to')
            if expr_start < expr_end:
                expression = query[expr_start:expr_end].strip()
                expression = expression.rstrip('.')
                return expression
        else:
            # Simple integrate format
            patterns = [
                r'integrat.*?\s+(.+)',
                r'integrate\s+(.+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, query_lower)
                if match:
                    return match.group(1).strip().rstrip('.')
    
    # Common patterns for mathematical expressions
    patterns = [
        r'integrate\s+(.+)',
        r'integral\s+of\s+(.+)',
        r'integral\s+(.+)',
        r'differentiate\s+(.+)',
        r'derivative\s+of\s+(.+)',
        r'derivative\s+(.+)',
        r'limit\s+of\s+(.+)',
        r'limit\s+(.+)',
        r'solve\s+(.+)',
        r'find\s+(.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query_lower)
        if match:
            result = match.group(1).strip().rstrip('.')
            # Remove "with respect to" part if it exists
            if 'with respect to' in result.lower():
                with_respect_pos = result.lower().find('with respect to')
                result = result[:with_respect_pos].strip()
            return result
    
    return query.strip().rstrip('.')

def parse_mathematical_expression(expression):
    """Parse and convert natural language math expressions to sympy format"""
    # Remove extra text like "with respect to x"
    expression = re.sub(r'\s+with\s+respect\s+to\s+.*$', '', expression, flags=re.IGNORECASE)
    
    # Replace common natural language terms with mathematical symbols
    expression = expression.replace('x squared', 'x**2')
    expression = expression.replace('x cube', 'x**3')
    expression = expression.replace('square of x', 'x**2')
    expression = expression.replace('cube of x', 'x**3')
    expression = expression.replace('^', '**')
    
    # Handle common functions
    expression = expression.replace('sin x', 'sin(x)')
    expression = expression.replace('cos x', 'cos(x)')
    expression = expression.replace('tan x', 'tan(x)')
    expression = expression.replace('log x', 'log(x)')
    expression = expression.replace('ln x', 'ln(x)')
    expression = expression.replace('e^x', 'exp(x)')
    
    # Fix spacing issues in expressions
    expression = re.sub(r'\s+', '', expression)
    
    # Fix multiplication issues (e.g., "5x" should be "5*x")
    expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
    
    return expression

def differentiate_expression(expression, variable='x', direct_answer=False):
    """Calculate the derivative of an expression"""
    try:
        x = symbols(variable)
        parsed_expr = parse_mathematical_expression(expression)
        expr = sp.sympify(parsed_expr)
        derivative = diff(expr, x)
        if direct_answer:
            return str(derivative)
        else:
            return f"The derivative of {expression.strip()} with respect to {variable} is: {derivative}"
    except Exception as e:
        return f"Error calculating derivative: {str(e)}"

def integrate_expression(expression, variable='x', definite=False, lower_bound=None, upper_bound=None, direct_answer=False):
    """Calculate the integral of an expression"""
    try:
        x = symbols(variable)
        parsed_expr = parse_mathematical_expression(expression)
        expr = sp.sympify(parsed_expr)
        
        if definite and lower_bound is not None and upper_bound is not None:
            integral = integrate(expr, (x, lower_bound, upper_bound))
            if direct_answer:
                return str(integral)
            else:
                return f"The definite integral of {expression.strip()} from {lower_bound} to {upper_bound} is: {integral}"
        else:
            integral = integrate(expr, x)
            if direct_answer:
                return str(integral) + " + C"
            else:
                return f"The indefinite integral of {expression.strip()} is: {integral} + C"
    except Exception as e:
        return f"Error calculating integral: {str(e)}"

def calculate_limit(expression, variable='x', point=0):
    """Calculate the limit of an expression"""
    try:
        x = symbols(variable)
        parsed_expr = parse_mathematical_expression(expression)
        expr = sp.sympify(parsed_expr)
        limit_result = limit(expr, x, point)
        return f"The limit of {expression.strip()} as {variable} approaches {point} is: {limit_result}"
    except Exception as e:
        return f"Error calculating limit: {str(e)}"

def solve_equation(expression):
    """Solve an equation"""
    try:
        x = symbols('x')
        parsed_expr = parse_mathematical_expression(expression)
        
        # Handle equations (expressions with equals)
        if '=' in parsed_expr:
            left, right = parsed_expr.split('=')
            equation = sp.sympify(left) - sp.sympify(right)
        else:
            equation = sp.sympify(parsed_expr)
            
        solutions = solve(equation, x)
        if len(solutions) == 1:
            return f"The solution is: x = {solutions[0]}"
        elif len(solutions) > 1:
            return f"The solutions are: x = {', x = '.join(map(str, solutions))}"
        else:
            return "No solutions found."
    except Exception as e:
        return f"Error solving equation: {str(e)}"

def process_mathematical_query(query, direct_answer=True):
    """Process mathematical queries and return appropriate responses"""
    query_lower = query.lower().strip().rstrip('?').rstrip('.')
    
    # Integration queries - expanded to include "integration"
    if any(word in query_lower for word in ['integrate', 'integral', 'integration']):
        expression = extract_mathematical_expression(query)
        # Check for definite integral
        if 'from' in query_lower and 'to' in query_lower:
            # Extract bounds (simplified approach)
            return integrate_expression(expression, definite=True, direct_answer=direct_answer)
        else:
            return integrate_expression(expression, direct_answer=direct_answer)
    
    # Differentiation queries - expanded to include "differentiation"
    elif any(word in query_lower for word in ['differentiate', 'derivative', 'differentiation']):
        expression = extract_mathematical_expression(query)
        # Extract variable if specified
        variable = 'x'  # default
        if 'with respect to' in query_lower:
            # Try to extract the variable
            match = re.search(r'with respect to\s+([a-zA-Z])', query_lower)
            if match:
                variable = match.group(1)
        return differentiate_expression(expression, variable, direct_answer=direct_answer)
    
    # Limit queries
    elif 'limit' in query_lower:
        expression = extract_mathematical_expression(query)
        # Extract point if specified
        return calculate_limit(expression)
    
    # Equation solving queries
    elif any(word in query_lower for word in ['solve', 'equation']):
        expression = extract_mathematical_expression(query)
        return solve_equation(expression)
    
    # Default mathematical processing
    else:
        expression = extract_mathematical_expression(query)
        # Try to determine what operation is needed based on context
        if 'derivative' in query_lower or 'differentiate' in query_lower or 'differentiation' in query_lower:
            variable = 'x'  # default
            if 'with respect to' in query_lower:
                match = re.search(r'with respect to\s+([a-zA-Z])', query_lower)
                if match:
                    variable = match.group(1)
            return differentiate_expression(expression, variable, direct_answer=direct_answer)
        elif 'integral' in query_lower or 'integrate' in query_lower or 'integration' in query_lower:
            return integrate_expression(expression, direct_answer=direct_answer)
        else:
            # Try to solve as equation
            return solve_equation(expression)

def MathematicsDecisionMaker(query):
    """
    Decision maker for mathematical queries
    Returns True if query should be handled by mathematics module
    """
    return is_mathematical_query(query)

if __name__ == "__main__":
    # Test the module
    test_queries = [
        "What is the derivative of x squared?",
        "Integrate x^2",
        "Find the integral of sin x",
        "What is the limit of 1/x as x approaches 0?",
        "Solve x^2 - 5x + 6 = 0",
        "Differentiate e^x"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        print(f"Result: {process_mathematical_query(query)}")
        print("-" * 50)