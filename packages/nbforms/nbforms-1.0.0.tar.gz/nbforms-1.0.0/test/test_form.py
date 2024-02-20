"""Tests for ``nbforms.Form``"""

from contextlib import contextmanager
import json
import os
import pytest
import responses
import tempfile

from contextlib import nullcontext
from ipywidgets import Button, Label, Output, RadioButtons, SelectMultiple, Text, Textarea, VBox
from responses import matchers
from unittest import mock

from nbforms import Form


NOTEBOOK = "nb1"
SERVER_URL = "http://127.0.0.1:5000"

make_url = lambda path: f"{SERVER_URL}{path}"


@contextmanager
def make_form(config):
  """
  A context manager that provides a ``Form`` initialized with the provided config. It also stubs
  out ``nbforms.input`` and ``nbforms.getpass`` so that they return predetermined values.
  """
  def fake_input(prompt):
    if "server url" in prompt.lower():
      return "http://myserver.com"
    else:
      return "user1"

  with mock.patch("nbforms.input") as mocked_input, \
      mock.patch("nbforms.getpass") as mocked_getpass:
    mocked_input.side_effect = fake_input
    mocked_getpass.return_value = "pass1"

    fh, fp = tempfile.mkstemp()
    with open(fp, "w") as f:
      json.dump(config, f)

    yield Form(fp)

  os.close(fh)
  os.remove(fp)


class TestInit:
  """Tests for the ``Form`` constructor."""

  def test_invalid_config_path(self):
    fh, fp = tempfile.mkstemp()
    os.close(fh)
    os.remove(fp)

    # sanity check that the file was deleted
    assert not os.path.exists(fp)

    with pytest.raises(FileNotFoundError, match=f"Could not find config file: {fp}"):
      Form(fp)

  def make_test(config, want_error=None):
    """
    Create a test function that uses the provided config. If the constructor should error, set
    ``want_error`` to a non-null error.
    """
    def do_test(self):
      cm = nullcontext()
      if want_error is not None:
        cm = pytest.raises(type(want_error), match=str(want_error))

      with cm:
        with make_form(config):
          pass

    return do_test

  test_no_questions = make_test(
    {"server_url": SERVER_URL},
    want_error=ValueError("Config file missing required key: questions"),
  )

  test_no_notebook = make_test(
    {"server_url": SERVER_URL, "questions": []},
    want_error=ValueError("Config file missing required key: notebook"),
  )

  test_no_question_identifier = make_test(
    {"server_url": SERVER_URL, "notebook": "", "questions": [
      {},
    ]},
    want_error=ValueError("Question at index 0 is missing required key 'identifier'"),
  )

  test_no_question_type = make_test(
    {"server_url": SERVER_URL, "notebook": "", "questions": [
      {"identifier": "q1"},
    ]},
    want_error=ValueError("Question at index 0 is missing required key 'type'"),
  )

  test_invalid_question_type = make_test(
    {"server_url": SERVER_URL, "notebook": "", "questions": [
      {"identifier": "q1", "type": "foo", "question": ""},
    ]},
    want_error=ValueError("Invalid question type: foo"),
  )

  test_no_question_question = make_test(
    {"server_url": SERVER_URL, "notebook": "", "questions": [
      {"identifier": "q1", "type": "multiplechoice"},
    ]},
    want_error=ValueError("Question at index 0 is missing required key 'question'"),
  )

  @pytest.mark.parametrize(("auth", "make_res"), (
    (None, lambda: responses.post(
      url = make_url("/auth"),
      body = "deadbeef",
      match=[matchers.json_params_matcher({"username": "user1", "password": "pass1"})],
    )),
    ("default", lambda: responses.post(
      url = make_url("/auth"),
      body = "deadbeef",
      match=[matchers.json_params_matcher({"username": "user1", "password": "pass1"})],
    )),
    ("none", lambda: responses.post(
      url = make_url("/auth"),
      body = "deadbeef",
    )),
  ))
  @responses.activate
  def test_auth(self, auth, make_res):
    """Test user authentication in ``Form`` constructor."""
    make_res()

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "A, B, or C?",
        }
      ]
    }

    if auth:
      config["auth"] = auth

    with make_form(config) as form:
      assert form._api_key == "deadbeef"

  def test_invalid_auth_type(self):
    """Test invalid auth type handling in ``Form`` constructor."""
    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "auth": "foobar",
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "A, B, or C?",
        }
      ]
    }

    with pytest.raises(ValueError, match="Unsupported auth type: foobar"), make_form(config):
      pass

  @responses.activate
  def test_auth_http_error(self):
    """Test authentication HTTP error response handling in ``Form`` constructor."""
    responses.post(
      url = make_url("/auth"),
      body = "doh!",
      status = 400,
      match=[matchers.json_params_matcher({"username": "user1", "password": "pass1"})],
    )

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "A, B, or C?",
        }
      ]
    }

    with pytest.raises(RuntimeError, match="Server returned error response during authentication: \\[400\\] doh!"), \
        make_form(config):
      pass

  @responses.activate
  def test_no_server_url(self):
    """Test authentication HTTP error response handling in ``Form`` constructor."""
    responses.post(
      url = "http://myserver.com/auth",
      body = "deadbeef",
      match=[matchers.json_params_matcher({"username": "user1", "password": "pass1"})],
    )

    config = {
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "A, B, or C?",
        }
      ]
    }

    with make_form(config) as form:
      assert form._api_key == "deadbeef"

  invalid_url_error = ValueError("Invalid server URL; the server URL may contain only a protocol \\(http or https\\), a domain name, and a port")

  @pytest.mark.parametrize(("server_url", "want_auth_domain", "want_error"), (
    ("http://myapp.com", "http://myapp.com", None),
    ("http://myapp.com/", "http://myapp.com", None),
    ("https://myapp.com/", "https://myapp.com", None),
    ("https://127.0.0.1:5000", "https://127.0.0.1:5000", None),
    ("http://127.0.0.1:5000/", "http://127.0.0.1:5000", None),
    ("http://myapp.com/foo", None, invalid_url_error),
    ("file:///some/path", None, invalid_url_error),
    ("notaurl", None, invalid_url_error),
  ))
  @responses.activate
  def test_server_url_validation(self, server_url, want_auth_domain, want_error):
    """Test server URL validation in the ``Form`` constructor."""
    if want_auth_domain is not None:
      responses.post(
        url = f"{want_auth_domain}/auth",
        body = "deadbeef",
        match=[matchers.json_params_matcher({"username": "user1", "password": "pass1"})],
      )

    config = {
      "server_url": server_url,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "A, B, or C?",
        }
      ]
    }

    cm = nullcontext()
    if want_error is not None:
      cm = pytest.raises(type(want_error), match=str(want_error))

    with cm, make_form(config):
      pass

  @pytest.mark.parametrize(("identifiers", "want_widgets"), (
    (("q1", "q2"), [
      {
        "label": "A, B, or C?",
        "widget": RadioButtons,
        "options": ("A", "B", "C"),
      },
      {
        "label": "A, B, or C?",
        "widget": SelectMultiple,
        "options": ("A", "B", "C"),
      },
    ]),
    (("q3",), [
      {
        "label": "A, B, or C?",
        "widget": Text,
      },
    ]),
    (("q4", "q5", "q6"), [
      {
        "label": "A, B, or C?",
        "widget": Text,
        "placeholder": "Enter A, B, or C here",
      },
      {
        "label": "A, B, or C?",
        "widget": Textarea,
      },
      {
        "label": "A, B, or C?",
        "widget": Textarea,
        "placeholder": "Enter A, B, or C here",
      },
    ]),
    # check that entering no identifiers renders all questions.
    (tuple(), [
      {
        "label": "A, B, or C?",
        "widget": RadioButtons,
        "options": ("A", "B", "C"),
      },
      {
        "label": "A, B, or C?",
        "widget": SelectMultiple,
        "options": ("A", "B", "C"),
      },
      {
        "label": "A, B, or C?",
        "widget": Text,
      },
      {
        "label": "A, B, or C?",
        "widget": Text,
        "placeholder": "Enter A, B, or C here",
      },
      {
        "label": "A, B, or C?",
        "widget": Textarea,
      },
      {
        "label": "A, B, or C?",
        "widget": Textarea,
        "placeholder": "Enter A, B, or C here",
      },
    ]),
  ))
  @responses.activate
  @mock.patch("nbforms.display")
  def test_ask(self, mocked_display, identifiers, want_widgets):
    """
    Test ``Form.ask``.
    """
    responses.post(url=make_url("/auth"))

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
        {
          "identifier": "q2",
          "type": "checkbox",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
        {
          "identifier": "q3",
          "type": "text",
          "question": "A, B, or C?",
        },
        {
          "identifier": "q4",
          "type": "text",
          "question": "A, B, or C?",
          "placeholder": "Enter A, B, or C here",
        },
        {
          "identifier": "q5",
          "type": "paragraph",
          "question": "A, B, or C?",
        },
        {
          "identifier": "q6",
          "type": "paragraph",
          "question": "A, B, or C?",
          "placeholder": "Enter A, B, or C here",
        },
      ],
    }

    with make_form(config) as form:
      form.ask(*identifiers)

    mocked_display.assert_called_once()

    # check the rendered widget tree
    vbox = mocked_display.call_args.args[0]
    assert isinstance(vbox, VBox)
    assert len(vbox.children) == len(want_widgets) + 1
    
    for c, w in zip(vbox.children[:-1], want_widgets):
      assert isinstance(c, VBox)
      assert len(c.children) == 2
      assert isinstance(c.children[0], VBox)
      assert isinstance(c.children[1], Output)

      assert len(c.children[0].children) == 2
      label, widget = c.children[0].children
      assert isinstance(label, Label)
      assert label.value == w["label"]
      assert isinstance(widget, w["widget"])
      if "options" in w:
        assert widget.options == w["options"]
      else:
        assert widget.placeholder == w.get("placeholder", "Type something")

    # check submit button
    assert isinstance(vbox.children[-1], Button)
    assert vbox.children[-1].description == "Submit"

  @responses.activate
  @mock.patch("nbforms.display")
  def test_ask_widget_initial_value(self, mocked_display):
    """
    Test that ``Form.ask`` sets the initial value of its widgets to the user's last recorded
    response.
    """
    responses.post(url=make_url("/auth"))

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
        {
          "identifier": "q2",
          "type": "checkbox",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
        {
          "identifier": "q3",
          "type": "text",
          "question": "A, B, or C?",
        },
        {
          "identifier": "q5",
          "type": "paragraph",
          "question": "A, B, or C?",
        },
      ],
    }

    with make_form(config) as form:
      form._questions[0].response = "A"
      form._questions[1].response = ("B",)
      form._questions[2].response = "C"
      form._questions[3].response = "D"

      form.ask()

    mocked_display.assert_called_once()
    vbox = mocked_display.call_args.args[0]
    widgets = [c.children[0].children[1] for c in vbox.children[:-1]]
    for w, want in zip(widgets, ["A", ("B",), "C", "D"]):
      assert w.value == want, f"wrong value for widget {w}"

  @responses.activate
  @mock.patch("nbforms.display")
  def test_submit(self, mocked_display):
    """
    Test that submit button submits responses to the server.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")
    responses.post(
      url = make_url("/submit"),
      match = [matchers.json_params_matcher({
        "api_key": "deadbeef",
        "notebook": NOTEBOOK,
        "responses": [
          {
            "identifier": "q1",
            "response": "B",
          },
          {
            "identifier": "q2",
            "response": ["A", "C"],
          },
          {
            "identifier": "q3",
            "response": "A and B",
          },
        ],
      })]
    )
    responses.post(
      url = make_url("/submit"),
      match = [matchers.json_params_matcher({
        "api_key": "deadbeef",
        "notebook": NOTEBOOK,
        "responses": [
          {
            "identifier": "q1",
            "response": "C",
          },
          {
            "identifier": "q4",
            "response": "none of the above",
          },
        ],
      })]
    )

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
        {
          "identifier": "q2",
          "type": "checkbox",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
        {
          "identifier": "q3",
          "type": "text",
          "question": "A, B, or C?",
        },
        {
          "identifier": "q4",
          "type": "paragraph",
          "question": "A, B, or C?",
        },
      ],
    }

    with make_form(config) as form:
      form.ask()

      # updating the value fields of the widget instances simulates the user interacting with the
      # widget
      mocked_display.assert_called_once()
      vbox = mocked_display.call_args.args[0]
      widgets = [c.children[0].children[1] for c in vbox.children[:-1]]
      widgets[0].value = "B"
      widgets[1].value = ("A", "C")
      widgets[2].value = "A and B"

      button = vbox.children[-1]
      assert button.button_style != "success"

      button.click()

      assert button.button_style == "success"

      # check that only updated responses are sent in subsequent requests, and that that state is
      # persisted between calls for ``Form.ask``
      form.ask()

      vbox = mocked_display.call_args.args[0]
      widgets = [c.children[0].children[1] for c in vbox.children[:-1]]
      widgets[0].value = "C"
      widgets[3].value = "none of the above"

      button = vbox.children[-1]
      assert button.button_style != "success"

      button.click()

      assert button.button_style == "success"

  @responses.activate
  @mock.patch("nbforms.display")
  def test_submit_error(self, mocked_display, caplog):
    """
    Test how the submit button handler responds to an HTTP error response from the server.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")
    responses.post(
      url = make_url("/submit"),
      body = "doh!",
      status = 400,
      match = [matchers.json_params_matcher({
        "api_key": "deadbeef",
        "notebook": NOTEBOOK,
        "responses": [
          {
            "identifier": "q1",
            "response": "B",
          },
        ],
      })]
    )

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
      ],
    }

    with make_form(config) as form:
      form.ask()

      # updating the value fields of the widget instances simulates the user interacting with the
      # widget
      mocked_display.assert_called_once()
      vbox = mocked_display.call_args.args[0]
      widgets = [c.children[0].children[1] for c in vbox.children[:-1]]
      widgets[0].value = "B"

      button = vbox.children[-1]

      button.click()

      assert isinstance(caplog.records[0].exc_info[1], RuntimeError)
      assert str(caplog.records[0].exc_info[1]) == "Submit request returned error response: [400] doh!"

      assert button.button_style != "success"

  @responses.activate
  def test_ask_invalid_identifier(self):
    """
    Test ``Form.ask`` with an invalid question identifier.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
      ],
    }

    with make_form(config) as form, pytest.raises(ValueError, match="No such question: q2"):
      form.ask("q2")

  @pytest.mark.parametrize(("identifiers", "user_hashes", "csv"), (
    (("q1", "q2"), False, "q1,q2\n1,2\n2,3\n3,4"),
    (("q1", "q2"), True, "user,q1,q2\nabc,1,2\nbcd,2,3\ncde,3,4"),
    (tuple(), False, "q1,q2,q3\n\n1,2,3\n2,3,4\n3,4,5")
  ))
  @responses.activate
  @mock.patch("nbforms.pd.read_csv")
  def test_to_df(self, mocked_read_csv, identifiers, user_hashes, csv):
    """
    Test ``Form.to_df``.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")
    responses.get(
      url = make_url("/data"),
      body = csv,
      content_type = "text/csv",
      match=[matchers.json_params_matcher({
        "questions": [*(identifiers if identifiers else ("q1", "q2", "q3"))],
        "notebook": NOTEBOOK,
        "user_hashes": user_hashes,
      })]
    )

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "write something",
        },
        {
          "identifier": "q2",
          "type": "text",
          "question": "write something",
        },
        {
          "identifier": "q3",
          "type": "text",
          "question": "write something",
        },
      ],
    }

    with make_form(config) as form:
      df = form.to_df(*identifiers, user_hashes=user_hashes)

    assert df is mocked_read_csv.return_value
    mocked_read_csv.assert_called_once()
    assert mocked_read_csv.call_args.args[0].getvalue() == csv

  @responses.activate
  def test_to_df_invalid_identifier(self):
    """
    Test ``Form.to_df`` with an invalid question identifier.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
      ],
    }

    with make_form(config) as form, pytest.raises(ValueError, match="No such question: q2"):
      form.to_df("q2")

  @pytest.mark.parametrize(("identifiers", "user_hashes", "csv"), (
    (("q1", "q2"), False, "q1,q2\n1,2\n2,3\n3,4"),
    (("q1", "q2"), True, "user,q1,q2\nabc,1,2\nbcd,2,3\ncde,3,4"),
    (tuple(), False, "q1,q2,q3\n\n1,2,3\n2,3,4\n3,4,5")
  ))
  @responses.activate
  @mock.patch("nbforms.pd.read_csv")
  @mock.patch("nbforms.ds.Table.from_df")
  def test_to_table(self, mocked_from_df, mocked_read_csv, identifiers, user_hashes, csv):
    """"""
    responses.post(url=make_url("/auth"), body="deadbeef")
    responses.get(
      url = make_url("/data"),
      body = csv,
      content_type = "text/csv",
      match=[matchers.json_params_matcher({
        "questions": [*(identifiers if identifiers else ("q1", "q2", "q3"))],
        "notebook": NOTEBOOK,
        "user_hashes": user_hashes,
      })]
    )

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "write something",
        },
        {
          "identifier": "q2",
          "type": "text",
          "question": "write something",
        },
        {
          "identifier": "q3",
          "type": "text",
          "question": "write something",
        },
      ],
    }

    with make_form(config) as form:
      table = form.to_table(*identifiers, user_hashes=user_hashes)

    assert table is mocked_from_df.return_value
    mocked_read_csv.assert_called_once()
    assert mocked_read_csv.call_args.args[0].getvalue() == csv
    mocked_from_df.assert_called_once_with(mocked_read_csv.return_value)

  @responses.activate
  def test_to_table_invalid_identifier(self):
    """
    Test ``Form.to_table`` with an invalid question identifier.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
      ],
    }

    with make_form(config) as form, pytest.raises(ValueError, match="No such question: q2"):
      form.to_table("q2")

  @responses.activate
  def test_data_retrieval_http_error(self):
    """
    Test handling of non-200 statuses return by the ``/data`` server route.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")
    responses.get(
      url = make_url("/data"),
      body = "doh!",
      status = 400,
      match=[matchers.json_params_matcher({
        "questions": ["q1", "q2", "q3"],
        "notebook": NOTEBOOK,
        "user_hashes": False,
      })]
    )

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "questions": [
        {
          "identifier": "q1",
          "type": "text",
          "question": "write something",
        },
        {
          "identifier": "q2",
          "type": "text",
          "question": "write something",
        },
        {
          "identifier": "q3",
          "type": "text",
          "question": "write something",
        },
      ],
    }

    with make_form(config) as form, \
        pytest.raises(RuntimeError, match="Server data request returned error response: \\[400\\] doh!"):
      form.to_df()

  @pytest.mark.parametrize(("enabled", "status", "want_out", "want_err"), (
    # attendance tracking not enabled in config
    (False, None, "", ValueError("This notebook does not record attendance")),
    # success
    (True, 200, "Your attendance has been recorded.\n", None),
    # failure
    (True, 400, "", RuntimeError(f"Server returned an error response while recording attendance: \\[400\\] ok")),
  ))
  @responses.activate
  def test_take_attendance(self, capsys, enabled, status, want_out, want_err):
    """
    Test ``Form.take_attendance``.
    """
    responses.post(url=make_url("/auth"), body="deadbeef")
    responses.post(
      url = make_url("/attendance"),
      body = "ok",
      status = status,
      match=[matchers.json_params_matcher({"api_key": "deadbeef", "notebook": NOTEBOOK})],
    )

    config = {
      "server_url": SERVER_URL,
      "notebook": NOTEBOOK,
      "attendance": enabled,
      "questions": [
        {
          "identifier": "q1",
          "type": "multiplechoice",
          "question": "A, B, or C?",
          "options": ["A", "B", "C"],
        },
      ],
    }

    cm = nullcontext()
    if want_err is not None:
      cm = pytest.raises(type(want_err), match=str(want_err))

    with make_form(config) as form, cm:
      form.take_attendance()

    captured = capsys.readouterr()
    assert captured.out == f"Please enter a username and password for nbforms.\n{want_out}"
