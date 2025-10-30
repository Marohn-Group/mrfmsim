Contribute
========================

We welcome contributions to mrfmsim! This guide will help you get started.

Getting Started
---------------

1. **Fork the Repository**
   
   Fork the mrfmsim repository on GitHub and clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/Marohn-Group/mrfmsim.git
      cd mrfmsim


2. **Create a Branch**
   
   Create a new branch for your feature or bug fix:

   .. code-block:: bash

      git checkout -b feature/your-branch-name

Development Guidelines
----------------------

Code Style
~~~~~~~~~~

- Follow PEP 8 style guidelines for Python code (use ``Black`` formatter's default settings)
- Use meaningful variable and function names
- Keep functions focused and modular
- Add type hints where appropriate

Documentation
~~~~~~~~~~~~~

- Write clear docstrings for all public classes, methods, and functions
- Use reStructuredText (reST) format for docstrings
- Refer to the `Sphinx docstring guide <https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html>`__ for detailed formatting information
- Include:
  
  - Brief description of what the function/class does
  - Parameter descriptions with types and units in **Sphinx** docstring format
  - Return value description
  - Usage examples where helpful
  - Mathematical formulas using Sphinx math directive when relevant

Example docstring format:

.. code-block:: python

   def example_method(x, y, z):
       r"""Calculate some property.

       Brief description of what this method does and any important
       details about the calculation or algorithm.

       :param float x: :math:`x` coordinate [nm]
       :param float y: :math:`y` coordinate [nm]
       :param float z: :math:`z` coordinate [nm]
       :return: calculated value
       :rtype: float
       """
       pass


Building Documentation
----------------------

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The built documentation will be in ``docs/_build/html/``.

Testing
~~~~~~~

- Write tests for all new features and bug fixes
- Tests should be fast and independent from one another
- Ensure all tests pass before submitting a pull request
- Aim for good test coverage of your code

Install test dependencies:

.. code-block:: bash

   pip install ".[test]"

Run tests with tox:

.. code-block:: bash

   tox

This will run tests across multiple Python environments and check code coverage.


Submitting a Pull Request
--------------------------

**Important**: Each pull request should focus on a single feature or bug fix. This makes the code easier to review, test, and maintain.

1. **Push to Your Fork**

   .. code-block:: bash

      git push origin feature/your-feature-name

2. **Create Pull Request**
   
   - Go to the mrfmsim repository on GitHub
   - Click "New Pull Request"
   - Select your fork and the ``develop`` branch as the base branch
   - Fill out the pull request template with:
     
     - Type of pull request (bug fix, feature, documentation, etc.)
     - Description of changes
     - Related issue numbers (if applicable)
     - Any breaking changes
     - Testing performed

3. **Review Process**
   
   - Maintainers will review your pull request
   - Address any feedback or requested changes
   - Once approved, your changes will be merged


Reporting Issues
----------------

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment (Python version, OS, etc.)
- Any relevant error messages or stack traces

Questions?
----------

If you have questions about contributing, feel free to:

- Open an issue on GitHub
- Check existing documentation
- Reach out to the maintainers

Thank you for contributing to mrfmsim!

