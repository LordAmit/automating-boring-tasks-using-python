import json
import requests
import pathlib

def process_request(project_id:str):
    base_url = "https://gitlab.com/api/v4/"
    user_id = "4539137"
    token_file = pathlib.Path.home() / "workspaces/python/gitlab_token"
    token = token_file.read_text()
    print(token)
    headers = {"header": "PRIVATE-TOKEN: {}".format(token)}
    print(headers)
    # response = requests.get(base_url+"projects/{}/issues".format(project_id), headers=headers)
    response = requests.get(
        base_url +
        # "users/{}/projects?custom_attributes[membership]=true&custom_attributes[owned]=false".format(
        "users/{}/projects?custom_attributes[visibility]='private'".format(
        user_id), headers=headers)

    if response.status_code is 200:
        parsed = json.loads(response.content.decode("utf-8"))
        print(json.dumps(parsed, indent=4, sort_keys=True))
    else:
        print("something broke")
        print(response)



if __name__ == '__main__':
    process_request("14442682")