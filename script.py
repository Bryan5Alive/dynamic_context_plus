from datetime import datetime

import gradio as gr

params = {
    'location': '',
    'temperature': 'pleasant',
    'weather': 'clear',
    'time_context': False,
    'date_context': False,
    'auto_append': False
}


def state_modifier(state):
    month = datetime.now().month
    day = datetime.now().day

    if (month > 3 and month < 6) or (month == 3 and day >= 20) or (month == 6 and day < 21):
        season = 'spring'
    elif (month > 6 and month < 9) or (month == 6 and day >= 21) or (month == 9 and day < 22):
        season = 'summer'
    elif (month > 9 and month < 12) or (month == 9 and day >= 22) or (month == 12 and day < 21):
        season = 'autumn'
    else:
        season = 'winter'

    hour = datetime.now().hour
    if 5 <= hour < 12:
        time_of_day = 'morning'
    elif 12 <= hour < 17:
        time_of_day = 'afternoon'
    elif 17 <= hour < 21:
        time_of_day = 'evening'
    else:
        time_of_day = 'night'

    weekday = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')[datetime.now().weekday()]

    if not params['auto_append']:
        state['context'] = state['context'].replace('{{location}}', params['location'])
        state['context'] = state['context'].replace('{{temperature}}', params['temperature'])
        state['context'] = state['context'].replace('{{weather}}', params['weather'])
        state['context'] = state['context'].replace('{{time}}', datetime.now().strftime('%I:%M %p'))
        state['context'] = state['context'].replace('{{time_of_day}}', time_of_day)
        state['context'] = state['context'].replace('{{date}}', datetime.now().strftime('%B %d, %Y'))
        state['context'] = state['context'].replace('{{season}}', season)
        state['context'] = state['context'].replace('{{weekday}}', weekday)
    else:
        auto_context = get_auto_context(season, time_of_day, weekday)
        if ('context' in state) and state['context']:
            state['context'] += '\n\n' + auto_context + '\n'
        else:
            state['context'] = auto_context + '\n'

    return state


def get_auto_context(season, time_of_day, weekday):
    base_template = f'This conversation takes place on a {weekday} {time_of_day}'

    if ('location' in params) and params['location']:
        base_template += f', in {params["location"]}'

    if season:
        base_template += f', during the {season} season'

    if (('temperature' in params) and params['temperature']) and (('weather' in params) and params['weather']):
        base_template += f', with a {params["temperature"]} temperature and {params["weather"]} weather'

    return base_template + '.'


def input_modifier(string):
    if params['time_context']:
        string += f' [Current time: {datetime.now().strftime("%I:%M %p")}]'
    if params['date_context']:
        string += f' [Current date: {datetime.now().strftime("%B %d, %Y")}]'
    return string


def ui():
    with gr.Accordion('Dynamic context'):
        with gr.Row():
            with gr.Column():
                location = gr.Textbox(placeholder=params['location'], value=params['location'], label='Location')
                temperature = gr.Dropdown(['hot', 'warm', 'pleasant', 'chilly', 'cold'], value=params['temperature'], allow_custom_value=True, label='Temperature', type='value')
                weather = gr.Dropdown(['clear', 'rainy', 'snowy', 'foggy'], value=params['weather'], allow_custom_value=True, label='Weather', type='value')
            with gr.Column():
                time_context = gr.Checkbox(value=params['time_context'], label='Append current time context to the prompt')
                date_context = gr.Checkbox(value=params['date_context'], label='Append current date context to the prompt')

    location.change(lambda x: params.update({'location': x}), location, None)
    temperature.change(lambda x: params.update({'temperature': x}), temperature, None)
    weather.change(lambda x: params.update({'weather': x}), weather, None)
    time_context.change(lambda x: params.update({'time_context': x}), time_context, None)
    date_context.change(lambda x: params.update({'date_context': x}), date_context, None)
