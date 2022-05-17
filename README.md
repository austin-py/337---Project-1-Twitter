# 337---Project-1-Twitter



Github Repo: https://github.com/austin-py/337---Project-1-Twitter

Files to run: 
    - Output.py is the only file necessary to generate output. The file can be called from the command line after
    importing. For example: 
        > python3 
        > import get_output.py as output
        > output.save_to_json('INPUT FILE')
        > output.save_to_text('INPUT FILE')

    In this case input file needs to be a json object in the data folder. The output will appear in the data folder as the file name that was given plus "_answers.json". 

    Additionally, this file could easily be run from within the actual python file by modifying the input under the 
    "if __name__ == '__main__':" statement.  

Dependencies: 
    - We used a number of python packages within our code. These requirements can be found in requirements.txt and can be installed using "pip3 install -r requirements.txt". On some systems this might just be "pip install -r requirements.txt" but we found that for our laptops it was pip3. 
    - We were using the latest version of pip. 


Other info: 
    -  On top of the minimum requirements we also ran sentiment analysis on the tweets, and gathered twitter voted "best 
    dressed" and "worst dressed". This data can also be found in the human readable output file. 