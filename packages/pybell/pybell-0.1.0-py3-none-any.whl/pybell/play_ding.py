from audioplayer import AudioPlayer
from xdialog import info
from time import sleep
from pathlib import Path


def play_ding(file: str | None, time: float | None, warning: bool) -> None:
    """
    Play a sound file.
    :param file: The path to the sound file.
    :param time: The time to play the sound for. If None, the sound will be played until it finishes.
    :param warning: Show a warning dialog after the sound is played. Note that this will block the program until the dialog is closed.
    :return: None
    """
    if file is None:
        folder = Path(__file__).parent
        file = str(folder / 'ding.wav')

    player = AudioPlayer(file)

    if time is not None:
        player.play(block=False)
        sleep(time)
        player.stop()

    else:
        player.play(block=True)

    if warning:
        info('Task done!', 'Press okay to continue.')
