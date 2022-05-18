# 337---Project-1-Twitter



Github Repo: https://github.com/austin-py/337---Project-1-Twitter

Files to run: 
    - get_output.py is the only file necessary to generate output. It calls all of the helper functions we wrote and compiles them into a . This file could easily 
      be run from within the actual python file by modifying the input under the  "if __name__ == '__main__':" statement.  The default we have it set to is to run 
      save to json and save to text for both the 2013 and 2015 data.  We have the data housed in the '/data/' subdirectory and our code relies on this. 


    - Additionally, the file can be called from the command line after importing. 
    For example: 
        > python3 
        > import get_output.py as output
        > output.save_to_json('INPUT FILE') # This gives a json version of the output 
        > output.save_to_text('YEAR') # This gives a human-readable version of the output. 

    In this case input file needs to be a json object in the data folder. The output will appear in the data folder as the file name that was given plus "_answers.json". The year for save_to_text needs to correspond to a ggYEAR.json file in the data folder

   
    The output of get_output is found in the data subdirectory with the following file: 
        ggYEAR_answers.json for the data output
        ggYEAR_answers.txt for the text output 



Dependencies: 
    - We used a number of python packages within our code. These requirements can be found in requirements.txt and can 
    be installed using "pip3 install -r requirements.txt". On some systems this might just be "pip install -r 
    requirements.txt" but we found that for our laptops it was pip3. 
    - We were using the latest version of pip. 

    - One more requirement is to download "en_core_web_sm" which can be done with the command "python3 -m spacy download en_core_web_sm"(on mac) or "python -m spacy download en_core_web_sm"(on pc).  


Other info: 
    -  On top of the minimum requirements we also ran sentiment analysis on the tweets, and gathered twitter voted "best 
    dressed" and "worst dressed". This data can also be found in the human readable output file. 