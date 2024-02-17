import numpy as np

from .. import _api, cbook, transforms
from . import backend_agg, backend_gtk3
from .backend_gtk3 import Gtk, _BackendGTK3

import cairo  # Presence of cairo is already checked by _backend_gtk.


class FigureCanvasGTK3Agg(backend_agg.FigureCanvasAgg,
                          backend_gtk3.FigureCanvasGTK3):
    def __init__(self, figure):
        super().__init__(figure=figure)
        self._bbox_queue = []

    def on_draw_event(self, widget, ctx):
        scale = self.device_pixel_ratio
        allocation = self.get_allocation()
        w = allocation.width * scale
        h = allocation.height * scale

        if not len(self._bbox_queue):
            Gtk.render_background(
                self.get_style_context(), ctx,
                allocation.x, allocation.y,
                allocation.width, allocation.height)
            bbox_queue = [transforms.Bbox([[0, 0], [w, h]])]
        else:
            bbox_queue = self._bbox_queue

        for bbox in bbox_queue:
            x = int(bbox.x0)
            y = h - int(bbox.y1)
            width = int(bbox.x1) - int(bbox.x0)
            height = int(bbox.y1) - int(bbox.y0)

            buf = cbook._unmultiplied_rgba8888_to_premultiplied_argb32(
                np.asarray(self.copy_from_bbox(bbox)))
            image = cairo.ImageSurface.create_for_data(
                buf.ravel().data, cairo.FORMAT_ARGB32, width, height)
            image.set_device_scale(scale, scale)
            ctx.set_source_surface(image, x / scale, y / scale)
            ctx.paint()

        if len(self._bbox_queue):
            self._bbox_queue = []

        return False

    def blit(self, bbox=None):
        # If bbox is None, blit the entire canvas to gtk. Otherwise
        # blit only the area defined by the bbox.
        if bbox is None:
            bbox = self.figure.bbox

        scale = self.device_pixel_ratio
        allocation = self.get_allocation()
        x = int(bbox.x0 / scale)
        y = allocation.height - int(bbox.y1 / scale)
        width = (int(bbox.x1) - int(bbox.x0)) // scale
        height = (int(bbox.y1) - int(bbox.y0)) // scale

        self._bbox_queue.append(bbox)
        self.queue_draw_area(x, y, width, height)


@_api.deprecated("3.6", alternative="backend_gtk3.FigureManagerGTK3")
class FigureManagerGTK3Agg(backend_gtk3.FigureManagerGTK3):
    pass


@_BackendGTK3.export
class _BackendGTK3Cairo(_BackendGTK3):
    FigureCanvas = FigureCanvasGTK3Agg
