import tkinter as ttk
from PIL import Image, ImageTk

class AnimatedGIFLabel(ttk.Label):
    '''
    Helps our precious duck move.
    '''
    def __init__(self, master, gif_path):
        self.gif = Image.open(gif_path)
        self.gif_frames = []
        self.delay = self.gif.info.get('duration', 100)
        self.current_frame = 0
        super().__init__(master, bg='black')  # Set background color

        self.load_frames()
        self._animate()

    def load_frames(self):
        try:
            while True:
                frame = Image.new("RGBA", self.gif.size)
                frame.paste((255, 255, 255, 0), (0, 0, self.gif.size[0], self.gif.size[1]))  # Clear the frame
                frame.paste(self.gif, (0, 0), self.gif.convert("RGBA"))
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            pass

    def _animate(self):
        self.config(image=self.gif_frames[self.current_frame])
        self.current_frame += 1
        if self.current_frame >= len(self.gif_frames):
            self.current_frame = 0
        self.after(self.delay, self._animate)
        