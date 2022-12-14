from aiogram.utils.callback_data import CallbackData

START_REG = "start_reg"
DONE_REGISTRATION = "done_reg"
ADD_TO_CHANNEL = "add_user_to_channel"
MAIN_MENU = "get_mm"

reg = CallbackData("reg", "action")
mm = CallbackData("mm", "action")
settings_menu = CallbackData("sm", "first_lvl", "second_lvl")
sub_menu = CallbackData("sub_m", "first_lvl", "second_lvl")
settings_currency = CallbackData("select_cur", "first_lvl", "second_lvl", "third_lvl")
select_customize_currency = CallbackData("s_c_cur", "first_lvl", "second_lvl", "third_lvl", "selected_cur")
