send_board_id = '<b>Введите свой id платы</b>'
confirm_board = '<b>Плата успешно добавлена\nСписок ваших плат</b>'
delete_board_confirm = '<b>Плата успешно удалена\nСписок ваших плат</b>'
list_board = '<b>Список ваших плат</b>'
no_boards = '<b>У вас нет плат, добавьте новую!</b>'
no_correct_board_id = "<b>Некорректный ID доски. Пожалуйста, введите правильный ID.</b>"
view_board = lambda board_id: f"<b>Управление платой {board_id}</b>"
error_journal = '<b>Журнал ошибок платы</b>'
no_error = '<b>Ошибок нет</b>'
show_error = lambda error: (f'<b>Ошибка: {error.title}\n'
                            f'Сообщение: {error.message}\n\n'
                            f'Дата: {error.date.strftime("%d.%m.%y %H:%M:%S")}</b>')