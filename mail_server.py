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
        The save_mail method takes in list of dictionaries called mail

    Functionality:
        It seems like the code takes in the list of dictionaries and uses joinpath method to
        to create a file path with the present directory and the write_text is used to write 
        the list of dictionaries to a json file which json.dump() helps with by converting the 
        python objects in the list into json objects.

    Returns: 
        the function returns none which means nothing is returned
    """ 
    thisdir.joinpath('mail_db.json').write_text(json.dumps(mail, indent=4))

def add_mail(mail_entry: Dict[str, str]) -> str:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
     Parameters: 
        The add_mail method takes in a dictionary called mail_entry

    Functionality:
       It loads in the mail that is already on the json file and then adds the parameter,
       mail_entry by using append. Then it assigns a unique id for the mail entry and then 
       saves the list of mail back to the json file.

    Returns: 
        the function returns a string back which is a unique id for ther mail entry

    """
    mail = load_mail()
    mail.append(mail_entry)
    mail_entry['id'] = str(uuid.uuid4()) # generate a unique id for the mail entry
    save_mail(mail)
    return mail_entry['id']

def delete_mail(mail_id: str) -> bool:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
    Parameters: 
        The delete_mail function takes in a string called mail_id which is the unique id that
        each mail gets

    Functionality:
        The function takes in the mail id and checks if the pail id exists by going throigh 
        the entire list of the id. If the id is found, it deletes the mail of the list, and then
        saves the list back into the json file
    
    Returns: 
        returns true if mail was successfully deleted or false if it wasn't
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
        The function takes in the mail id and checks if the pail id exists by going throigh 
        the entire list of the id. If the id is found, it prints the mail that the id that 
        it corresponds with
    
    Returns: 
        The function returns an optional meaning that though it says it returns a dictionary,
        an optional allows None to be returned too
    """
    mail = load_mail()
    for entry in mail:
        if entry['id'] == mail_id:
            return entry

    return None

def get_inbox(recipient: str) -> List[Dict[str, str]]:
    """TODO: fill out this docstring (using the load_mail docstring as a guide)
    Parameters: 
        The get_inbox function takes in string called recipient 

    Functionality:
        The function loads in the mail from the json file and initalizes a list called inbox. Afterwards, it
        checks if the list from the json has the recipient that was given in the parameters and appends it to 
        the inbox list. Afterwards, it returns all the emails that have that specific recipient associated 
        to it
    
    Returns: 
        the function return a list of dictionarys which contain emails associated to the recipient
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
        The get_sent function takes in string called sender

    Functionality:
        The function loads in the mail from the json file and initalizes a list called sent. Afterwards, it
        checks if the list from the json has the specific sender that was given in the parameters and appends 
        it to the inbox list. Afterwards, it returns all the emails that have that specific sender associated 
        to it
    
    Returns: 
        the function return a list of dictionarys which contain emails associated to the sender
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