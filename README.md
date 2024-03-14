# Beno-t-Catez-MLOps

- Read the README in the Moodle in Best Practice section
- Initialize a GitHub/GitLab project named {Firstname Lastname MLOps}.
- Set up a pyenv with Python version 3.11.6
- Install Poetry along with required dependencies.
- Develop a data application using Streamlit to display various statitics and graphs based on the Housing.csv file.
- Create a Dockerfile that install dependencies and run the app.
- Write several Make commands :
    - prepare: Initialize the project with dependencies.
    - run: Run the data app
    - check: Verify formating of the python files with the commands:
        - vulture
        - isort
        - black
        - mypy
    - build: Build the docker image
- Add a prometheus client in the project with at least one counter that increment each time we push a specific button
- Create a deployment file for the app