import importlib.util

timecode_path = '/Users/schang/Google Drive/Editables/Python/Timecode/timecode.py'
resolve_path = '/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples/python_get_resolve.py'
spec1 = importlib.util.spec_from_file_location('timecode', timecode_path)
spec2 = importlib.util.spec_from_file_location('davinci', resolve_path)

tc = importlib.util.module_from_spec(spec1)
dvr = importlib.util.module_from_spec(spec2)
spec1.loader.exec_module(tc)
spec2.loader.exec_module(dvr)

resolve = dvr.GetResolve()
pm = resolve.GetProjectManager()
ms = resolve.GetMediaStorage()
project = pm.GetCurrentProject()
mp = project.GetMediaPool()
active_timeline = project.GetCurrentTimeline()
presets = project.GetRenderPresets()
fps = float(project.GetSetting('timelineFrameRate'))
clip_colors = ['Blue', 'Green', 'Yellow', 'Pink', 'Purple']
sep = '.'

track_num = 1
while track_num <= active_timeline.GetTrackCount('video'):
    video_track_items = active_timeline.GetItemsInTrack('video', track_num)

    for video_item in video_track_items.values():
        video_clip = video_item
        if video_clip.GetClipColor() != 'Default':
            for clip_color in clip_colors:
                if clip_color == video_clip.GetClipColor():
                    for preset in presets.values():
                        if clip_color in preset:
                            project.LoadRenderPreset(preset)
                            file_name = video_clip.GetName().split(sep, 1)[0] + '-' \
                            + str(tc.remove_tc_format(tc.frame_to_tc(video_clip.GetStart(), fps)))
                            check = project.SetRenderSettings({'MarkIn': video_clip.GetStart(), \
                            'MarkOut': video_clip.GetEnd() -1, 'CustomName': file_name})
                            print(check)
                            project.AddRenderJob()
    
    track_num += 1

project.StartRendering()

while project.IsRenderingInProgress():
    continue

print('Rendering is done.')

render_num = 1
while render_num <= len(project.GetRenderJobs()):
    if project.GetRenderJobStatus(render_num)['JobStatus'] == 'Complete':
        project.DeleteRenderJobByIndex(render_num)
        print(render_num)

print('End')