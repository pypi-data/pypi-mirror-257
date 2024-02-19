
**Dependencies**
pandas: For data manipulation and preprocessing.
scikit-learn: For machine learning algorithms, metrics, and label encoding.
nltk: For tokenization and natural language processing tasks.
pickle: For saving and loading trained models.


**How to use this on ur local system**
Clone this repo from Github
Open the terminal and run the following commands 

--- You can run this file directly after installing all the required dependencies
            -> python3 /Users/ameybhat/PycharmProjects/MonocallsClassifier/MonocallsClassifier/hello.py
                    -> add the above file path according to your local system 
                    -> Also use the access key and secret key that can be found in the Security Credentials tab in the AWS DS account
--- If you want to make any changes then follow below steps:
    --- python3 setup.py sdist bdist_wheel 
    --- pip3 install dist/MonocallsClassifier-0.6-py3-none-any.whl  --force-reinstall
                -> use force reinstall if you have already installed this package and have made any changes in the main.py, __init__.py or setup.py
    --- python3 /Users/ameybhat/PycharmProjects/MonocallsClassifier/MonocallsClassifier/hello.py
                -> add the above file path according to your local system 
                -> Also use the access key and secret key that can be found in the Security Credentials tab in the AWS DS account
    --- If you have made any changes and want to re-run the package, run the same above commands
            after changing the version in setup.py file and also install according to the .whl file generated after these changes