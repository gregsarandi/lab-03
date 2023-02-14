from typing import Dict, List, Optional
from flask import Flask, request, jsonify
import pathlib
import uuid
import json


app = Flask(__name__)
thisdir = pathlib.Path(__file__).parent.absolute() # path to directory of this file

# Function to load and save the mail to/from the json file

def load_mail() -> List[Dict[str, str]]:
    """
    Loads the mail from the json file

    Returns:
        list: A list of dictionaries representing the mail entries
    """
    try:
        return json.loads(thisdir.joinpath('mail_db.json').read_text())
    except FileNotFoundError:
        return []

def save_mail(mail: List[Dict[str, str]]) -> None:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
    
    Parameters: 
        save_mail() takes in a list of dictionaries called mail

    Functionality:
        This portion of code takes in the list of dictionaries and uses the joinpath method to
        to create a file path with the present directory. Then, the write_text method is called, which writes
        the list of dictionaries to a json file. Within the argument of write_text, json.dump() converts the 
        python objects in the list into json objects.

    Returns: 
        Since the function returns "None", nothing is returned by the function save_mail
    """ 
    thisdir.joinpath('mail_db.json').write_text(json.dumps(mail, indent=4))

def add_mail(mail_entry: Dict[str, str]) -> str:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
     Parameters: 
        The add_mail() method takes in a dictionary called mail_entry

    Functionality:
       add_mail first loads the mail that is already in the json file. Next, it adds that parameter 
       contained in "mail_entry" using the append method. It then assigned a unique id for the selected mail entry.
       Finally, it saved the list of mail into the json file.

    Returns: 
        The add_mail function returns a string serving as a unique id for the mail entry

    """
    mail = load_mail()
    mail.append(mail_entry)
    mail_entry['id'] = str(uuid.uuid4()) # generate a unique id for the mail entry
    save_mail(mail)
    return mail_entry['id']

def delete_mail(mail_id: str) -> bool:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
    Parameters: 
        The delete_mail function takes in a string called mail_id, which is the unique id associated with each separate piece of mail

    Functionality:
        The function takes in the unique id checks if the it exists within the mail_id list. If it does exist within mail_id,
        the function pops it from the stack, effectively deleting it. Then it saves the updated mail list using the save_mail() function.
        
    
    Returns: 
        Returns True if the mail_id did exist and has been removed from the mail() list, or False if the mail_id did not exist in the mail() list
    """
    mail = load_mail()
    for i, entry in enumerate(mail):
        if entry['id'] == mail_id:
            mail.pop(i)
            save_mail(mail)
            return True

    return False

def get_mail(mail_id: str) -> Optional[Dict[str, str]]:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
    Parameters: 
        The get_mail function takes in a string called mail_id which is the unique id that
        each mail gets

    Functionality:
        get_mail takes in a specific mail_id string and checks if said mail_id exists by going through the entire
        mail list. If the unique id is found in mail, the function prints the mail corresponding to the unique id.
    
    Returns: 
        The function returns an optional. Therefore, if the mail_id is found in the mail list, get_mail() will output the mail corresponding to that mail_id.
        If the mail_id is not found in the list, it will return None. 
    """
    mail = load_mail()
    for entry in mail:
        if entry['id'] == mail_id:
            return entry

    return None

def get_inbox(recipient: str) -> List[Dict[str, str]]:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
    Parameters: 
        The get_inbox function takes in a string initialized as "recipient"

    Functionality:
        First, the function loads in the mail from the json file using the load_mail() function. Then, a list called "inbox" is initialized. Next, the function
        checks if the list from the json file has has the recipient named in the parameters. If it does, the function appends it to 
        the inbox list. After this, the function returns all the emails tied to the specific recipient requested.
    
    Returns: 
        get_inox() return a list of dictionarys called "inbox", which contains all the emails sent to the user specified by the "recipient" string.
    """
    mail = load_mail()
    inbox = []
    for entry in mail:
        if entry['recipient'] == recipient:
            inbox.append(entry)

    return inbox

def get_sent(sender: str) -> List[Dict[str, str]]:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
    Parameters: 
        The get_sent function takes in a string initialized as "sender"

    Functionality:
        The get_sent() first loads in the mail list from the json file. Then, it initalizes a list called sent. Afterwards, it
        checks if the mail list has the sender specified in the parameters. If it does, it appends every mail entry sent by the specified sender
        to the inbox list. It then returns all the emails associated to that specific sender.
    
    Returns: 
        the get_sent() function returns a list of dictionarys containing all the emails previously sent by the specified sender
    """
    mail = load_mail()
    sent = []
    for entry in mail:
        if entry['sender'] == sender:
            sent.append(entry)

    return sent

# API routes - these are the endpoints that the client can use to interact with the server
@app.route('/mail', methods=['POST'])
def add_mail_route():
    """
    Summary: Adds a new mail entry to the json file

    Returns:
        str: The id of the new mail entry
    """
    mail_entry = request.get_json()
    mail_id = add_mail(mail_entry)
    res = jsonify({'id': mail_id})
    res.status_code = 201 # Status code for "created"
    return res

@app.route('/mail/<mail_id>', methods=['DELETE'])
def delete_mail_route(mail_id: str):
    """
    Summary: Deletes a mail entry from the json file

    Args:
        mail_id (str): The id of the mail entry to delete

    Returns:
        bool: True if the mail was deleted, False otherwise
    """
    # TODO: implement this function
    res = jsonify({'deleted': delete_mail(mail_id)})
    res.status_code = 200 # Status code for "ok"
    return res

@app.route('/mail/<mail_id>', methods=['GET'])
def get_mail_route(mail_id: str):
    """
    Summary: Gets a mail entry from the json file

    Args:
        mail_id (str): The id of the mail entry to get

    Returns:
        dict: A dictionary representing the mail entry if it exists, None otherwise
    """
    res = jsonify(get_mail(mail_id))
    res.status_code = 200 # Status code for "ok"
    return res

@app.route('/mail/inbox/<recipient>', methods=['GET'])
def get_inbox_route(recipient: str):
    """
    Summary: Gets all mail entries for a recipient from the json file

    Args:
        recipient (str): The recipient of the mail

    Returns:
        list: A list of dictionaries representing the mail entries
    """
    res = jsonify(get_inbox(recipient))
    res.status_code = 200
    return res

# TODO: implement a rout e to get all mail entries for a sender
# HINT: start with soemthing like this:
#   @app.route('/mail/sent/<sender>', ...)
@app.route('/mail/sent/<sender>', methods=['GET'])
def get_sent_route(sender: str):
    """
    Summary: Gets all mail entries for a sender from the json file

    Args:
        sender (str): The sender of the mail

    Returns:
        list: A list of dictionaries representing the mail entries
    """
    res = jsonify(get_sent(sender))
    res.status_code = 200
    return res

if __name__ == '__main__':
    app.run(port=5000, debug=True)