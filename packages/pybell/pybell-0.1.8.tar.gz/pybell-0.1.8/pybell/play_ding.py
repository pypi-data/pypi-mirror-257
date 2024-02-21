import audioplayer
from xdialog import info
from time import sleep
from pathlib import Path


def play_ding(file: str | None, time: float | None, dialog: bool) -> None:
    """
    Play a sound file.
    :param file: The path to the sound file.
    :param time: The time to play the sound for. If None, the sound will be played until it finishes.
    :param dialog: Show a dialog after the sound is played. Note that the program is blocked until the dialog is closed.
    :return: None
    """
    if file is None:
        folder = Path(__file__).parent
        file = str(folder / 'ding.wav')

    player = audioplayer.AudioPlayer(file)

    if time is not None:
        player.play(block=False)
        sleep(time)
        player.stop()

    else:
        player.play(block=True)

    if dialog:
        info('Task done!', 'Press okay to continue.')
