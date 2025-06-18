from nicegui import ui

def date_input():
    with ui.input('Data de estreia').classes('w-48 mb-4') as date:
        date.on('click', lambda: menu.open())
        with ui.menu().props('anchor="bottom middle" self="top middle"') as menu:
            calendar = ui.date(mask='DD/MM/YYYY')
            calendar.bind_value(date)
            calendar.on('update:model-value', lambda: menu.close())
    return date