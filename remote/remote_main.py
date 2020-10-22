#!/usr/bin/python3

import click
import random
import logging
import time
import sys
import libraries.LCD_1in44 as LCD_1in44
import libraries.LCD_Config as LCD_Config

from PIL import Image, ImageDraw, ImageFont, ImageColor

from libraries.launch_control import LaunchControl


class StreamToLogger(object):
    ''' Fake file-like stream object that redirects writes to a logger instance.
    '''

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


logging.basicConfig(level=logging.INFO, format='(%(threadName)-9s) %(message)s', )

stdout_logger = logging.getLogger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl


@click.command()
@click.option('-d', '--debug', is_flag=True, help='Turn on debugging')
def main(debug):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    LCD = LCD_1in44.LCD()
    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)
    LCD.LCD_Clear()

    image = Image.new('RGB', (LCD.width, LCD.height), 'WHITE')
    draw = ImageDraw.Draw(image)

    remoteid = random.randint(0, 10)
    print(f'remote id: {remoteid}')
    draw.text((33, 22), f'REMOTE ID\n{remoteid}', fill='BLUE')
    LCD.LCD_ShowImage(image, 0, 0)
    draw.rectangle([(0, 0), (LCD.width, LCD.height)], fill='WHITE')

    lc = LaunchControl(remoteid)

    while True:
        print('Safe...')
        draw.text((33, 22), 'SAFE', fill='BLUE')
        LCD.LCD_ShowImage(image, 0, 0)
        draw.rectangle([(0, 0), (LCD.width, LCD.height)], fill='WHITE')

        lc.wait_for_ready()
        print('Ready...')
        draw.text((33, 22), 'READY', fill='BLUE')
        LCD.LCD_ShowImage(image, 0, 0)
        draw.rectangle([(0, 0), (LCD.width, LCD.height)], fill='WHITE')

        print('Launch...')
        if lc.wait_for_launch():
            LCD.LCD_ShowImage(image, 0, 0)
            draw.rectangle([(0, 0), (LCD.width, LCD.height)], fill='WHITE')

            draw.text((33, 22), 'LAUNCH!!!', fill='BLUE')

        lc.send_safe()


if __name__ == '__main__':
    main()
