# blackjack
blackjack server

# Test Case
    ## fix reference error
    ```python
        import sys
        import os

        # Add the parent directory (src) to the Python path
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
    ```

    ## output content even the test case success
        python -m pytest {file_name}.py -v -s