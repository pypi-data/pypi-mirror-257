# builtin
import copy
import os
import json
import tempfile
import pathlib
from datetime import datetime, timedelta


class Checkpoints:
    """
    This is a class to make gathering data more resumable.
    The web is subject to many interruptions, since you are rely on many touch points between yourself and your destination to work smoothly.
    As such, you may crash out before getting to fully download items from your list of links, and the process to return to that point may take some time.
    This is a simple interface to make that slightly less bothersome.
    """

    # The key in the source data for our checkpoints
    _url  = ''
    # The path the file is stored to
    _path = ''
    # The total data from the file (can contain other keyed checkpoints)
    _data = {}
    # The header of data for our checkpoint
    _checkpoint_header = {}
    # The body of data for our checkpoint
    _checkpoint_data = []

    def __init__(self, url, path=None, timeout_minutes=480):
        """
        Checkpoints must be initialized against a url, used as the unique id for it's data.
        You may specify a specific outfile, or one is made in temp data for you.
        :param url: url to checkpoint with
        :param path: checkpoint file destination
        """

        self._url = url

        # ascertain path
        self._path = path
        if path is None:
            tempdir = tempfile.gettempdir()
            bt_tempdir = pathlib.Path(tempdir).joinpath('brushtail')
            bt_tempdir.mkdir(parents=True, exist_ok=True)
            self._path = bt_tempdir.joinpath('checkpoints.json')
            # self._path = str(self._path)

        if os.path.exists(self._path):
            # handle existing file
            with open(self._path, 'r') as f:
                self._data = json.loads(f.read())
            # try:
            #     with open(path, 'r') as f:
            #         self._data = json.loads(f.read())
            # except Exception as e:
            #     print("Error loading checkpoints.")

            # handle existing url key in data
            if self._url not in self._data:
                self._checkpoint_header = {}
                self._checkpoint_header['timeout'] = datetime.now() + timedelta(minutes=timeout_minutes)
                self._checkpoint_data = []
            else:
                self._checkpoint_header, self._checkpoint_data = self._data[self._url]

                # deserialize timeout
                self._checkpoint_header['timeout'] = datetime.fromisoformat(self._checkpoint_header['timeout'])

                # if links are expired, start anew
                if self._checkpoint_header['timeout'] < datetime.now():
                    print("Checkpoint is expired, starting again.")
                    self._checkpoint_header = {}
                    self._checkpoint_header['timeout'] = datetime.now() + timedelta(minutes=timeout_minutes)
                    self._checkpoint_data = []

        else:
            # make a whole new file
            self._data = {}
            self._checkpoint_header = {}
            self._checkpoint_header['timeout'] = datetime.now() + timedelta(minutes=timeout_minutes)
            self._checkpoint_data = []

    def save(self):
        # ensure any outward transformations are on a deepcopy
        self._data[self._url] = copy.deepcopy((self._checkpoint_header, self._checkpoint_data))

        # ensure timeout is isoformat
        # other data assumed to be a sleeping dog
        self._data[self._url][0]['timeout'] = self._data[self._url][0]['timeout'].isoformat()

        with open(self._path, 'w') as f:
            f.write(json.dumps(self._data, indent=2))

    def append(self, data, then_save=True):
        self._checkpoint_data.append(data)
        if then_save:
            self.save()

    def __gt__(self, other):
        if len(self._checkpoint_data) > other:
            return True
        return False

    def __lt__(self, other):
        if len(self._checkpoint_data) < other:
            return True
        return False

    def __getitem__(self, item):
        return self._checkpoint_data[item]
