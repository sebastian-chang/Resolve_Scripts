import resolve_functions as my_resolve

def clip_color_render(user_input, *vfx_shot_df):
    if vfx_shot_df:
        my_resolve.add_clip_color_with_shot_list(user_input.timelines.currentIndex(), user_input.presets.currentText(), user_input.clip_colors.currentText(), user_input.filename_prefix_textbox.text(), user_input.render_location.text(),
                                                  vfx_shot_df)
    else:
        my_resolve.add_clip_color_to_render_queue(user_input.timelines.currentIndex(), user_input.presets.currentText(), user_input.clip_colors.currentText(), user_input.filename_prefix_textbox.text(), user_input.render_location.text())