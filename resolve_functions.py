import importlib.util
import os
import time
import csv

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

# Function to get clip colors in given timeline.  Returns an array of used colors called 'active_clip_colors'.
def get_clip_colors(user_timeline):
    timeline = project.GetTimelineByIndex(user_timeline)
    check_timeline = project.SetCurrentTimeline(timeline)
    # Gets active timeline from current project
    # active_timeline = project.GetCurrentTimeline() 

    if(not check_timeline):
        return 'Invalid timeline.'

    track_num = 1
    active_clip_colors = []
    while track_num <= timeline.GetTrackCount('video'):
        # Grabs all clips from 'track_num' track from active timeline.
        video_track_items = timeline.GetItemsInTrack('video', track_num)

        # Checks each individual clip to see if a clip color has been assigned.
        # If clip has a color check to see if that color as already been added to our list.  If not add.
        for video_clip in video_track_items.values():
            if video_clip.GetClipColor() != 'Default':
                if video_clip.GetClipColor() not in active_clip_colors:
                    active_clip_colors.append(video_clip.GetClipColor())
        track_num += 1
    return active_clip_colors

# Function to get the marker colors of given timeline.  Returns an array of used marker colors.
def get_marker_colors(user_timeline):
    timeline = project.GetTimelineByIndex(user_timeline)
    check_timeline = project.SetCurrentTimeline(timeline)
    # Gets active timeline from current project
    # active_timeline = project.GetCurrentTimeline() 

    if(not check_timeline):
        return 'Invalid timeline.'

    markers = timeline.GetMarkers()
    active_marker_colors = []
    for marker in markers:
        if markers[marker]['color'] not in active_marker_colors:
            active_marker_colors.append(markers[marker]['color'])
    return active_marker_colors

# Function to return a list of render presets.
def get_render_presets():
    dict_presets = project.GetRenderPresets()
    return(list(dict_presets.values()))

# Function to return all timeline names from current project.
def get_timelines():
    dict_timelines = {}
    index = 1
    
    while index <= project.GetTimelineCount():
        dict_timelines[index] = project.GetTimelineByIndex(index).GetName()
        index += 1
    
    return dict_timelines

# Adds clips to render queue based on given clip color with given render location.
def add_clip_color_to_render_queue(user_timeline, user_preset, user_clip_color, user_prefix, render_location):
    timeline = project.GetTimelineByIndex(user_timeline)
    check_preset = project.LoadRenderPreset(user_preset)
    check_timeline = project.SetCurrentTimeline(timeline)
    track_num = 1

    if(not check_preset):
        return 'Invalid preset.'
    if(not check_timeline):
        return 'Invalid timeline.'

    # Gets every item from every video track from the active timeline.
    while track_num <= timeline.GetTrackCount('video'):
        video_track_items = timeline.GetItemsInTrack('video', track_num)

        # Checks each video clip color to see if it matches selected clip color and adds to Render queue.
        # Adds given suffix to file name, otherwise adds timecode of start point of  clip in active timeline.
        # This will only be added if render preset allows unique filenames.
        for video_item in video_track_items.values():
            video_clip = video_item
            if user_clip_color == video_clip.GetClipColor():
                if(user_prefix and not user_prefix.isspace()):
                    filename = user_prefix + '-' + video_clip.GetName().split(sep, 1)[0]
                else:
                    filename = video_clip.GetName().split(sep, 1)[0] + '-' \
                    + str(tc.remove_tc_format(tc.frame_to_tc(video_clip.GetStart(), fps)))
                check_render = project.SetRenderSettings({'MarkIn': video_clip.GetStart(), \
                'MarkOut': video_clip.GetEnd() -1, 'TargetDir': render_location, 'CustomName': filename})
                if(not check_render):
                    return 'An error has occured.'
                project.AddRenderJob()
        
        track_num += 1

# Adds clips to render queue based on given clip color with given render location.
def add_clip_color_with_shot_list(user_timeline, user_preset, user_clip_color, user_prefix, render_location, vfx_list):
    timeline = project.GetTimelineByIndex(user_timeline)
    check_preset = project.LoadRenderPreset(user_preset)
    check_timeline = project.SetCurrentTimeline(timeline)
    track_num = 1
    vfx_shot_df = vfx_list[0]
    vfx_name_list = []

    if(not check_preset):
        return 'Invalid preset.'
    if(not check_timeline):
        return 'Invalid timeline.'

    # Gets every item from every video track from the active timeline.
    while track_num <= timeline.GetTrackCount('video'):
        video_track_items = timeline.GetItemsInTrack('video', track_num)

        # Checks each video clip color to see if it matches selected clip color and adds to Render queue.
        # Adds given suffix to file name, otherwise adds timecode of start point of  clip in active timeline.
        # This will only be added if render preset allows unique filenames.
        for video_item in video_track_items.values():
            video_clip = video_item
            if user_clip_color == video_clip.GetClipColor():
                if(user_prefix and not user_prefix.isspace()):
                    clip_tc = tc.frame_to_tc(video_clip.GetStart(), fps)
                    vfx_shot_row = vfx_shot_df[vfx_shot_df.loc[:, 'TIMECODE IN'] == clip_tc]
                    if not vfx_shot_row.empty:
                        shot_number = vfx_shot_row.iloc[0, :]['SHOT NUMBER']
                        scene = vfx_shot_row.iloc[0, :]['SCENE']
                        filename = user_prefix + shot_number + '_SC' + scene
                        clip_render_location = render_location + '/' + filename + '/'
                    else:
                        filename = video_clip.GetName().split(sep, 1)[0] + '-' \
                        + str(tc.remove_tc_format(tc.frame_to_tc(video_clip.GetStart(), fps)))
                        clip_render_location = render_location + '/' + filename + '/'
                    vfx_name_list.append(filename)
                    filename += '_'
                else:
                    filename = video_clip.GetName().split(sep, 1)[0] + '-' \
                    + str(tc.remove_tc_format(tc.frame_to_tc(video_clip.GetStart(), fps)))
                    clip_render_location = render_location
                    vfx_name_list.append(filename)
                check_render = project.SetRenderSettings({'MarkIn': video_clip.GetStart(), 
                'MarkOut': video_clip.GetEnd() -1, 'TargetDir': clip_render_location, 'CustomName': filename})
                if(not check_render):
                    return 'An error has occured.'
                project.AddRenderJob()
        
        track_num += 1
    csv_filename = os.path.expanduser('~/Desktop') + '/' + timeline.GetName() + '-list.csv'
    print(vfx_name_list)
    with open(csv_filename, 'w', newline = '\n') as file:
        writer = csv.writer(file)
        writer.writerows(zip(vfx_name_list))

# Adds marked portions of a sequence to render queue to the given render location.
def add_marker_stringout_batch_render_queue(user_timeline, user_preset, user_color, user_suffix, render_location):
    timeline = project.GetTimelineByIndex(user_timeline)
    check_preset = project.LoadRenderPreset(user_preset)
    check_timeline = project.SetCurrentTimeline(timeline)

    if(not check_preset):
        return 'Invalid preset.'
    if(not check_timeline):
        return 'Invalid timeline.'
    
    timeline_markers = timeline.GetMarkers()

    for marker in timeline_markers:
        if(timeline_markers[marker]['color'] == user_color):
            filename = timeline_markers[marker]['name']
            if(user_suffix and not user_suffix.isspace()):
                filename = filename + '-' + user_suffix
            else:
                filename = timeline.GetName() + '-' + str(tc.remove_tc_format(tc.frame_to_tc(timeline.GetStartFrame() + marker, fps)))

            start_time = timeline.GetStartFrame() + marker
            end_time = start_time + timeline_markers[marker]['duration'] - 1
            check_render = project.SetRenderSettings({'MarkIn': start_time, 'MarkOut': end_time, 'TargetDir': render_location, 'CustomName': filename})
            if(not check_render):
                return 'An error has occured.'
            project.AddRenderJob()

# Adds given sequence to render queue with given render preset and render location.
def add_sequence_batch_render_queue(user_timeline, user_preset, render_location, header_time):
    timeline = project.GetTimelineByIndex(user_timeline)
    check_preset = project.LoadRenderPreset(user_preset)
    check_timeline = project.SetCurrentTimeline(timeline)

    if(not check_preset):
        return 'Invalid preset.'
    if(not check_timeline):
        return 'Invalid timeline.'

    start_time = timeline.GetStartFrame() + header_time
    end_time = timeline.GetEndFrame() - 1
    check_render = project.SetRenderSettings({'MarkIn': start_time, 'MarkOut': end_time, 'TargetDir': render_location, 'CustomName': timeline.GetName()})

    if(not check_render):
        return 'An error has occured.'
    project.AddRenderJob()

# Returns the number of jobs in render queue.
def get_number_of_render_jobs():
    return(len(project.GetRenderJobs()))

# Deletes all completed jobs in render queue.
def delete_completed_jobs():
    render_num = 1
    while render_num <= len(project.GetRenderJobs()):
        if project.GetRenderJobStatus(render_num)['JobStatus'] == 'Complete':
            project.DeleteRenderJobByIndex(render_num)
        else:
            render_num += 1
    return('Completed jobs have been removed.')

# Tells Resolve to start rendering all jobs in render queue.
def start_render_jobs():
    project.StartRendering()
    while project.IsRenderingInProgress():
        continue
    return('Rendering is done.')

# Creates a new bin under the Master bin with the name of the folder name in 'folder_location'.
# Appends the time to the end of the bin name.
# Add media from 'folder_location' to the media pool in newly created bin.
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