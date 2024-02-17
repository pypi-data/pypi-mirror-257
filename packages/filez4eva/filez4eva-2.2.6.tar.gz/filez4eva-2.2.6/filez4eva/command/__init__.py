from wizlib.command import WizCommand
from wizlib.input_handler import InputHandler
from wizlib.config_handler import ConfigHandler
from wizlib.ui_handler import UIHandler


class Filez4EvaCommand(WizCommand):

    default = 'scan'
    handlers = [InputHandler, ConfigHandler, UIHandler]
