import sys
import os
from ctypes import Structure, c_int32, c_int, c_char_p,\
                   create_string_buffer, memmove,\
                   c_void_p, POINTER, byref, c_double, cdll
from ctypes.util import find_library
from kivy.core.image import ImageData
from kivy.graphics.texture import Texture

current_dir = os.path.dirname(__file__)

class PdfPopplerException(Exception):
    pass

class PdfBase(object):
    def __init__(self, filename):
        self._cache_texture = {}
        self._cache_image = {}
        self.filename = filename
        self.open()

    def __del__(self):
        self.close()

    def open(self):
        raise NotImplemented()

    def close(self):
        raise NotImplemented()

    def get_n_pages(self):
        raise NotImplemented()

    def get_page_size(self, index):
        raise NotImplemented()

    def render_page(self, index):
        raise NotImplemented()

    def get_page_texture(self, index, zoom=1):
        if not (index, zoom) in self._cache_texture:
            self._cache_texture[(index, zoom)] = self.render_page(index, zoom)
        return self._cache_texture[(index, zoom)]


class PdfPoppler(PdfBase):

    l_poppler   = None
    l_cairo     = None
    l_gdk       = None

    def __init__(self, *largs, **kwargs):
        self._doc = None
        self._init_poppler()
        super(PdfPoppler, self).__init__(*largs, **kwargs)

    def _init_poppler(self):
        if self.l_poppler is not None:
            return

        if sys.platform in ('win32', 'cygwin'):
            filename = 'libpoppler-glib-4.dll'
            #filename = os.path.join(current_dir, filename)
            self.l_poppler = cdll.LoadLibrary(filename)
        elif sys.platform in ('darwin', ):
            filename = '/usr/local/lib/libpoppler-glib.dylib'
            self.l_poppler = cdll.LoadLibrary(filename)
        else:
            filename = find_library('poppler-glib')
            if filename is None:
                raise PdfPopplerException('Unable to found poppler-glib library')
            self.l_poppler = cdll.LoadLibrary(filename)
        if self.l_poppler is None:
            raise PdfPopplerException('Unable to load poppler-glib library')

        self.l_poppler.poppler_get_version.restype = c_char_p
        self.l_poppler.poppler_document_get_n_pages.restype = c_int
        self.l_poppler.poppler_document_get_n_pages.argtypes = [c_void_p]
        self.l_poppler.poppler_document_get_page.restype = c_void_p
        self.l_poppler.poppler_document_get_page.argtypes = [c_void_p, c_int]
        self.l_poppler.poppler_page_get_size.restype = None
        self.l_poppler.poppler_page_get_size.argtypes = [c_void_p, c_void_p, c_void_p]
        self.l_poppler.poppler_document_new_from_file.restype = c_void_p
        self.l_poppler.poppler_document_get_page.restype = c_void_p
        self.l_poppler.poppler_page_render.restype = None
        self.l_poppler.poppler_page_render.argtypes = [c_void_p, c_void_p]

        if sys.platform in ('win32', 'cygwin'):
            filename = 'libgobject-2.0-0.dll'
            self.l_gobject = cdll.LoadLibrary(filename)
        else:
            self.l_gobject = self.l_poppler

        print 'type init'
        self.l_gobject.g_type_init()
        print 'type init done'

        backend = self.l_poppler.poppler_get_backend()

        print 'PdfPoppler: using version', self.l_poppler.poppler_get_version()
        print 'PdfPoppler: backend is', backend

        if backend == 2: # Cairo
            self._init_poppler_cairo()
        elif backend == 1: # GdkPixbuf
            self._init_poppler_gdk()
        else:
            raise PdfPopplerException('Unknown backend number %d' % backend)

    def _init_poppler_cairo(self):
        print 'PdfPoppler: use Cairo'
        self.l_cairo = self.l_poppler
        self.l_cairo.cairo_create.restype = c_void_p
        self.l_cairo.cairo_create.argtypes = [c_void_p]
        self.l_cairo.cairo_destroy.restype = None
        self.l_cairo.cairo_destroy.argtypes = [c_void_p]
        self.l_cairo.cairo_image_surface_create.restype = c_void_p
        self.l_cairo.cairo_image_surface_create.argtypes = [c_int, c_int, c_int]
        self.l_cairo.cairo_image_surface_get_data.restype = c_void_p
        self.l_cairo.cairo_image_surface_get_data.argtypes = [c_void_p]
        self.l_cairo.cairo_surface_destroy.restype = None
        self.l_cairo.cairo_surface_destroy.argtypes = [c_void_p]
        self.l_cairo.cairo_scale.restype = None
        self.l_cairo.cairo_scale.argtypes = [c_void_p, c_double, c_double]

    def _init_poppler_gdk(self):
        print 'PdfPoppler: use GDK'
        if sys.platform in ('win32', 'cygwin'):
            filename = 'libgdk_pixbuf-2.0-0.dll'
            #filename = os.path.join(current_dir, filename)
            self.l_gdk = cdll.LoadLibrary(filename)
        else:
            self.l_gdk = self.l_poppler
        self.l_gdk.gdk_pixbuf_new.restype = c_void_p

    def open(self):
        class GError(Structure):
            _fields_ = [('domain', c_int32),
                        ('code', c_int),
                        ('message', c_char_p)]

        filename = 'file://'
        if sys.platform in ('win32', 'cygwin'):
            filename += '/'
        filename += self.filename

        error = POINTER(GError)()
        self.l_poppler.poppler_document_new_from_file.argtypes = [
            c_char_p, c_char_p, c_void_p]
        self._doc = self.l_poppler.poppler_document_new_from_file(
                c_char_p(filename), None, byref(error))
        if self._doc is None:
            raise PdfPopplerException(str(error.contents.message))

    def close(self):
        pass

    def get_n_pages(self):
        return int(self.l_poppler.poppler_document_get_n_pages(self._doc))

    def get_page_size(self, index):
        w = c_double(0)
        h = c_double(0)

        page = self.l_poppler.poppler_document_get_page(self._doc, index)
        assert( page is not None )

        self.l_poppler.poppler_page_get_size(page, byref(w), byref(h))
        return ( w.value, h.value )

    def render_page(self, index, zoom=1):
        w, h = map(int, self.get_page_size(index))
        w, h = map(lambda x: x * zoom, (w, h))

        print 'render1', index
        page = self.l_poppler.poppler_document_get_page(self._doc, index)
        print 'render2', page
        assert( page is not None )

        # use cairo ?
        if self.l_cairo is not None:

            # create a cairo surface
            # first argument 0 is ARGB32
            surface = self.l_cairo.cairo_image_surface_create(0, w, h)
            assert( surface is not None )

            # create cairo context
            context = self.l_cairo.cairo_create(surface)
            assert( context is not None )

            # apply zoom
            print 'apply scale'
            self.l_cairo.cairo_scale(context, c_double(zoom), c_double(zoom))

            # render to cairo
            print 'render page'
            self.l_poppler.poppler_page_render(page, context)

            # dump cairo to texture
            print 'render to texture'
            data = self.l_cairo.cairo_image_surface_get_data(surface)
            print 'got', type(data), data
            size = int(4 * w * h)
            print 'create string buffer', size
            buf = create_string_buffer(size)
            memmove(buf, data, size)

            # release cairo
            print 'destroy surface'
            self.l_cairo.cairo_surface_destroy(surface)
            print 'destroy context'
            self.l_cairo.cairo_destroy(context)
            print 'done!'

        # use gdk ?
        else:

            # 1: GDK_COLORSPACE_RGB (0)
            # 2: has_alpha (1)
            # 3: bit per samples
            print 'render3'
            self.l_gdk.gdk_pixbuf_new.restype = c_void_p
            surface = self.l_gdk.gdk_pixbuf_new(0, 1, 8, w, h)
            print 'render4'

            assert( surface is not None )

            # render to pixbuf (fix 6 arg)
            print 'render5'
            self.l_poppler.poppler_page_render_to_pixbuf.argtypes = [
                    c_void_p, c_int, c_int, c_int, c_int, c_double, c_int, c_void_p]
            self.l_poppler.poppler_page_render_to_pixbuf(page, 0, 0,
                    w, h, zoom, 0, surface)
            print 'render6'

            # get data
            class GdkPixdata(Structure):
                _fields_ = [('magic', c_int),
                        ('length', c_int),
                        ('pixdata_type', c_int),
                        ('rowstride', c_int),
                        ('width', c_int),
                        ('height', c_int),
                        ('pixel_data', c_void_p)]

            pixdata = (GdkPixdata)()

            # get a pixdata
            print 'render7'
            self.l_gdk.gdk_pixdata_from_pixbuf.argtypes = [
                    c_void_p, c_void_p, c_int]
            self.l_gdk.gdk_pixdata_from_pixbuf(byref(pixdata), surface, 0)
            print 'render8'

            # convert to buffer
            size = int(4 * w * h)
            buf = create_string_buffer(size)
            memmove(buf, pixdata.pixel_data, size)
            print 'render9'

            # unref
            self.l_gobject.g_object_unref(surface)
            print 'render10'

        # picking only RGB
        print 'create texture'
        im = ImageData(w, h, 'rgba', buf.raw)
        texture = Texture.create_from_data(im, mipmap=True)
        print 'done !'
        texture.flip_vertical()

        return texture

Pdf = PdfPoppler

if __name__ == '__main__':
    import os
    from kivy.uix.image import Image
    from kivy.factory import Factory
    from kivy.core.window import Window
    from kivy.properties import ObjectProperty, StringProperty, NumericProperty
    from kivy.base import runTouchApp
    from kivy.lang import Builder

    curdir = os.path.dirname(__file__)
    if curdir == '':
        curdir = os.getcwd()
    filename = os.path.join(curdir, 'media/bonjour/edt_tc2.pdf')

    class PdfWidget(Image):
        pdf = ObjectProperty(None)
        source = StringProperty(None)
        pages_count = NumericProperty(0)
        page = NumericProperty(0)

        def texture_update(self, *largs):
            # avoid texture update from Image
            pass

        def on_source(self, instance, value):
            self.pdf = Pdf(value)
            self.pages_count = self.pdf.get_n_pages()
            # force triggering page and check for min/max
            page = self.page
            self.page = -1
            self.page = page

        def on_page(self, instance, value):
            if value < 0 or value >= self.pages_count:
                self.page = max(0, min(value, self.pages_count - 1))
                return
            if self.pdf is None:
                return
            self.texture = self.pdf.get_page_texture(value, 2)

    Factory.register('PdfWidget', cls=PdfWidget)


    # add white background for pdfwidget
    # + create tiny ui for demoing the widget
    root = Builder.load_string('''
<PdfWidget>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

<PdfReaderUI>:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 50
        Button:
            text: '<< Previous'
            on_release: pdf.page -= 1
        Label:
            text: '%d / %d' % (pdf.page+1, pdf.pages_count)
            size_hint_x: 3
        Button:
            text: 'Next >>'
            on_release: pdf.page += 1
    FloatLayout:
        Scatter:
            size_hint: None, None
            size: pdf.texture_size
            canvas:
                Color:
                    rgb: 1, 0, 0
                Rectangle:
                    size: self.size
            PdfWidget:
                id: pdf
                source: root.source
                size: self.texture_size
''')

    # make a simple test
    from kivy.uix.boxlayout import BoxLayout
    class PdfReaderUI(BoxLayout):
        source = StringProperty(None)
    runTouchApp(PdfReaderUI(source=filename))
