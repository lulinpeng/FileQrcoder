import os

class VideoCutMerge:
    fragments:list = None
    def __init__(self):
        self.clear()
        pass
    
    # convert *.rmvb into *.mp4
    def rmvb_to_mp4(self, in_video:str, out_video:str='output.rmvb'):
        cmd = f'ffmpeg -i {in_video} -c:v libx264 -c:a aac {out_video}'
        status = os.system(cmd)
        print(f"Exit code: {status}")
        return

    # load details of cutting task
    def load_cut_task(self, task_path:str):
        self.fragments = []
        with open(task_path) as f:
            lines = f.readlines()
        lines = lines[1:]
        for line in lines:
            if line.startswith('#'):
                print('skip the line which starts with special symbol')
                continue
            print(line, line.split())
            fragment = tuple(line.split())
            self.fragments.append(fragment)
        return
    
    def clear(self):
        os.system('rm -rf cut merge')
        return

    # cut video accroding to the detail described in 'task.txt' 
    def cut(self, cut_dir:str='cut'):
        os.makedirs(cut_dir, exist_ok=True)
        out_videos = []
        for i in range(len(self.fragments)):
            in_video, start, end, title = self.fragments[i]
            out_video = f'{title}.mp4'
            out_video = os.path.join(cut_dir, f'{title}.mp4')
            out_videos.append(out_video)
            cmd = f"ffmpeg -i {in_video} -ss {start} -to {end} -c copy {out_video}"
            status = os.system(cmd)
            print(f"{i}: Exit code: {status}")
        return out_videos

    # merge a list of videos into a single video
    def merge(self, in_videos:list, title:str = 'merged_video.mp4', merge_dir:str='merge'):
        if len(in_videos) <= 1:
            print('no enough videos to be merged')
            return
        os.makedirs(merge_dir, exist_ok=True)
        tmp = 'merge.txt'
        with open(tmp, 'w+') as f:
            for video in in_videos:
                print(video)
                f.write(f'file {video}\n')
        out_video = os.path.join(merge_dir, f'{title}.mp4')
        cmd = f"ffmpeg -f concat -safe 0 -i {tmp} -c copy {out_video}"
        print(cmd)
        status = os.system(cmd)
        print(f"Exit code: {status}")
        return


tool = VideoCutMerge()

# cut video
cut_task_path = 'task.txt'
## loading all cutting task 
tool.load_cut_task(cut_task_path) 
print(f'tasks = {tool.fragments}')
## cutting
out_videos = tool.cut() 
print(f'out_videos = {out_videos}')

# merge video
tool.merge(out_videos, title='wedding_1.mp4')