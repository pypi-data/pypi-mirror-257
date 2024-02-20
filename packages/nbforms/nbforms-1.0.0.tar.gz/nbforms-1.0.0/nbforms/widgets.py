"""Question widgets for nbforms"""

from abc import ABC, abstractmethod
from ipywidgets import Label, RadioButtons, SelectMultiple, Text, Textarea
from typing import Any, Dict, List, Tuple, Type, TYPE_CHECKING, Union

if TYPE_CHECKING:
  from ipywidgets import Widget


class QuestionWidget(ABC):
  """
  An ABC representing a widget for a type of question.
  """

  _question: str
  """the question text"""

  @abstractmethod
  def __init__(self, config: Dict[str, Union[str, List[str]]]):
    raise NotImplementedError()

  @abstractmethod
  def to_widget_tuple(self, value: Any) -> Tuple[Label, "Widget"]:
    """
    Create a label containing the question and a widget for entering the user's response and
    return them in a tuple. The widget's value is set to ``value``.
    """
    raise NotImplementedError()


class MultipleChoiceQuestion(QuestionWidget):
  """
  A multiple choice question widget.
  """

  _options: List[str]
  """the response options"""

  def __init__(self, config):
    self._question = config["question"]
    self._options = config["options"]

  def to_widget_tuple(self, value):
    return Label(self._question), RadioButtons(options=self._options, value=value)


class CheckboxQuestion(QuestionWidget):
  """
  A select multiple question widget.
  """

  _options: List[str]
  """the response options"""

  def __init__(self, config):
    self._question = config["question"]
    self._options = config["options"]

  def to_widget_tuple(self, value):
    if value is None:
      value = tuple()
    return Label(self._question), SelectMultiple(options=self._options, value=value)


class TextQuestion(QuestionWidget):
  """
  A text input question widget.
  """

  _placeholder: str
  """the text entry placeholder"""

  def __init__(self, config):
    self._question = config["question"]
    self._placeholder = config.get("placeholder", "Type something")

  def to_widget_tuple(self, value):
    return Label(self._question), Text(placeholder=self._placeholder, value=value)


class TextAreaQuestion(QuestionWidget):
  """
  A text area question widget.
  """

  _placeholder: str
  """the text entry placeholder"""

  def __init__(self, config):
    self._question = config["question"]
    self._placeholder = config.get("placeholder", "Type something")

  def to_widget_tuple(self, value):
    return Label(self._question), Textarea(placeholder=self._placeholder, value=value)


TYPE_MAPPING: Dict[str, Type[QuestionWidget]] = {
  "multiplechoice": MultipleChoiceQuestion,
  "checkbox": CheckboxQuestion,
  "text": TextQuestion,
  "paragraph": TextAreaQuestion,
}
"""maps question type strings to their ``QuestionWidget`` subclass"""
