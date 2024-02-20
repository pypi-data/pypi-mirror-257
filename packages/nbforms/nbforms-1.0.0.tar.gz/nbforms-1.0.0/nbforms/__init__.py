"""nbforms: A Python library for interactive multi-user Jupyter notebook forms"""

import datascience as ds
import json
import os
import pandas as pd
import re
import requests

from dataclasses import dataclass
from getpass import getpass
from io import StringIO
from IPython.display import display
from ipywidgets import Button, VBox, interactive_output
from typing import Any, Dict, FrozenSet, List, Tuple, TYPE_CHECKING

from .widgets import TYPE_MAPPING
from .version import *

if TYPE_CHECKING:
  from ipywidgets import Output

  from .widgets import QuestionWidget


SERVER_URL_REGEX = re.compile(r"^https?://[\w\-.]+(?::\d+)?/?$")


@dataclass
class _Question:
  identifier: str
  """the question name"""

  widget: "QuestionWidget"
  """the widget to render for the question"""

  response: Any = None
  """the user's response"""

  updated_since_last_post: bool = False
  """whether the value of ``self.response`` has changed since the last time it was sent to the server"""


class Form:
  """
  A class for interacting with the nbforms server.

  The ``Form`` class sends requests to the nbforms server that records users' resposnes. It
  provides authentication so that users can be differentiated on the server, stores users'
  responses from widgets, generates and displays the necessary widgets, and pulls data from the
  server for analysis.

  Args:
    config_path (``str``): the path to an nbforms config file
  """

  _config: Dict
  """the parsed config file"""

  _server_url: str
  """the URL of the server instance"""

  _notebook: str
  """the notebook identifier"""

  _questions: List[_Question]
  """the question data"""

  _question_identifiers: FrozenSet[str]
  """all question identifiers from the config"""

  _api_key: str
  """the user's API key for the server instance"""

  def __init__(self, config_path: str = "nbforms_config.json"):
    # check that config_path exists
    if not (os.path.exists(config_path) and os.path.isfile(config_path)): 
      raise FileNotFoundError(f"Could not find config file: {config_path}")

    # load in config file
    with open(config_path) as f:
      self._config = json.load(f)

    # check that config file has required info
    for k in ["questions", "notebook"]:
      if k not in self._config:
        raise ValueError(f"Config file missing required key: {k}")

    if "server_url" in self._config:
      self._server_url = self._config["server_url"]
    else:
      self._server_url = input("Enter the server URL:")

    # check validity of server URL
    if not SERVER_URL_REGEX.match(self._server_url):
      raise ValueError(f"Invalid server URL; the server URL may contain only a protocol (http or https), a domain name, and a port")

    # remove trailing slash if present
    if self._server_url.endswith("/"):
      self._server_url = self._server_url[:-1]

    self._notebook = self._config["notebook"]

    questions = self._config["questions"]
    self._questions = []
    for i, q in enumerate(questions):
      for k in ["identifier", "type", "question"]:
        if k not in q:
          raise ValueError(f"Question at index {i} is missing required key '{k}'")

      if q["type"] not in TYPE_MAPPING:
        raise ValueError(f"Invalid question type: {q['type']}")

      widget = TYPE_MAPPING[q["type"]](q)
      self._questions.append(_Question(identifier=q["identifier"], widget=widget))

    self._question_identifiers = frozenset(q.identifier for q in self._questions)

    self._auth()

  def _get_url(self, path: str) -> str:
    return f"{self._server_url}{path}"

  def _auth(self):
    """
    Authenticate the user with the server instance and record their API key.

    Raises:
      ``ValueError``: if the authentication request returns a non-200 status code
    """
    auth_type = self._config.get("auth", "default")
    if auth_type not in {"default", "none"}:
      raise ValueError(f"Unsupported auth type: {auth_type}")

    if auth_type == "none":
      data = None

    else:
      print("Please enter a username and password for nbforms.")
      username = input("Username: ")
      password = getpass("Password: ")
      
      data = {
        "username": username,
        "password": password,
      }

    # auth to get API key
    res = requests.post(self._get_url("/auth"), json=data)

    # check that sign in was OK, store API key
    if res.status_code != 200:
      raise RuntimeError(f"Server returned error response during authentication: [{res.status_code}] {res.text}")

    self._api_key = res.text

  def _get_question(self, identifier: str) -> _Question:
    """
    Get the ``Question`` instance with the provided identifier.
    """
    for q in self._questions:
      if q.identifier == identifier:
        return q
    raise ValueError(f"No such question: {identifier}")

  def _save_current_response(self, identifier: str, response: Any):
    """
    Save a question response from a widget.
    """
    q = self._get_question(identifier)
    if q.response == response:
      return
    q.response = response
    q.updated_since_last_post = True

  def _send_responses(self):
    """
    Send all updated responses to the server.
    """
    responses: List[Dict[str, str]] = []
    updated: List[_Question] = []
    for q in self._questions:
      if q.updated_since_last_post:
        responses.append({"identifier": q.identifier, "response": q.response})
        updated.append(q)
    
    res = requests.post(self._get_url("/submit"), json = {
      "api_key": self._api_key,
      "notebook": self._notebook,
      "responses": responses,
    })

    if res.status_code != 200:
      raise RuntimeError(f"Submit request returned error response: [{res.status_code}] {res.text}")
    
    for q in updated:
      q.updated_since_last_post = False

  def _get_data(self, identifiers: List[str], user_hashes: bool = False):
    """
    Get question data from the server.
    """
    res = requests.get(self._get_url("/data"), json = {
      "questions": identifiers,
      "notebook": self._notebook,
      "user_hashes": user_hashes,
    })
    if res.status_code != 200:
      raise RuntimeError(f"Server data request returned error response: [{res.status_code}] {res.text}")
    return res.text

  def _create_submit_button(self) -> Button:
    """
    Create the submit button for a widget.
    """
    button = Button(description="Submit")

    # create the function that will be called when the button is clicked
    def send(b):
      self._send_responses()
      b.button_style = 'success'

    button.on_click(send)
    return button

  def _arrange_single_widget(self, q: _Question) -> Tuple[VBox, "Output"]:
    """
    Set up a single widget with its label.
    """
    label, widget = q.widget.to_widget_tuple(q.response)

    def do_update(response):
      if response:
        self._save_current_response(q.identifier, response)

    # set up the interactive part of the widget
    interactive = interactive_output(
      do_update,
      {"response": widget},
    )

    # create the UI with VBoxes and return the (UI, interactive) tuple
    ui = VBox([label, widget])
    return ui, interactive

  def ask(self, *identifiers: str):
    """
    Ask configured questions by dispalying widgets.
    
    Args:
      identifiers (``str``): question identifiers to be asked in the widget; if none are specified,
        defaults to all questions
    """
    questions = []
    for qi in identifiers:
      questions.append(self._get_question(qi))
    
    # default to asking all questions
    if len(questions) == 0:
      questions = list(self._questions)

    # capture all widgets in list of VBoxes
    displays = []
    for q in questions:
      displays += [VBox(self._arrange_single_widget(q))]

    # create submit button
    displays += [self._create_submit_button()]

    # create VBox to display
    t = VBox(displays)

    # display the widget
    display(t)

  def to_table(self, *identifiers: str, user_hashes: bool = False):
    """
    Get data from the server and return a datascience ``Table``.
    
    Args:
      identifiers (``str``): which questions to include in the table; if none are specified,
        defaults to all questions
      user_hashes (``bool``): whether to include hashes of usernames

    Returns:
      ``datascience.Table``: a table containing the data from the server
    """
    # get a pandas DataFrame and return that turned into a Table
    df = self.to_df(*identifiers, user_hashes=user_hashes)
    return ds.Table.from_df(df)

  def to_df(self, *identifiers, user_hashes=False):
    """
    Get data from the server and return a pandas ``DataFrame``.
    
    Args:
      identifiers (``str``): which questions to include in the table; if none are specified,
        defaults to all questions
      user_hashes (``bool``): whether to include hashes of usernames

    Returns:
      ``pandas.DataFrame``: a dataframe containing the data from the server

    Raises:
      ``ValueError``: if any of the question identifiers are not present in the config
    """
    # check that all identifiers are valid
    for i in identifiers:
      if i not in self._question_identifiers:
        raise ValueError(f"No such question: {i}")

    # default to getting all questions
    if len(identifiers) == 0:
      identifiers = sorted(self._question_identifiers)

    # send request to server and get the CSV string
    csv_string = self._get_data(identifiers, user_hashes=user_hashes)
  
    return pd.read_csv(StringIO(csv_string))

  def take_attendance(self):
    """
    Log attendance on the server instance.

    Raises:
      ``ValueError``: if this notebook is not configured to take attendance
    """
    if not self._config.get("attendance"):
      raise ValueError("This notebook does not record attendance")

    res = requests.post(self._get_url("/attendance"), json = {
      "api_key": self._api_key,
      "notebook": self._notebook,
    })

    if res.status_code != 200:
      raise RuntimeError(f"Server returned an error response while recording attendance: [{res.status_code}] {res.text}")

    print("Your attendance has been recorded.")
