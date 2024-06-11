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
    now = datetime.now()
    month = now.month
    day = now.day

    if (month > 3 and month < 6) or (month == 3 and day >= 20) or (month == 6 and day < 21):
        season = 'spring'
    elif (month > 6 and month < 9) or (month == 6 and day >= 21) or (month == 9 and day < 22):
        season = 'summer'
    elif (month > 9 and month < 12) or (month == 9 and day >= 22) or (month == 12 and day < 21):
        season = 'autumn'
    else:
        season = 'winter'

    hour = now.hour
    if 5 <= hour < 12:
        time_of_day = 'morning'
    elif 12 <= hour < 17:
        time_of_day = 'afternoon'
    elif 17 <= hour < 21:
        time_of_day = 'evening'
    else:
        time_of_day = 'night'

    weekday = now.strftime('%A')

    replacements = {
        'location': params['location'],
        'temperature': params['temperature'],
        'weather': params['weather'],
        'time': now.strftime('%I:%M %p'),
        'time_of_day': time_of_day,
        'date': now.strftime('%B %d, %Y'),
        'season': season,
        'weekday': weekday
    }

    if not params['auto_append']:
        state['context'] = state['context'].format_map(replacements)
    else:
        auto_context = get_auto_context(season, time_of_day, weekday)

        if 'context' in state and state['context']:
            state['context'] += f'\n\n{auto_context}\n'
        else:
            state['context'] = f'{auto_context}\n'

    return state


def get_auto_context(season, time_of_day, weekday):
    base_template = f'This conversation takes place on a {weekday} {time_of_day}'

    attributes_str = {
        'location': f', in {params["location"]}',
        'season': f', during the {season} season',
        'temperature_weather': f', with a {params["temperature"]} temperature and {params["weather"]} weather'
    }

    for key, value in attributes_str.items():
        if key in params and params[key]:
            base_template += value

    return base_template + '.'


def input_modifier(string):
    now = datetime.now()
    if params['time_context']:
        string += f' [Current time: {now.strftime("%I:%M %p")}]'
    if params['date_context']:
        string += f' [Current date: {now.strftime("%B %d, %Y")}]'
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
