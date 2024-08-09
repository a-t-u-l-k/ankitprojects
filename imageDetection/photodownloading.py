import requests
import os
import json
import time

API_KEYS_FILE = 'api_keys.json'

def load_api_keys():
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as file:
            data = json.load(file)
            if time.time() - data.get('timestamp', 0) < 86400:  # 24 hours
                return data.get('keys', {})
    return {}

def save_api_keys(api_keys):
    data = {'keys': api_keys, 'timestamp': time.time()}
    with open(API_KEYS_FILE, 'w') as file:
        json.dump(data, file)

def get_api_keys():
    api_keys = load_api_keys()
    
    if api_keys:
        use_stored_keys = input("\nStored API keys found. Do you want to use them? (yes/no): ").strip().lower()
        if use_stored_keys == 'yes':
            return api_keys
    
    unsplash_key = input("Enter your Unsplash API key (leave blank if not using): ")
    pixabay_key = input("Enter your Pixabay API key (leave blank if not using): ")
    pexels_key = input("Enter your Pexels API key (leave blank if not using): ")
    
    api_keys = {
        'unsplash': unsplash_key,
        'pixabay': pixabay_key,
        'pexels': pexels_key
    }
    
    save_api_keys(api_keys)
    
    return api_keys

def download_images(api_key, query, num_images, save_dir, api_name):
    headers = {'Authorization': f'Client-ID {api_key}'} if api_name == 'unsplash' else {'Authorization': api_key}
    urls = {
        'unsplash': f'https://api.unsplash.com/search/photos?query={query}&per_page={num_images}',
        'pixabay': f'https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&per_page={num_images}',
        'pexels': f'https://api.pexels.com/v1/search?query={query}&per_page={num_images}'
    }
    url = urls.get(api_name)
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP status
        data = response.json()
        if 'errors' in data:
            raise Exception("API Key might be invalid or expired.")
        
        # Check if the response is empty
        if not data or not data.get('results') and not data.get('hits') and not data.get('photos'):
            raise Exception(f"No data returned from {api_name} API.")
        
        os.makedirs(save_dir, exist_ok=True)
        
        for i, photo in enumerate(data.get('results', []) or data.get('hits', []) or data.get('photos', [])):
            img_url = photo['urls']['regular'] if api_name == 'unsplash' else photo['webformatURL'] if api_name == 'pixabay' else photo['src']['medium']
            img_data = requests.get(img_url).content
            with open(os.path.join(save_dir, f'image_{i+1}.jpg'), 'wb') as img_file:
                img_file.write(img_data)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching images from {api_name}: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    api_keys = get_api_keys()
    
    while True:
        print("\nStored API keys:")
        for api_name, key in api_keys.items():
            print(f"{api_name}: {'********' if key else 'Not provided'}")
        
        change_api = input("\nDo you want to change any API keys? (yes/no): ").strip().lower()
        if change_api == 'yes':
            unsplash_key = input("Enter your Unsplash API key (leave blank if not using): ")
            pixabay_key = input("Enter your Pixabay API key (leave blank if not using): ")
            pexels_key = input("Enter your Pexels API key (leave blank if not using): ")
            
            api_keys['unsplash'] = unsplash_key or api_keys.get('unsplash')
            api_keys['pixabay'] = pixabay_key or api_keys.get('pixabay')
            api_keys['pexels'] = pexels_key or api_keys.get('pexels')
            
            save_api_keys(api_keys)
        
        query = input("Enter the type of photos you would like to download (separated by spaces): ")
        save_dir = input("Enter the directory to save the images: ")
        
        categories = query.split()
        
        if len(categories) > 50:
            print("You can enter up to 50 categories. Only the first 50 will be processed.")
            categories = categories[:50]
        
        for i, category in enumerate(categories):
            num_images = int(input(f"Enter the number of images to download for category '{category}': "))
            category_dir = os.path.join(save_dir, f'category_{i+1}_{category.replace(" ", "_")}')
            print(f"Downloading images for category '{category}' (Category {i+1})...")
            for api_name, key in api_keys.items():
                if key:
                    download_images(key, category, num_images, category_dir, api_name)
        
        again = input("\nDo you want to download more images? (yes/no): ").strip().lower()
        if again != 'yes':
            break
    
    print("Download complete.")

if __name__ == "__main__":
    main()
