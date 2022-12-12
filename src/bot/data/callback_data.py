from aiogram.utils.callback_data import CallbackData

START_REG = "start_reg"
DONE_REGISTRATION = "done_reg"
ADD_TO_CHANNEL = "add_user_to_channel"
MAIN_MENU = "get_mm"

reg = CallbackData("reg", "action")
mm = CallbackData("mm", "action")
settings_menu = CallbackData("sm", "first_lvl", "second_lvl")
sub_menu = CallbackData("sub_m", "first_lvl", "second_lvl")
