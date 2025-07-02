import logging,openai,warnings
import os, sys, ast
import json
import pandas as pd
import numpy as np
import configparser
import re
from PIL import Image
from google import genai


# Suppress the specific FutureWarning
warnings.filterwarnings("ignore", message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.", category=FutureWarning)
warnings.filterwarnings("ignore", message="TypedStorage is deprecated.", category=UserWarning)


def model_fn(model_dir):
    
    logging.info("model_fn started, current working directory")
    logging.info(os.getcwd())

    sys.path.append(model_dir)
    
    import utils as myutil
    from config import OPENAI_API_KEY, GOOGLE_API_KEY

    # print("model_fn started, current working directory")
    
    try:
        config = configparser.ConfigParser()
        config.read(os.path.join(model_dir,'config.ini'))
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        
       
        oai_client = openai.OpenAI()
        goog_client = genai.Client()
        
        model_fn_tuple = (config, myutil, oai_client, OPENAI_API_KEY, goog_client, GOOGLE_API_KEY)
    
        logging.info("model_fn ended")
    
        return model_fn_tuple
    
    except Exception as e:
        logging.info(e)

        ## Debugging
        print("model_fn")
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, "Line number: ", exc_tb.tb_lineno)


