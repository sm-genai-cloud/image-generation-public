from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import requests
import os, logging, sys
import inference as inf
import base64
import uuid

app = Flask(__name__)
STATIC_DIR = os.path.abspath("static")

@app.route('/')
def index():
    return render_template('index.html')

def load_model():
    model_fn_tuple = inf.model_fn("model_artifacts")
    return model_fn_tuple

with app.app_context():
    app.model = load_model()

@app.route('/generate_asset', methods=['POST'])
def generate_asset():
    logging.info("generate_asset fn")

    api_provider = "openai"

    try:
        model_fn_tuple = app.model
        local_assets = []
    
        config, myutil, oai_client, api_key, goog_client, goog_api_key = model_fn_tuple    
    
        prompt_txt = request.form.get('prompt')
        rewrite_prompt = request.form.get('rewrite_prompt')
        generation_type = request.form.get('generation_type')
        
        moderation = True
        user_instructions = ''
  

        # moderation_resp = 'bypass'

        if moderation:
            prompt_moderation = myutil.moderate_prompt_fn(config, prompt_txt, api_provider)
            if prompt_moderation['moderation'].lower() == "failure":
                prompt_txt = prompt_moderation['new_prompt']
                
        # print(prompt_txt)

        rewritten_prompt = ''
        if rewrite_prompt == 'on':
            rewritten_prompt = myutil.rewrite_prompt_fn(config, prompt_txt, generation_type, api_provider)['prompt']
            prompt_txt = rewritten_prompt

        # print(prompt_txt)
        
        image_source = request.form.get('image_source')
        image_urls = request.form.getlist('image_urls[]')
        image_files = request.files.getlist('image_files[]')
        predefined_style = request.form.get("predefined_style")

        # print(image_urls)

        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

        images = []
        if image_source == 'url' and image_urls:
            for image_url in image_urls:
                if image_url == '':
                    continue
                response = requests.get(image_url, headers=headers)
                if response.status_code == 200:
                    images.append(('url', image_url))
                else:
                    return jsonify({"error": f"Invalid image URL: {image_url}"}), 400
        
        elif image_source == 'upload' and image_files:
            for image_file in image_files:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                images.append(('base64', image_base64))

        elif image_source == 'prompt' or image_source == 'style_select':
            logging.info("No input images")
            
        
        else:
            return jsonify({"error": "Image URL or file is required"}), 400

  
        
        process_images(prompt_txt, user_instructions, images, generation_type, myutil, config, oai_client, api_key, goog_client, local_assets, image_source, predefined_style)
        
        return jsonify({"local_assets": local_assets,
                        "prompt_outputs": {"moderated_prompt": prompt_moderation['new_prompt'],
                                            "moderation_reason": prompt_moderation['reason'],
                                            "enhanced_prompt": rewritten_prompt
                                          }
                       })

    except Exception as e:
        logging.info(e)
        return jsonify({"error": "Internal Server Error"}), 500

        # ## Debugging
        # print("generate_asset fn exception")
        # print(e)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, "Line number: ", exc_tb.tb_lineno)

def process_images(prompt, user_instructions, images, generation_type, myutil, config, oai_client, api_key, goog_client, local_assets, image_source, predefined_style=''):

    if len(images) > 0:
        style_prompt = myutil.create_style_prompt_from_img(images, api_key, generation_type, prompt)

        text = style_prompt.lower()
        if ("sorry" in text and
                ("can't" in text or "cannot" in text) and
                ("assist" in text or "help" in text or "request" in text)):
            print(text)
            raise Exception(text)
        
        new_prompt = style_prompt.replace('<subject>', prompt)
    elif image_source == 'style_select' and predefined_style != '':
        new_prompt = prompt + f" in {predefined_style} style"
    else:
        new_prompt = prompt

    # print(new_prompt)
    asset_url = myutil.generate_openai_img(new_prompt, oai_client)
    # asset_img = myutil.generate_goog_img(new_prompt, goog_client)

    # img_path = f"static/generated_assets/"
    # img_name = f"{prompt.replace(' ','_')}_{uuid.uuid4().hex}.png"
    
    # myutil.save_image_from_url(asset_url, img_path, img_name)
    # img = Image.open(os.path.join(img_path, img_name))
    # img.thumbnail((512, 512))
    # img.save(os.path.join(img_path, "thumbnail_" + img_name))

    # if generation_type == 'icon':
    #     local_assets.append("thumbnail_" + img_name)
    # else:
    #     local_assets.append(img_name)

    local_assets.append(asset_url)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(STATIC_DIR, path)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
