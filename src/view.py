from gi import require_version
require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GLib
from PIL import Image
import io
import math

class View:


    class __View:

        def __init__(self, tree_view, title, album, artist, genre, cover, track, year, length, size):
            '''
            Here, we initiliase the widget we are going to use in the future.
            '''

            self.tree_view = tree_view
            self.title = title
            self.album = album
            self.artist = artist
            self.genre = genre
            self.cover = cover
            self.track = track
            self.year = year
            self.length = length
            self.size = size
            # The size of the cover
            self.cover_width = 300
            self.cover_height = 300

        def erase(self):
            '''
            We erase value written in the GtkEntry of each of those tags
            '''
            self.genre.set_text("")
            self.album.set_text("")
            self.title.set_text("")
            self.artist.set_text("")
            self.year.set_text("")
            self.track.set_text("")


        def set_editibility_title(self, multiple_rows, title):
            if multiple_rows == 1 :
                self.title.set_text("")
                self.title.set_editable(0)
            else :
                self.title.set_editable(1)
                self.title.set_text(title)

        def set_editability_size(self, multiple_rows, size):
            if multiple_rows == 1 :
                self.size.set_text("")
            else :
                self.size.set_text(size)

        def set_editability_length(self, multiple_rows, length):
            if multiple_rows == 1 :
                self.length.set_text("")
            else :
                self.length.set_text(length)


        def show_cover_from_bytes(self,bytes_file):
            with  Image.open(io.BytesIO(bytes_file)) as img :
                glibbytes = GLib.Bytes.new(img.tobytes())

                width = img.width  ##The best fix i could find for the moment
                height = img.height
                if glibbytes.get_size() < width * height * 3 :
                     width = math.sqrt(glibbytes.get_size()/3)
                     height = math.sqrt(glibbytes.get_size()/3)

                pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(glibbytes, # TODO ERROR HAPPENS WITH SOME COVER
                                                        GdkPixbuf.Colorspace.RGB,
                                                        False,
                                                        8,
                                                        width,
                                                        height,
                                                        len(img.getbands())*img.width)

                pixbuf = pixbuf.scale_simple(self.cover_width, self.cover_height, GdkPixbuf.InterpType.BILINEAR)

                self.cover.set_from_pixbuf(pixbuf)


        def show_cover_from_file(self,namefile):
            with  Image.open(name_file) as img :
                glibbytes = GLib.Bytes.new(img.tobytes())

                pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(glibbytes,
                                                        GdkPixbuf.Colorspace.RGB,
                                                        False,
                                                        8,
                                                        img.width,
                                                        img.height,
                                                        len(img.getbands())*img.width)

                pixbuf = pixbuf.scale_simple(self.cover_width, self.cover_height, GdkPixbuf.InterpType.BILINEAR)

                self.cover.set_from_pixbuf(pixbuf)



        def show(self,tagdico, multiple_rows):

            # We show those tags uniquely if there ais only one row selected #TODO is it reallly usefull ? I don't think so
            self.set_editibility_title(multiple_rows,tagdico["title"]["value"])
            self.set_editability_size(multiple_rows,tagdico["size"]["value"])
            self.set_editability_length(multiple_rows,tagdico["length"]["value"])

            # We show the tag currently in tagdico
            self.genre.set_text(tagdico["genre"]["value"])
            self.album.set_text(tagdico["album"]["value"])
            self.artist.set_text(tagdico["artist"]["value"])
            self.year.set_text(tagdico["year"]["value"])
            self.track.set_text(tagdico["track"]["value"])


            if tagdico["cover"]["value"] != "": # A test to handle if there is a cover
                if len(tagdico["cover"]["value"])>100 : # A test to detect bytes file
                    self.show_cover_from_bytes(tagdico["cover"]["value"])
                else:
                    self.show_cover_from_file(tagdico["cover"]["value"])
            else :

                self.cover.set_from_icon_name('gtk-missing-image',6)


        def add_column(self, name):
            '''
            A function to add a new column in the left panel treen useless in the code
            for the moment
            '''
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(name, renderer, text=0)
            self.tree_view.append_column(column)



    __instance = None

    def __init__(self, tree_view, title, album, artist, genre, cover, track, year, length, size):
        """ Virtually private constructor. """
        if View.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            View.__instance = View.__View(tree_view, title, album, artist, genre, cover, track, year, length, size)


    @staticmethod
    def getInstance():
        """ Static access method. """
        if View.__instance == None:
            View(None,None,None,None,None, None, None, None, None, None)
        return View.__instance
