import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '336600070:AAH3oZzwf9xHxF4nYHdv2BXj1Rv5Kw2xYA8'
WEBHOOK_URL = 'https://b92ef005.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'init',
        'user',
        'talk',
        'sorry',
        'suck',
        'play',
        'east',
        'animal',
        'animalDetail',
        'west',
        'astro',
        'astroDetail',
        'math',
        'matheq',
        'mathneq'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'user'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'talk',
            'conditions': 'is_going_to_talk'
        },
        {
            'trigger': 'advance',
            'source': 'talk',
            'dest': 'sorry',
            'conditions': 'is_going_to_sorry'
        },
        {
            'trigger': 'advance',
            'source': 'talk',
            'dest': 'suck',
            'conditions': 'is_going_to_suck'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'play',
            'conditions': 'is_going_to_play'
        },
        {
            'trigger': 'advance',
            'source': 'play',
            'dest': 'west',
            'conditions': 'is_going_to_west'
        },
        {
            'trigger': 'advance',
            'source': 'west',
            'dest': 'astro',
            'conditions': 'is_going_to_astro'
        },
        {
            'trigger': 'advance',
            'source': 'astro',
            'dest': 'astroDetail',
            'conditions': 'is_going_to_astroDetail'
        },
        {
            'trigger': 'advance',
            'source': 'play',
            'dest': 'east',
            'conditions': 'is_going_to_east'
        },
        {
            'trigger': 'advance',
            'source': 'east',
            'dest': 'animal',
            'conditions': 'is_going_to_animal'
        },
        {
            'trigger': 'advance',
            'source': 'animal',
            'dest': 'animalDetail',
            'conditions': 'is_going_to_animalDetail'
        },
        {
            'trigger': 'advance',
            'source': 'animalDetail',
            'dest': 'animalDetail',
            'conditions': 'is_going_to_animalDetail'
        },
        {
            'trigger': 'advance',
            'source': 'animalDetail',
            'dest': 'user',
            'conditions': 'is_going_out_animalDetail'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'math',
            'conditions': 'is_going_to_math'
        },
        {
            'trigger': 'advance',
            'source': 'math',
            'dest': 'matheq',
            'conditions': 'is_going_to_matheq'
        },
        {
            'trigger': 'advance',
            'source': 'math',
            'dest': 'mathneq',
            'conditions': 'is_going_to_mathneq'
        },
        {
            'trigger': 'go_back',
            'source': [
                'sorry',
                'suck',
                'astroDetail',
                'matheq',
                'mathneq'
            ],
            'dest': 'user'
        }
    ],
    initial='init',
    auto_transitions=True,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    print('In handler')
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
