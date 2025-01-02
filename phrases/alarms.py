main_alarms_phrase = '<b>Выберите функцию</b>'
control_alarms_phrase = '<b>Управление будильником</b>'

date_phrase = lambda date: f'<b>{date.strftime('%d.%m.%Y')}</b>'
passed_date_phrase = lambda date: f'<b>Выбранная дата уже прошла. Пожалуйста, введите новую дату.\n{date.strftime("%d.%m.%Y")}</b>'
select_date_phrase = lambda now: f'<b>Выберите дату\n {now.strftime('%d.%m.%Y')}</b>'

time_phrase = lambda time: f'<b>{time.strftime("%H:%M")}</b>'
passed_time_phrase = lambda time: f'<b>Выбранное время уже прошло. Пожалуйста, введите новое время\n {time.strftime("%H:%M")}</b>'
select_time_phrase = lambda time: f'<b>Выберите время\n {time.strftime("%H:%M")}</b>'
time_range_phrase = lambda time: f'<b>Между будильниками должен быть диапазон 15 минут. Пожалуйста, введите новое время\n {time.strftime("%H:%M")}</b>'
set_alarms_phrase = lambda date_time: (f"<b>Будильник успешно установлен!\n"
                                       f"Дата: {date_time.date().strftime("%d.%m.%y")}\n"
                                       f"Время: {date_time.time().strftime("%H:%M")}</b>")

no_alarms_phrase = '<b>У вас нет установленных будильников.</b>'
alarms_list_phrase = '<b>Ваши будильники</b>'
delete_alarms_phrase = '<b>Будильник успешно удален.</b>'

alarms_sticker = 'CAACAgIAAxkBAAIWL2dyqzoGM-1tZjfGkU8jIhvru1w4AALkAAP3AsgPyqv-fxPmEhs2BA'
set_alarms_sticker = 'CAACAgEAAxkBAAIWLWdyqj85KNPcN2tpgL-1y5OyouvAAAK8AgAC7NBZRE-slDaxGAujNgQ'