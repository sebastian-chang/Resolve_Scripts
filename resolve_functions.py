import importlib.util
import os
import time

# Initialize  additional Python scripts needed to run code.
# timecode.py is used to do any timecode conversions.
# python_get_resolve.py is script giving By BlackMagicDesign to load resolve python modules.
timecode_path = '/Users/schang/Google Drive/Editables/Python/Timecode/timecode.py'
resolve_path = '/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples/python_get_resolve.py'
spec1 = importlib.util.spec_from_file_location('timecode', timecode_path)
spec2 = importlib.util.spec_from_file_location('davinci', resolve_path)

tc = importlib.util.module_from_spec(spec1)
dvr = importlib.util.module_from_spec(spec2)
spec1.loader.exec_module(tc)
spec2.loader.exec_module(dvr)

# Initialize main variables to DaVinci Resolve environment.
resolve = dvr.GetResolve()
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
ms = resolve.GetMediaStorage()
mp = project.GetMediaPool()
sep = '.'
fps = float(project.GetSetting('timelineFrameRate'))

# Function to get clip colors in active timeline.  Returns an array of used colors called 'active_clip_colors'.
def get_clip_colors():
    # Gets active timeline from current project
    active_timeline = project.GetCurrentTimeline() 
    track_num = 1
    active_clip_colors = []
    while track_num <= active_timeline.GetTrackCount('video'):
        # Grabs all clips from 'track_num' track from active timeline.
        video_track_items = active_timeline.GetItemsInTrack('video', track_num)

        # Checks each individual clip to see if a clip color has been assigned.
        # If clip has a color check to see if that color as already been added to our list.  If not add.
        for video_clip in video_track_items.values():
            if video_clip.GetClipColor() != 'Default':
                if video_clip.GetClipColor() not in active_clip_colors:
                    active_clip_colors.append(video_clip.GetClipColor())
        track_num += 1
    return active_clip_colors

def get_render_presets():
    dict_presets = project.GetRenderPresets()
    return(list(dict_presets.values()))

def add_job_to_render_queue(clip_color, user_preset, render_location):
    # Gets active timeline from current project
    active_timeline = project.GetCurrentTimeline() 
    track_num = 1
    project.LoadRenderPreset(user_preset)

    while track_num <= active_timeline.GetTrackCount('video'):
        video_track_items = active_timeline.GetItemsInTrack('video', track_num)

        for video_item in video_track_items.values():
            video_clip = video_item
            if video_clip.GetClipColor() != 'Default':
                if clip_color == video_clip.GetClipColor():
                    file_name = video_clip.GetName().split(sep, 1)[0] + '-' \
                    + str(tc.remove_tc_format(tc.frame_to_tc(video_clip.GetStart(), fps)))
                    check = project.SetRenderSettings({'MarkIn': video_clip.GetStart(), \
                    'MarkOut': video_clip.GetEnd() -1, 'CustomName': file_name})
                    if check == False:
                        return 'An error has occured.'
                    project.AddRenderJob()
        
        track_num += 1

def get_number_of_render_jobs():
    return(len(project.GetRenderJobs()))

def delete_completed_jobs():
    render_num = 1
    while render_num <= len(project.GetRenderJobs()):
        if project.GetRenderJobStatus(render_num)['JobStatus'] == 'Complete':
            project.DeleteRenderJobByIndex(render_num)
        else:
            render_num += 1
    return('Completed jobs have been removed.')

def start_render_jobs():
    project.StartRendering()
    while project.IsRenderingInProgress():
        continue
    return('Rendering is done.')

def add_to_media_pool(folder_location):
    if os.path.exists(folder_location):
        t = time.localtime()
        current_time = time.strftime(" - %H:%M:%S" , t)
        folder_name = os.path.basename(folder_location) + current_time
        root_folder = mp.GetRootFolder()
        mp.AddSubFolder(root_folder, folder_name)
        ms.AddItemsToMediaPool(folder_location)
        return(f'Media in {folder_location} has been added to the media pool.')
    else:
        return("Folder location doesn't exist.")


get_render_presets()
add_job_to_render_queue('Green','Pink - ProResProxy HD 2398', '/Users/schang/Desktop/Render Tests')
get_clip_colors()
get_number_of_render_jobs()
start_render_jobs()
delete_completed_jobs()
add_to_media_pool('/Users/schang/Desktop/Resolve Tests')