import requests
import click
import json
import os
import csv
from dotenv import load_dotenv


@click.command()
@click.argument("phone_num")
def lookup_num(phone_num):
    """This command takes in a phone and makes a validates it with the Bird API."""
    load_dotenv()
    api_key = os.environ.get("api_key")
    if api_key is None:
        print("""API Key doesn't exist. Create a .env with your key:\n
              echo \"api_key=\"<BIRD_API_KEY>\" > .env\"""")
        return

    header = {"Authorization" : f"AccessKey {api_key}"}
    try:
        res = requests.get(f"https://rest.messagebird.com/lookup/{phone_num}", headers=header) 
        match res.status_code:
            case 200:
                res_content = json.loads(res.content)
                print(f"Country code: {res_content['countryCode']}")
                print(f"Country prefix: {res_content['countryPrefix']}")
                print(f"Phone number as e164 format: {res_content['formats']['e164']}")
            case 403:
                res_cotent = json.loads(res.content)
                error = res_content["errors"][0]
                print(f"""Bird has responded that the API is not accessible:
                      Error code: {error['code']}
                      Description: {error['description']}""")
                return
            case 404:
                res_content = json.loads(res.content)
                error = res_content["errors"][0]
                print(f"""Bird API indicates the f{res.request.url} resource was not found:
                      Error code: {error['code']}
                      Description: {error['description']}""")
                return
            case 429:
                print("Server has rate limited your request, please try again.")
                return
            case _:
                print(f"Unhandled status code: {res.status_code}")
                res_content = json.loads(res.content)
                print(f"Response content is: {res_content}")
                return
        
    except requests.ConnectionError as e:
        print("Occams razor indicates it is probably DNS")
        print(f"Error is: {e}")

    except requests.RequestException as e:
        print("Requests has thrown a general request error.")
        print(f"Error is: {e}")

    except Exception as e:
        print(f"Unknown error: {e}")

@click.command()
@click.option("--id", prompt="Please enter space delimited album IDs")
def get_photos(id):
    """This command takes an ID and writes the associated files to present working directory."""
    try:
        ids = id.strip()
        ids = str.split(ids, sep=" ")
        ids = [int(id) for id in ids]
    except ValueError as e:
        print("Parsing the argument into an array failed, exiting.")
        return
    except Exception as e:
        print(e)

    photos = requests.get("https://jsonplaceholder.typicode.com/photos")
    albums = requests.get("https://jsonplaceholder.typicode.com/albums")

    photos = json.loads(photos.content)
    albums = json.loads(albums.content)

    rows = []
    for album in albums:
        if album['id'] in ids:
            dir_name = album['title'].replace(' ', '_')
            dir_name = f"{dir_name}_{album['id']}"
            try:
                if not os.path.exists(f"./{dir_name}"):
                    os.mkdir(f"./{dir_name}")
                dl_photo(album['id'], dir_name, photos, rows, album['title'])
            except Exception as e:
                print(e)

    with open("./photos.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['id', 'title', 'album_id', 'album_title', 'remote_path', 'local_path'])
        csvwriter.writerows(rows)


def dl_photo(album_id, target, photos, rows, album_title):
    for photo in photos:
        if photo['albumId'] == album_id:
            res = requests.get(photo['url'])
            file_name = photo['title'].replace(' ', '_')
            local_path = f"./{target}/{file_name}.png"
            with open(local_path, "ab") as file:
                      file.write(res.content)
            rows.append([ photo['id'], photo['title'], album_id, album_title, photo['url'], local_path ])
