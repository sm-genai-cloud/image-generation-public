


# Compute cosine similarities between the stacked arrays and embeddings lists
def compute_cos_sim(embedding_list1, embedding_list2, metric="mean"):



def find_cos_sim(emb_list1, emb_list2, metric):
    


def check_value_in_dict(my_dict, value):
   
def process_text(text,nlp):
    

def style_provider_recos_fn(prompt_txt,styles_dict,providers_dict,embeddings_list,model,device):
    
def save_image_from_url(url, img_path, img_name):
    


# Function to split text into chunks
def split_into_chunks(input_list, max_seq_length, tokenizer):
    



def find_similar_rows(table_name, vector_column_name, vector_to_compare, threshold=0.9):
    


# Function to fetch image from S3
def get_image_from_s3(bucket_name, key, s3_client):
    
    



def get_embeddings(input_list, embed_model_type, normalize=False, precision="fp32", embedding_dim=1024, embedding_pre="fp32"):
    


def create_prompt_fn(config, prompt_txt, project_brief, negative_prompt, api_provider):
    


def rewrite_prompt_fn(config, orig_prompt_txt, asset_type, api_provider):
    

   


def moderate_prompt_fn(config, orig_prompt_txt, api_provider):
    

def prompt_tags_fn(config, prompt_txt, api_provider):
    
   


# Function to read data from S3
def get_data_from_s3(s3_client, bucket_name, data_key_s3):

   

# Function to encode the image
def encode_image_to_base64(image_path):
  
def create_style_prompt_from_img(images,api_key,asset_type,prompt,user_instructions=""):
   

def generate_openai_img(prompt, oai_client):
  
def generate_goog_img(prompt, goog_client):
   
    
    