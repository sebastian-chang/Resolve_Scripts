import importlib.util

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
presets = project.GetRenderPresets()
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

def

get_clip_colors()