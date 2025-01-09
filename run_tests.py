import pytest
import sys

if __name__ == '__main__':
    # Add coverage reporting
    args = [
        '--cov=.',
        '--cov-report=html',
        '--cov-report=term-missing',
        '-v'
    ]
    
    # Add any additional arguments passed to the script
    args.extend(sys.argv[1:])
    
    # Run tests
    sys.exit(pytest.main(args))
