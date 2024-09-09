# Contribute to the development of anjana

If this library is being useful for your research and you want to contribute to its improvement, we are happy to receive your proposals! Below you will find a guide on how you can contribute to improving anjana.

### Add a new feature

If you are using anjana and have developed a new feature (especially implementing an additional anonymity functionality), and you want to contribute to the community, follow the steps below:
1. Fork the repository
2. Clone the local repository:
   
   ```bash
   git clone https://github.com/your-user/anjana.git

3. Set up a virtual environment and install the requirements:

    ```bash
    cd anjana
    virtualenv .venv -p python3
    source .venv/bin/activate
    pip install -e .

4. Create a new brach (e.g. develop)

     ```bash
     git checkout -b develop

5. Add the functionalities you want to contribute.
6. Include commits that are descriptive and clear about the changes made and functionality added. Make sure you create Semantic Commit Messages (conventional commits) including the use of flags such as `feat`, `fix`, `refactor`, `test`, etc
7. Check the style and that linting is successfully executed by using `tox`.
8. Check that the code coverage is greater than 90%:

     ```bash
     pytest --cov=.

9. Send your code to your fork:

    ```bash
    git push

10. Open a [pull request](https://github.com/IFCA-Advanced-Computing/anjana/pulls) from your fork.
    
### Solve a bug

If you have found a bug with some functionality of the library, it is recommended that you open an [issue](https://github.com/IFCA-Advanced-Computing/anjana/issues) so that we can solve it. You can follow the next steps: 
1. First, check that it is not an open [issue](https://github.com/IFCA-Advanced-Computing/anjana/issues) or one that has been previously resolved.
2. Give us information about the issue: clearly describe what you expected to receive and the error that occurred.
3. Describe clearly the steps that will allow us to reproduce your error, indicating the function you are using and details about the input introduced. 
4. Provide us details about the computing environment used: operating system, version of Python used and version of Anajan used.  

Any additional details you consider important will help us to resolve it more quickly.

### Suggest a new feature:

If you are missing some functionality that you would like to see implemented in anjana, you can request it by opening an [issue](https://github.com/IFCA-Advanced-Computing/anjana/issues) as indicated in the previous section.
1. check that this functionality is not included or has not been previously requested in another issue.
2. Give us information about the required functionality, including why it is important for the users to have it be available in anjana.
3. Include theoretical information about the new technique or feature requested, including papers supporting its usefulness.

   

