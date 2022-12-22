from aiogram.utils.callback_data import CallbackData

START_REG = "start_reg"
DONE_REGISTRATION = "done_reg"
ADD_TO_CHANNEL = "add_user_to_channel"
MAIN_MENU = "get_mm"

reg = CallbackData("reg", "action")
mm = CallbackData("mm", "action")
select_date = CallbackData("sd", "action", "date")
change_post = CallbackData("change_p", "action", "date", "comp_or_post", "post_id")
turn_on_or_off_post = CallbackData("turn_o_o", "action", "date", "comp_or_post", "post_id", "status")
send_one_or_all = CallbackData("soop", "action", "date", "comp_or_post", "post_id", "send_one_or_all")
select_platform = CallbackData("sp", "action", "date", "comp_or_post", "post_id", "send_one_or_all", "platform")
select_channel = CallbackData("sc", "action", "date", "comp_or_post", "post_id", "send_one_or_all", "platform",
                              "channel_id")
get_post_by_id = CallbackData("gpbic", "action", "date", "comp_or_post", "post_id")
settings_menu = CallbackData("sm", "first_lvl", "second_lvl")
sub_menu = CallbackData("sub_m", "first_lvl", "second_lvl")
rates_menu = CallbackData("rates_m", "first_lvl", "second_lvl", "third_lvl")
rate_for_helper_menu = CallbackData("rfhm", "first_lvl", "second_lvl", "rate_pk", "inviter_id")
pay_menu = CallbackData("pay_m", "first_lvl", "second_lvl", "rate_pk")
pay_menu_helper = CallbackData("p_m_h", "first_lvl", "second_lvl", "rate_pk", "inviter_id")
settings_currency = CallbackData("select_cur", "first_lvl", "second_lvl", "third_lvl")
settings_rounder = CallbackData("rounder", "first_lvl", "second_lvl", "third_lvl")
settings_product = CallbackData("s_prod", "first_lvl", "second_lvl", "third_lvl")
settings_link = CallbackData("s_link", "first_lvl", "second_lvl", "third_lvl")
settings_channel = CallbackData("s_ch", "first_lvl", "second_lvl", "third_lvl")
settings_signature = CallbackData("s_sign", "first_lvl", "second_lvl", "third_lvl")
settings_formula_and_comm = CallbackData(
    "s_f_a_c", "first_lvl", "second_lvl", "third_lvl"
)
select_customize_currency = CallbackData(
    "s_c_cur", "first_lvl", "second_lvl", "third_lvl", "selected_cur"
)
settings_wm = CallbackData("s_wm", "first_lvl", "second_lvl", "third_lvl")
settings_wm_position = CallbackData("s_wm_pos", "first_lvl", "second_lvl", "third_lvl")
