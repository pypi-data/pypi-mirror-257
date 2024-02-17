import markdown

class ReleaseNotes:
  
  DIR = "templates/status/partials"
  RELEASE_NOTES = f'{DIR}/release_notes.md'

  def __init__(self):
    self._text = ""
    self._read()

  def notes(self):
    return markdown.markdown(self._text)

  def _read(self):
    with open(self.__class__.RELEASE_NOTES, "r") as f:
      self._text = f.read()

