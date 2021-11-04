# Bravo pour avoir ouvert ce fichier ! C’est super d’être curieux
# et de vouloir comprendre comment le code donné fonctionne

import matplotlib.pyplot as plt
from IPython.display import HTML, display, Video
import tempfile
import matplotlib.animation as animation
from pathlib import Path


def display_env(env, ax=None):
    if ax is None:
        ax = plt.gca()
    img = env.render("rgb_array")
    ax.imshow(img)
    ax.set_axis_off()
    return ax


class EnvVideoRecorder:
    def __init__(self) -> None:
        self.imgs = []
        self.tempdir = tempfile.TemporaryDirectory()
        self.video_count = 0
    
    def __del__(self):
        self.tempdir.cleanup()

    def add_record(self, env):
        self.imgs.append(env.render("rgb_array"))
    
    def clear_records(self):
        self.imgs = []
    
    def show_anim(self):
        anim = self.build_anim()
        display(HTML(anim.to_jshtml()))
        plt.close()
    
    
    def show_mp4(self):
        raise NotImplementedError("Not fully functional")
        videopath = Path(self.tempdir.name).as_posix() + f"/video{self.video_count}.mp4"
        self.video_count += 1
        self.save_mp4(videopath)
        display(Video(videopath))


    def build_anim(self):
        fig = plt.figure()
        ax = fig.gca()
        ims = []
        for i, true_img in enumerate(self.imgs):
            im = ax.imshow(true_img, animated=True)
            if i == 0:
                ax.imshow(true_img)
            ims.append([im])
            
        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat=False)
        return ani
    
    
    def save_mp4(self, path):
        if not path.endswith(".mp4"):
            raise ValueError("Path must end with .mp4")
        ani = self.build_anim()
        ani.save(path)