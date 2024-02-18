#! /usr/bin/env python3
#
# Copyright (C) 2023  Michael Gale
# This file is part of the cq-gridfinity python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Gridfinity Rugged Boxes

import cadquery as cq
from cadquery.selectors import StringSyntaxSelector
from cqkit import (
    HasXCoordinateSelector,
    HasYCoordinateSelector,
    HasZCoordinateSelector,
    VerticalEdgeSelector,
    EdgeLengthSelector,
    RadiusSelector,
    FlatEdgeSelector,
)
from cqkit.cq_helpers import (
    rounded_rect_sketch,
    recentre,
    composite_from_pts,
    rotate_x,
    rotate_y,
    rotate_z,
    size_2d,
    size_3d,
    bounds_3d,
)
from cqkit import Ribbon
from cqgridfinity import *
from .gf_helpers import *


class GridfinityRuggedBox(GridfinityObject):
    def __init__(self, length_u, width_u, height_u, **kwargs):
        super().__init__()
        self.length_u = length_u
        self.width_u = width_u
        self.height_u = height_u
        self.lid_height = 10
        self.wall_vgrooves = True
        self.front_handle = True
        self.stackable = True
        self.side_clasps = True
        self.lid_baseplate = True
        self.inside_baseplate = True
        self.side_handles = True
        self.front_label = True
        self.label_length = None
        self.label_height = None
        self.label_th = GR_LABEL_TH
        self.back_feet = True
        self.hinge_width = GR_HINGE_SZ
        self.hinge_bolted = False
        self.box_color = cq.Color(0.25, 0.25, 0.25)
        self.lid_color = cq.Color(0.25, 0.5, 0.75)
        self.handle_color = cq.Color(0.75, 0.5, 0.25)
        self.latch_color = cq.Color(0.75, 0.5, 0.25)
        self.hinge_color = cq.Color(0.75, 0.5, 0.25)
        self.label_color = cq.Color(0.7, 0.7, 0.7)
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v

    def check_dimensions(self):
        """Verifies that the specified box dimensions are within specification."""
        assert self.length_u >= 3
        assert self.width_u >= 3
        assert self.height_u >= 4

    @property
    def box_length(self):
        return self.length_u * GRU + 2 * GR_RBOX_WALL

    @property
    def int_length(self):
        return self.length_u * GRU

    @property
    def box_width(self):
        return self.width_u * GRU + 2 * GR_RBOX_WALL

    @property
    def int_width(self):
        return self.width_u * GRU

    @property
    def clasp_pos(self):
        return self.int_length / 2 - GRU2, self.int_width / 2 - GRU2

    @property
    def box_height(self):
        return self.height_u * GRHU + 3

    @property
    def clasp_heights(self):
        h0 = GR_RIB_CTR / 2 + GR_RIB_L / 2
        h1 = h0 + GR_RIB_CTR
        return [GR_RIB_L / 2, self.box_height - h0, self.box_height - h1]

    @property
    def side_clasp_centres(self):
        xo = self.box_length / 2 + GR_RBOX_CHAN_D / 2
        yo = self.clasp_pos[1]
        return [(-xo, yo, 0), (xo, yo, 0), (-xo, -yo, 0), (xo, -yo, 0)]

    @property
    def front_clasp_centres(self):
        xo = self.clasp_pos[0]
        yo = self.box_width / 2 + GR_RBOX_CHAN_D / 2
        return [(-xo, -yo, 0), (xo, -yo, 0)]

    @property
    def hinge_centres(self):
        xo = self.box_length / 2 - GR_HINGE_CTR
        yo = self.box_width / 2 + GR_RBOX_CWALL - GR_RBOX_WALL
        zo = self.box_height
        return [(-xo, yo, zo), (xo, yo, zo)]

    @property
    def align_centres(self):
        ro = GR_RBOX_CHAN_D / 2 - GR_REG_W / 2
        xo, xc = self.box_length / 2 - GRU, self.box_length / 2 + ro
        yo, yc = self.box_width / 2 - GRU, self.box_width / 2 + ro
        pts = [
            (-xo, -yc, 0),
            (xo, -yc, 0),
            (-xc, -yo, 0),
            (xc, -yo, 0),
            (-xc, yo, 0),
            (xc, yo, 0),
        ]
        rots = [0, 0, 90, 90, 90, 90]
        return pts, rots

    @property
    def right_qtr_centre(self):
        return (
            self.box_length / 2 - GR_RBOX_WALL / 2 + 0.125,
            -self.box_width / 2 + GR_RBOX_WALL / 2 - 0.125,
            self.box_height,
        )

    @property
    def left_qtr_centre(self):
        return -self.right_qtr_centre[0], *self.right_qtr_centre[1:]

    @property
    def bottom_qtr_centres(self):
        return self.qtr_centres(tol=0.25)

    def qtr_centres(self, tol=0.25, at_height=0, front=True, back=True):
        xo = self.box_length / 2 - GR_RBOX_WALL / 2 + tol
        yo = self.box_width / 2 - GR_RBOX_WALL / 2 + tol
        qd = {}
        if front:
            qd["br"] = (xo, -yo, at_height)
            qd["bl"] = (-xo, -yo, at_height)
        if back:
            qd["tr"] = (xo, yo, at_height)
            qd["tl"] = (-xo, yo, at_height)
        return qd

    @property
    def long_enough_for_handle(self):
        return self.right_handle_centre[0] > GRU / 2

    @property
    def right_handle_centre(self):
        zo = (self.box_height + self.lid_height) / 2
        if (zo + GR_HANDLE_SZ / 2) > self.box_height:
            zo = self.box_height / 2
        return (
            self.box_length / 2 - GR_HANDLE_OFS,
            -self.box_width / 2,
            zo,
        )

    @property
    def left_handle_centre(self):
        return -self.right_handle_centre[0], *self.right_handle_centre[1:]

    @property
    def back_corner_centres(self):
        xo = self.box_length / 2 - GR_RBOX_BACK_L / 2 + GR_RBOX_CWALL - GR_RBOX_WALL
        yo = self.box_width / 2 - GR_RBOX_CORNER_W / 2 + GR_RBOX_CWALL - GR_RBOX_WALL
        return [(-xo, yo, 0), (xo, yo, 0)]

    @property
    def front_corner_centres(self):
        xo = self.box_length / 2 - GR_RBOX_FRONT_L / 2 + GR_RBOX_CWALL - GR_RBOX_WALL
        yo = -self.back_corner_centres[0][1]
        return [(-xo, yo, 0), (xo, yo, 0)]

    @property
    def label_centre(self):
        zo = self.left_handle_centre[2]
        zt = zo + self.label_size()[1] / 2
        # ensure the front label fits vertically
        if zt > self.box_height:
            zo = self.box_height / 2
        return (0, -self.box_width / 2, zo)

    def label_size(self, as_insert=False, as_aperture=False, tol=0):
        # use provided label size if applicable otherwise auto size
        if self.label_length is not None:
            length = self.label_length
        else:
            length = self.box_length - 2 * GR_RBOX_CORNER_W + (GR_RBOX_CWALL) / 2
        if self.label_height is not None:
            height = self.label_height
        else:
            height = GR_LABEL_H
        # ensure the label is not too tall
        if height >= self.box_height:
            height = self.box_height - 5
        # trim label size if handles are enabled
        if self.front_handle and self.long_enough_for_handle:
            length = length - 2 * (GR_HANDLE_SEP + GR_HANDLE_W)
        # return the desired size variant
        if as_insert:
            length -= 5
        if as_aperture:
            length -= 8
            height -= 8
        return length - 2 * tol, height - 2 * tol

    def body_shell(self, as_lid=False):
        """General purpose render function for both the box and the lid."""
        height = self.box_height if not as_lid else self.lid_height
        # render overall box shape
        rs = rounded_rect_sketch(self.box_length, self.box_width, GR_RAD)
        r = cq.Workplane("XY").placeSketch(rs).extrude(height)
        # back corners
        rc = cq.Workplane("XY").rect(GR_RBOX_BACK_L, GR_RBOX_CORNER_W).extrude(height)
        r = r.union(composite_from_pts(rc, self.back_corner_centres))
        # front corners
        rc = cq.Workplane("XY").rect(GR_RBOX_FRONT_L, GR_RBOX_CORNER_W).extrude(height)
        r = r.union(composite_from_pts(rc, self.front_corner_centres))
        # fillet external edges
        vs = VerticalEdgeSelector()
        cs = (
            StringSyntaxSelector("<X and <Y")
            + StringSyntaxSelector(">X and >Y")
            + StringSyntaxSelector("<X and >Y")
            + StringSyntaxSelector(">X and <Y")
        )
        r = r.edges(vs - cs).fillet(GR_RBOX_RAD).edges(cs).fillet(GR_RBOX_CRAD)

        if self.stackable or as_lid:
            # bottom stacking mates
            for k, v in self.qtr_centres(back=not as_lid).items():
                rq = quarter_circle(
                    GR_BREG_R0, GR_BREG_R1, GR_REG_H + 0.5, k, chamf=0, ext=0.25
                )
                r = r.cut(rq.translate(v))
            pts, rots = self.align_centres
            for pt, rot in zip(pts, rots):
                rc = chamf_rect(GR_REG_L, GR_REG_W, GR_REG_H, angle=rot)
                r = r.cut(rc.translate(pt))

        # chamfer edges
        r = r.edges(">Z").chamfer(GR_RBOX_VCUT_D)

        # front lid overhang
        if as_lid:
            w = min(GR_LID_HANDLE_W, self.box_length - 2 * GR_RBOX_FRONT_L)
            r = r.union(self.lid_handle(width=w).translate((0, -self.box_width / 2, 0)))
            hw = w / 2
            vs = VerticalEdgeSelector([9]) & HasXCoordinateSelector([-hw, hw])
            r = r.edges(vs).fillet(2.5 - EPS)

        # chamfer edges
        r = r.edges("<Z").chamfer(GR_RBOX_VCUT_D)

        # chamfer cuts
        if self.wall_vgrooves:
            r = r.intersect(self.render_vcut())

        # add clasp features
        rc = self.clasp_cut(as_lid=as_lid)
        if self.side_clasps:
            for pt in self.side_clasp_centres:
                r = r.cut(rc.translate(pt))
                if pt[0] < 0:
                    r = r.union(
                        self.clasp_ribs(side="left", as_lid=as_lid).translate(pt)
                    )
                else:
                    r = r.union(
                        self.clasp_ribs(side="right", as_lid=as_lid).translate(pt)
                    )
        rc = rotate_z(rc, 90)
        for pt in self.front_clasp_centres:
            r = r.cut(rc.translate(pt))
            r = r.union(self.clasp_ribs(side="front", as_lid=as_lid).translate(pt))

        return r

    def render_vcut(self):
        """Renders a matching box shape with side v-cuts to intersect with main box."""
        xl = self.box_length + 2 * GR_RBOX_CWALL - 2 * GR_RBOX_WALL
        yl = self.box_width + 2 * GR_RBOX_CWALL - 2 * GR_RBOX_WALL
        lead_height = self.lid_height - GR_RBOX_VCUT_D
        mid_height = self.box_height - 2 * (self.lid_height + GR_RBOX_VCUT_D)
        cut_half = GR_RBOX_VCUT_D * SQRT2
        profile = [
            lead_height,
            (cut_half, 45),
            (cut_half, -45),
            mid_height,
            (cut_half, 45),
            (cut_half, -45),
            lead_height,
        ]
        rs = rounded_rect_sketch(xl, yl, GR_RBOX_CRAD)
        return self.extrude_profile(rs, profile)

    def lid_handle(self, width=None):
        """Renders the front overhanging handle lip for the lid."""
        width = width if width is not None else GR_LID_HANDLE_W
        l0, l1, h1 = 3, 5, 4
        h2 = self.lid_height - GR_RBOX_VCUT_D
        rs = (
            cq.Sketch()
            .segment((l0, 0), (-l1, 0))
            .segment((-l1, h1))
            .segment((l0, h2 + l0))
            .close()
            .assemble()
        )
        r = cq.Workplane("YZ").placeSketch(rs).extrude(width)
        hw = width / 2
        r = r.translate((-hw, 0, 0))
        vs = VerticalEdgeSelector([h1]) & HasXCoordinateSelector([-hw, hw])
        r = r.edges(vs).fillet(2.45).faces("<Z").shell(-2.5)
        vs = VerticalEdgeSelector(3) & HasYCoordinateSelector(-l1 + 2.5)
        r = r.edges(vs).fillet(1)
        rc = cq.Workplane("XY").rect(4 * hw, 4 * hw).extrude(self.lid_height)
        r = r.intersect(rc)
        return r

    def side_handle(self, width=None):
        """Renders the handles for the left and right box sides."""
        width = width if width is not None else GR_LID_HANDLE_W
        l0, l1, h1 = GR_RBOX_WALL, 7, 4
        l2 = GR_RBOX_WALL / 2
        h2 = self.lid_height - GR_RBOX_VCUT_D + 2
        # handle shape
        rs = (
            cq.Sketch()
            .segment((l0, 0), (-l1, 0))
            .segment((-l1, h1))
            .segment((l0, h2 + l0))
            .close()
            .assemble()
        )
        r = cq.Workplane("YZ").placeSketch(rs).extrude(width)
        # vertical under support
        rs = (
            cq.Sketch()
            .segment((l0, 0), (l0, -h2))
            .segment((0.75, -h2 + 1.5))
            .segment((-l1, 0.5))
            .segment((-l1, h1))
            .segment((l0, h2 + l0))
            .close()
            .assemble()
        )
        rw = cq.Workplane("YZ").placeSketch(rs).extrude(2.5)
        re = (
            cq.Workplane("XY")
            .rect(20, GR_RBOX_WALL)
            .extrude(50)
            .translate((l2, l2, -h2 - 5))
        )
        rw = rw.union(re)
        bs = EdgeLengthSelector(GR_RBOX_WALL) & HasYCoordinateSelector(
            0, min_points=2
        ) - HasZCoordinateSelector(">0")
        rw = rw.edges(bs).fillet(5)
        rw = rw.cut(
            cq.Workplane("XY")
            .rect(20, GR_RBOX_WALL)
            .extrude(50)
            .translate((l2, l2, -h2 - 5))
        )
        rh = []
        for coord in [[0, 2.5], [0], [2.5]]:
            bs = (
                VerticalEdgeSelector()
                & HasXCoordinateSelector(coord, min_points=2)
                & (HasYCoordinateSelector("<0"))
            )
            bs = bs - HasZCoordinateSelector(">4")
            rh.append(rw.edges(bs).chamfer(0.5))
        hw = width / 2
        r = r.faces("<Z").shell(-2.5)
        bs = (
            HasZCoordinateSelector(0, min_points=2)
            - EdgeLengthSelector("<%.1f" % (width - 2.5))
            - HasYCoordinateSelector(">=0")
        )
        r = r.edges(bs).chamfer(0.5).translate((-hw, 0, -2))
        r = r.union(rh[2].translate((-hw, 0, -2)))
        if width > GR_LID_HANDLE_W / 2:
            r = r.union(rh[0].translate((-l2, 0, -2)))
        r = r.union(rh[1].translate((hw - GR_RBOX_WALL, 0, -2)))
        vs = VerticalEdgeSelector([h1 - 0.5]) & HasXCoordinateSelector([-hw, hw])
        r = r.edges(vs).fillet(2)
        vs = VerticalEdgeSelector(2.9) & HasYCoordinateSelector(-l1 + GR_RBOX_WALL)
        r = r.edges(vs).fillet(1)
        rc = cq.Workplane("XY").rect(4 * hw, 4 * hw).extrude(self.lid_height + 2 * h2)
        rc = rc.translate((0, 0, -2 * h2))
        r = r.intersect(rc)
        return r

    def label_slot(self):
        """Renders the front label holder."""
        rs = rounded_rect_sketch(*self.label_size(), GR_RAD)
        r = self.extrude_profile(rs, [(GR_LABEL_SLOT_TH * SQRT2, 45)], workplane="XZ")
        rc = (
            cq.Workplane("XZ")
            .rect(*self.label_size(as_aperture=True))
            .extrude(GR_LABEL_SLOT_TH)
        )
        rc = rc.edges(EdgeLengthSelector(GR_LABEL_SLOT_TH)).chamfer(2.5)
        r = r.cut(rc)
        xl, yl = self.label_size(as_insert=True)
        xl -= 8
        rc = cq.Workplane("XZ").rect(xl, yl).extrude(GR_LABEL_SLOT_TH)
        r = r.cut(rc.translate((0, 0, 5)))
        rc = (
            cq.Workplane("XZ")
            .rect(*self.label_size(as_insert=True))
            .extrude(GR_LABEL_SLOT_TH / 2)
        )
        rc = rc.edges("|Y and <Z").fillet(GR_LABEL_SLOT_TH / 2)
        r = r.cut(rc.translate((0, 0, GR_LABEL_SLOT_TH)))

        # simple restraining ramps to prevent the label slipping out
        rc = cq.Workplane("XZ").rect(5, 2.5).extrude(1)
        rc = rc.edges("<Y").chamfer(1 - EPS)
        for pt in [(-xl / 4, 0, yl / 2 - 2.0), (xl / 4, 0, yl / 2 - 2.0)]:
            r = r.union(rc.translate(pt))
        return r

    def render_label(self):
        """Renders a label panel insert"""
        rs = rounded_rect_sketch(*self.label_size(tol=3), GR_RAD)
        r = cq.Workplane("XZ").placeSketch(rs).extrude(self.label_th)
        self._obj_label = "label"
        self._cq_obj = r
        return self._cq_obj

    def clasp_cut(self, as_lid=False):
        """Renders the vertical channel where the clasps / latch are installed."""
        height = GR_CLASP_SLIDE_D + 6 if as_lid else self.box_height
        w = GR_RBOX_CHAN_W + GR_CLASP_SLIDE_W
        rs = cq.Sketch().slot(GR_CLASP_SLIDE_D, GR_CLASP_SLIDE_W, angle=90)
        rs = cq.Workplane("XZ").placeSketch(rs).extrude(w).translate((0, w / 2, 0))
        rc = cq.Workplane("XY").rect(GR_RBOX_CHAN_D, GR_RBOX_CHAN_W).extrude(height)
        zo = -GR_CLASP_SLIDE_D / 2 + GR_CLASP_SLIDE_W / 2
        # ensure clasp channel is deep enough for box heights <6U
        height = max(height, GR_CLASP_SLIDE_D + 5.2)
        pts = [(0, 0, height + zo), (0, 0, zo)]
        return rc.union(composite_from_pts(rs, pts))

    def clasp_rib(self, chamfered=False):
        """Renders a single clasp rib feature."""
        r = cq.Workplane("XY").rect(GR_RIB_L, GR_RIB_W).extrude(GR_RIB_H)
        r = r.faces(">Z").edges("<X or >X").chamfer(1.0)
        if chamfered:
            rc = (
                cq.Workplane("XZ")
                .moveTo(0, 0)
                .lineTo(0, GR_RIB_H)
                .lineTo(GR_RIB_L / 6, GR_RIB_H)
                .close()
                .extrude(GR_RIB_W)
            )
            rc = rc.translate((-GR_RIB_L / 1.85, GR_RIB_W / 2, 0))
            r = r.cut(rc)
            rc = cq.Workplane("XY").rect(GR_RIB_L / 2, GR_RIB_W).extrude(GR_RIB_H / 3)
            rc = rc.faces(">Z").edges("<X or >X").chamfer(GR_RIB_H / 3 - EPS)
            rc = rc.translate((-GR_RIB_L / 2.33, 0, 0))
            r = r.union(rc)
        return r

    def clasp_ribs(self, side="left", as_lid=False):
        """Renders a group of clasp ribs for any side for both the box and lid."""
        y1 = GR_RIB_SEP / 2 + GR_RIB_W / 2
        y2 = y1 + GR_RIB_W + GR_RIB_GAP
        zo = -GR_RBOX_CHAN_D / 2
        pts = [(0, -y2, zo), (0, -y1, zo), (0, y1, zo), (0, y2, zo)]
        rh = composite_from_pts(self.clasp_rib(), pts)
        rc = composite_from_pts(self.clasp_rib(chamfered=True), pts)
        if self.stackable or as_lid:
            r = rh.translate((self.clasp_heights[0], 0, 0))
        if not as_lid:
            rc = composite_from_pts(rc, [(h, 0, 0) for h in self.clasp_heights[1:]])
            if not self.stackable:
                r = rc
            else:
                r = r.union(rc)
        r = rotate_y(r, -90)
        if side == "front":
            r = rotate_z(r, 90)
        elif side == "right":
            r = rotate_z(r, 180)
        return r

    def handle_mount(self, side="left"):
        """Mounting features for front handle"""

        def _bracket(small_hole=False, side="left"):
            l1 = GR_HANDLE_L1 / 2
            l2 = min(GR_HANDLE_L2 / 2, (self.box_height - 6) / 2)
            d2 = M3_DIAM / 2 if small_hole else M3_CLR_DIAM / 2
            rs = (
                cq.Sketch()
                .segment((0, 0), (-l2, 0))
                .segment((-l1, GR_HANDLE_H))
                .segment((l1, GR_HANDLE_H))
                .segment((l2, 0))
                .close()
                .assemble()
                .vertices(">Y")
                .vertices("<X or >X")
                .fillet(GR_RAD)
                .reset()
                .push([(0, GR_HANDLE_H / 2)])
                .circle(d2, mode="s")
            )
            r = cq.Workplane("YZ").placeSketch(rs).extrude(GR_HANDLE_W)
            if not small_hole:
                face = ">X" if side == "left" else "<X"
                r = (
                    r.faces(face)
                    .workplane()
                    .pushPoints([(0, GR_HANDLE_H / 2)])
                    .hole(M3_CB_DIAM, M3_CB_DEPTH)
                )
            r = r.union(cq.Workplane("XY").rect(50, 50).extrude(-1))
            bs = EdgeLengthSelector(GR_HANDLE_W) & HasZCoordinateSelector(0)
            r = r.edges(bs).fillet(GR_RAD)
            r = r.cut(cq.Workplane("XY").rect(50, 50).extrude(-1))
            r = r.faces(">Z").chamfer(0.75)
            return rotate_x(r, 90)

        h1 = _bracket(small_hole=True, side=side)
        h2 = _bracket(small_hole=False, side=side)
        xo = GR_HANDLE_SEP if side == "left" else -GR_HANDLE_SEP
        r = recentre(h1.union(h2.translate((xo, 0, 0))), "xz")
        return r

    def render_handle(self):
        """Renders the front handle"""
        self.check_dimensions()
        x2 = self.right_handle_centre[0]
        if not self.long_enough_for_handle:
            print("Rugged box length dimension too small to include a handle")
            return None
        wt, h, rh = GR_HANDLE_TH, GR_HANDLE_SZ, GR_HANDLE_RAD
        lt = (2 * x2) - 2 * rh
        ht = h - rh - wt / 2
        path = [
            ("start", {"position": (x2, h), "direction": -90, "width": wt}),
            ("line", {"length": ht}),
            ("arc", {"radius": rh, "angle": 90}),
            ("line", {"length": lt}),
            ("arc", {"radius": rh, "angle": 90}),
            ("line", {"length": ht}),
        ]
        cw = Ribbon("XZ", path)
        r = cw.render()
        r = r.extrude(wt).faces(">Z").edges("|X").fillet(wt / 2 - EPS)
        r = recentre(r.edges().chamfer(1), "XY")
        r = r.cut(
            cq.Workplane("YZ")
            .circle(M3_CLR_DIAM / 2)
            .extrude(8 * lt)
            .translate((-4 * lt, 0, h - M3_CLR_DIAM))
        )
        self._obj_label = "handle"
        self._cq_obj = r
        return self._cq_obj

    def render_back_foot(self):
        """Renders a corresponding rear foot the same depth as the hinge for standing
        the box vertically."""
        rs = cq.Sketch().slot(2 * GR_HINGE_OFFS, 2 * GR_HINGE_RAD, 0)
        rc = cq.Workplane("YZ").placeSketch(rs).extrude(self.hinge_width - 0.4)
        rc = recentre(rc)
        return rc.edges().chamfer(1).translate((0, 0, GR_HINGE_RAD))

    def hinge_mount(self):
        """Mounting cutout for hinge"""
        l1 = self.hinge_width + 2
        l2 = self.hinge_width
        l3 = (self.hinge_width - 2) / 2
        r = cq.Workplane("XY").rect(l1, GR_HINGE_W1).extrude(GR_HINGE_H1)
        r = r.translate((0, -GR_HINGE_W1 / 2, -GR_HINGE_H1))
        r2 = cq.Workplane("XY").rect(l2, GR_HINGE_W2).extrude(GR_HINGE_H2)
        r2 = r2.translate((0, -GR_HINGE_D - GR_HINGE_W2 / 2, -GR_HINGE_H2))
        bs = HasZCoordinateSelector(-GR_HINGE_H1) & EdgeLengthSelector(
            [l2, GR_HINGE_W2]
        )
        r = r.union(r2).edges(bs).edges(">Y or <X or >X").chamfer(0.75)
        r3 = (
            cq.Workplane("XY")
            .placeSketch(rounded_rect_sketch(l3, GR_HINGE_W3, 0.5))
            .extrude(GR_HINGE_H2)
        )
        xo = GR_HINGE_SEP / 2 + l3 / 2
        yo = -GR_HINGE_W1 - 1.2 - GR_HINGE_W3 / 2
        rh = self.hex_cut().translate(
            (0, 0, GR_HINGE_H2 - GR_HINGE_H1 - GR_HEX_H / 2 + GR_HINGE_SKEW)
        )
        for pt in [(-xo, yo, -GR_HINGE_H2), (xo, yo, -GR_HINGE_H2)]:
            r = r.union(r3.translate(pt))
            r = r.union(rh.translate(pt))
        return r

    def hex_cut(self, depth=None):
        """Hexagonal shaped latch for hinge attachment"""
        l1 = 2 if depth is None else 1.7
        l2 = 3.5 if depth is None else 3.0
        d = depth if depth is not None else 4.0
        h = GR_HEX_H if depth is None else GR_HEX_H - 0.4
        rs = (
            cq.Sketch()
            .segment((0, 0), (-l1, 0))
            .segment((-l2, h / 2))
            .segment((-l1, h))
            .segment((l1, h))
            .segment((l2, h / 2))
            .segment((l1, 0))
            .close()
            .assemble()
        )
        r = cq.Workplane("XZ").placeSketch(rs).extrude(d).translate((0, d, -h / 2))
        if depth is not None:
            r = r.edges("<Z and >Y").chamfer(depth - EPS)
        return r

    def render_latch(self):
        """Renders the latch element used to secure the box and the lid."""
        l2, w2, h2 = GR_LATCH_L / 2, GR_LATCH_W / 2, GR_LATCH_H / 2
        c2, th = GR_RIB_CTR / 2, 2.5
        hf = GR_LATCH_H - th
        r = cq.Workplane("XY").rect(GR_LATCH_L, GR_LATCH_W).extrude(GR_LATCH_H)
        r = r.edges("|Y").edges(">X").chamfer(1.0)
        rs = cq.Sketch().slot(10, GR_LATCH_H, 0)
        rc = cq.Workplane("XZ").placeSketch(rs).extrude(GR_LATCH_W)
        r = r.union(rc.translate((-l2 + 4.5, w2, h2)))
        rc = cq.Workplane("XY").rect(16, 15.6).extrude(10).edges("|Z").fillet(4.0)
        r = r.cut(rc.translate((-l2 - 8, 0, 0)))

        rc = cq.Workplane("XY").rect(5, GR_LATCH_W - 2.4).extrude(10)
        rc = rc.faces("<Z").edges("|X").fillet(1.5).edges("|Z").fillet(1.0)
        r = r.cut(rc.translate((l2, 0, 2.0))).edges().chamfer(0.25)

        rc = cq.Workplane("XY").rect(GR_LATCH_IL, GR_LATCH_IW).extrude(hf)
        for x in (-GR_RIB_CTR, 0, GR_RIB_CTR):
            r = r.cut(rc.translate((x - 1.25, 0, th)))
        r = r.faces(">Z").edges(EdgeLengthSelector(GR_LATCH_IW)).chamfer(1.5)
        r = r.faces(">Z").edges(EdgeLengthSelector(GR_LATCH_IL)).chamfer(0.25)

        rc = cq.Workplane("XY").rect(20, 2.4).extrude(hf)
        r = r.cut(rc.translate((0, 0, th)))
        r = r.faces(">Z").edges(EdgeLengthSelector(1.8)).edges("|X").chamfer(0.25)

        rc = cq.Workplane("XY").rect(8, 0.75).extrude(4.5)
        rc = rc.faces(">Z").edges("|Y").chamfer(1.5)
        bs = EdgeLengthSelector(">0.8") - HasZCoordinateSelector(0, min_points=2)
        rc = rc.edges(bs).chamfer(0.2)
        (_, _, _), (xm, _, _) = bounds_3d(r)

        for pt in [(x - 1.25, y, th) for x in (-c2, c2) for y in (-1.575, 1.575)]:
            r = r.union(rc.translate(pt))
        rl = rc.intersect(
            cq.Workplane("XY").rect(3.5, 1).extrude(7).translate((2.25, 0, 0))
        )
        rr = rc.intersect(
            cq.Workplane("XY").rect(3.5, 1).extrude(7).translate((-2.25, 0, 0))
        )
        for pt in [(-xm, y, th) for y in (-1.575, 1.575)]:
            r = r.union(rl.translate(pt))
        for pt in [(13.75, y, th) for y in (-1.575, 1.575)]:
            r = r.union(rr.translate(pt))

        rc = cq.Workplane("XZ").rect(2, 3.4).extrude(0.4)
        rc = rc.edges("<Y").chamfer(0.4 - EPS)

        xo = xm - self.lid_height
        r = r.union(rc.translate((xo, -w2, h2)))
        r = r.union(rotate_z(rc, 180).translate((xo, w2, h2)))

        rc = cq.Workplane("XZ").rect(6.0, 0.4).extrude(-1.5)
        r = r.cut(rc.translate((xo, -w2, h2 + 2.1)))
        r = r.cut(rc.translate((xo, -w2, h2 - 2.1)))
        r = r.cut(rc.translate((xo, w2 - 1.5, h2 + 2.1)))
        r = r.cut(rc.translate((xo, w2 - 1.5, h2 - 2.1)))
        r = (
            r.edges(HasYCoordinateSelector(-w2, min_points=2))
            .edges(EdgeLengthSelector([6.0, 0.4]))
            .chamfer(0.2 - EPS)
        )
        r = (
            r.edges(HasYCoordinateSelector(w2, min_points=2))
            .edges(EdgeLengthSelector([6.0, 0.4]))
            .chamfer(0.2 - EPS)
        )

        rc = cq.Workplane("XZ").circle(3.8 / 2).extrude(2).faces("<Y").chamfer(0.5)
        re = cq.Workplane("XY").rect(50, 50).extrude(20).translate((0, 0, -1.4))
        rc = rc.intersect(re)
        r = r.union(rc.translate((-17.45, -w2, h2)))
        r = r.union(rotate_z(rc, 180).translate((-17.45, w2, h2)))
        self._cq_obj = rotate_z(recentre(r, "xy"), -90)
        self._obj_label = "latch"
        return self._cq_obj

    def render_hinge(self, as_closed=False, section=None):
        """Renders the rear hinge."""
        tol = 0.25 / 2
        cl = 2 * (GR_HINGE_OFFS + GR_HINGE_D + GR_HINGE_W2 / 2)
        wh, dh = GR_HINGE_W2 - 0.4, GR_HINGE_H2 - 1
        ls, ws = cl / 2, GR_HINGE_H1 - 0.4
        h = self.hinge_width - 0.4
        h3 = h / 3
        ha, hb = h3 - tol, h3 + tol
        hc, hd = 2 * h3 - tol, 2 * h3 + tol
        cro, cri = 3.9, 3.5
        crb, crs = 4.5 / 2, 4.0 / 2
        ctr = (cl / 2 + wh / 2, -GR_HINGE_SKEW)

        def _bracket(side="left"):
            xo = wh / 2 if side == "left" else cl + wh / 2
            r = cq.Workplane("XY").rect(wh, dh).extrude(h).translate((xo, dh / 2, 0))
            xo = ls / 2 if side == "left" else cl + wh - ls / 2
            rc = cq.Workplane("XY").rect(ls, ws).extrude(h).translate((xo, ws / 2, 0))
            r = r.union(rc)
            bs = VerticalEdgeSelector() & HasYCoordinateSelector(ws)
            if side == "left":
                r = r.edges(VerticalEdgeSelector()).edges("<X and <Y").chamfer(1.0)
                bs = bs & HasXCoordinateSelector(wh)
            else:
                r = r.edges(VerticalEdgeSelector()).edges(">X and <Y").chamfer(1.0)
                bs = bs & HasXCoordinateSelector(cl)
            r = r.edges(bs).chamfer(1.1)
            r = r.faces(">Y").edges(EdgeLengthSelector(wh)).chamfer(1.5)
            return r

        rl = _bracket(side="left")
        for pt in [0, hc]:
            rl = rl.cut(chamf_cyl(cro, hb, 0).translate((*ctr, pt)))
        rr = _bracket(side="right")
        rr = rr.cut(chamf_cyl(cro, hd - ha, 0).translate((*ctr, ha)))

        bs = EdgeLengthSelector(">0.2") - EdgeLengthSelector([wh, h], tolerance=0.02)
        bs = bs - HasYCoordinateSelector(dh - 1.5, min_points=2)
        bs = bs - (RadiusSelector(cro) & HasZCoordinateSelector([ha, hb, hc, hd]))
        rl = rl.edges(bs).chamfer(0.5)
        rr = rr.edges(bs).chamfer(0.5)

        rl = rl.union(chamf_cyl(cri, hc - hb).translate((*ctr, hb)))
        if not self.hinge_bolted:
            rl = rl.cut(chamf_cyl(crb, hc - hb, 0).translate((*ctr, hb)))

        for pt in [0, hd]:
            rr = rr.union(chamf_cyl(cri, ha).translate((*ctr, pt)))
        if not self.hinge_bolted:
            rr = rr.union(chamf_cyl(crs, h, 0).translate((*ctr, 0)))
        else:
            rr = rr.cut(chamf_cyl(M3_DIAM / 2, h, 0).translate((*ctr, 0)))
            rl = rl.cut(chamf_cyl(M3_CLR_DIAM / 2, h, 0).translate((*ctr, 0)))
            rr = rr.cut(chamf_cyl(M3_CLR_DIAM / 2, ha, 0).translate((*ctr, h - ha)))
            rr = rr.cut(
                chamf_cyl(M3_CB_DIAM / 2, M3_CB_DEPTH, 0).translate(
                    (*ctr, h - M3_CB_DEPTH)
                )
            )
        rh = self.hex_cut(depth=GR_HEX_D)
        rx = recentre(rh)
        rh = rotate_x(rotate_z(rx, 90), 90)
        xo = cl + wh + GR_HEX_D / 2
        yo = GR_HINGE_H1 + GR_HEX_H / 2 - 2 * GR_HINGE_SKEW
        zo = GR_HINGE_SEP / 2 + (self.hinge_width - 2) / 4
        rl = rl.union(rh.translate((-GR_HEX_D / 2, yo, h / 2 - zo)))
        rl = rl.union(rh.translate((-GR_HEX_D / 2, yo, h / 2 + zo)))
        rh = rotate_x(rotate_z(rx, -90), 90)
        rr = rr.union(rh.translate((xo, yo, h / 2 - zo)))
        rr = rr.union(rh.translate((xo, yo, h / 2 + zo)))
        if as_closed:
            rl = rotate_z(rl.translate((-ctr[0], -ctr[1], 0)), 90)
            rr = rotate_z(rr.translate((-ctr[0], -ctr[1], 0)), -90)
        if section is not None:
            if section == "outer":
                r = rr
            else:
                r = rl
        else:
            r = rl.union(rr)
        self._cq_obj = r
        self._obj_label = "hinge"
        return self._cq_obj

    def render(self):
        """Renders the rugged box body shell."""
        self.check_dimensions()
        r = self.body_shell(as_lid=False)

        # hollow out
        rc = (
            cq.Workplane("XY")
            .placeSketch(rounded_rect_sketch(self.length, self.width, GR_RAD))
            .extrude(self.box_height - GR_RBOX_FLOOR)
        )
        r = r.cut(rc.translate((0, 0, GR_RBOX_FLOOR)))

        # add registration features
        pts, rots = self.align_centres
        for pt, rot in zip(pts, rots):
            rc = chamf_rect(
                GR_REG_L,
                GR_REG_W,
                GR_REG_H,
                angle=rot,
                z_offset=self.box_height,
                tol=0.75,
            )
            r = r.union(rc.translate(pt))

        rq = quarter_circle(GR_REG_R0, GR_REG_R1, GR_REG_H, "bl")
        r = r.union(rq.translate(self.left_qtr_centre))
        rq = quarter_circle(GR_REG_R0, GR_REG_R1, GR_REG_H, "br")
        r = r.union(rq.translate(self.right_qtr_centre))

        # add handle mounts
        if self.front_handle and self.long_enough_for_handle:
            r = r.union(
                self.handle_mount(side="left").translate(self.left_handle_centre)
            )
            r = r.union(
                self.handle_mount(side="right").translate(self.right_handle_centre)
            )

        # add hinge mounts
        rc = self.hinge_mount()
        for pt in self.hinge_centres:
            r = r.cut(rc.translate(pt))

        # add side handles
        if self.side_handles:
            w = min(GR_SIDE_HANDLE_W, self.box_width - 2 * GR_RBOX_CORNER_W)
            rh = self.side_handle(width=w)
            rl = rotate_z(rh, -90)
            rr = rotate_z(rh, 90)
            zo = self.box_height - self.lid_height
            r = r.union(rl.translate((-self.box_length / 2, 0, zo)))
            r = r.union(rr.translate((self.box_length / 2, 0, zo)))
            hw, l2 = w / 2, self.box_length / 2
            vs = HasXCoordinateSelector([-l2, l2]) & HasYCoordinateSelector([-hw, hw])
            r = r.edges("|Z").edges(vs).fillet(2.5)

        # add front label slot
        if self.front_label:
            r = r.union(self.label_slot().translate(self.label_centre))

        # back feet
        if self.back_feet:
            rc = self.render_back_foot()
            for pt in self.hinge_centres:
                r = r.union(rc.translate((pt[0], pt[1], 0)))

        # add baseplate
        if self.inside_baseplate:
            rb = GridfinityBaseplate(self.length_u, self.width_u, ext_depth=1.6)
            r = r.union(rb.render().translate((0, 0, GR_RBOX_FLOOR)))
            r = r.edges(FlatEdgeSelector(GR_RBOX_FLOOR)).chamfer(0.8)
        else:
            rb = self.extrude_profile(
                rounded_rect_sketch(self.length, self.width, GR_RAD), [GR_RBOX_WALL]
            )
            r = r.union(rb)
        self._cq_obj = r
        self._obj_label = "body"
        return self._cq_obj

    def render_lid(self):
        """Renders the rugged box lid."""
        self.check_dimensions()
        r = self.body_shell(as_lid=True)
        # add hinge mounts
        rc = rotate_y(self.hinge_mount(), 180)
        for pt in self.hinge_centres:
            r = r.cut(rc.translate((pt[0], pt[1], 0)))
        rs = rounded_rect_sketch(self.length - GR_TOL, self.width - GR_TOL, GR_RAD)

        if self.lid_baseplate:
            # hollow out top half
            rc = self.extrude_profile(rs, [self.lid_height - 0.5, (1.0, -45)])
            r = r.cut(rc)
            # add topside baseplate
            rb = GridfinityBaseplate(
                self.length_u, self.width_u, ext_depth=0.4, straight_bottom=True
            )
            rb = rb.render()
            r = r.union(rb.translate((0, 0, 4.7 - 0.4)))

        # hollow out bottom
        rs = rounded_rect_sketch(self.length, self.width, GR_RAD)
        r = r.cut(cq.Workplane("XY").placeSketch(rs).extrude(4.6))

        # add modified bottom extrusion with a looser fit
        rs = self.extrude_profile(
            rounded_rect_sketch(35, 35, 0.8), [(2.82, -22.1), (5, -45)]
        )
        rs = rs.faces(">Z").shell(-1.2)
        ra = composite_from_pts(rs, self.grid_centres)
        ra = ra.translate((-self.half_l, -self.half_w, 0))
        r = r.union(ra)
        r = r.edges(
            EdgeLengthSelector(33.4) & HasZCoordinateSelector(0, min_points=2)
        ).chamfer(0.75)

        # add optional stackable features
        if self.stackable:
            for k, v in self.qtr_centres(tol=0.125, at_height=self.lid_height).items():
                rq = quarter_circle(GR_REG_R0, GR_REG_R1, GR_REG_H, k)
                r = r.union(rq.translate(v))

        self._cq_obj = r
        self._obj_label = "lid"
        return self._cq_obj

    def render_accessories(self):
        """Render functional accessories which are installed to main box body."""
        margin = 8
        latch_count = 2
        if self.side_clasps:
            latch_count += 4
        rl = self.render_latch()
        sx, sy = size_2d(rl)
        pts = [(x * (sx + margin) + sx / 2, sy / 2, 0) for x in range(latch_count)]
        r = composite_from_pts(rl, pts)
        oy = sy + margin

        if self.front_handle:
            rh = recentre(rotate_x(self.render_handle(), -90))
            hsx, hsy, hsz = size_3d(rh)
            r = r.union(rh.translate((hsx / 2, oy + hsy / 2, hsz / 2)))
            oy += hsy + margin

        rh = self.render_hinge()
        hsx, hsy = size_2d(rh)
        r = r.union(rh.translate((margin, oy, 0)))
        r = r.union(rh.translate((1.5 * hsx + margin, oy + hsy / 2, 0)))
        r = r.union(rh.translate((3 * hsx + margin, oy, 0)))
        r = r.union(rh.translate((4.5 * hsx + margin, oy + hsy / 2, 0)))

        rl = self.render_label()
        rl = rotate_x(rl, 90)
        r = r.union(rl.translate((40, -20, 0.5)))

        self._cq_obj = r
        self._obj_label = "acc"
        return self._cq_obj

    def render_assembly(self):
        """Renders a CadQuery Assembly object representing the entire box with accessories"""
        self.check_dimensions()
        r = self.render()
        a = cq.Assembly(obj=r, name="Gridfinity Rugged Box", color=self.box_color)

        r = self.render_lid()
        r = r.translate((0, 0, self.box_height))
        a.add(r, color=self.lid_color, name="Lid")

        if self.front_handle and self.long_enough_for_handle:
            r = self.render_handle()
            zo = self.right_handle_centre[2] - (GR_HANDLE_SZ - M3_CB_DEPTH)
            r = r.translate((0, -self.box_width / 2 - GR_HANDLE_H / 2, zo))
            a.add(r, color=self.handle_color, name="Handle")

        rf = rotate_x(self.render_latch(), -90)
        idx = 1
        yo = GR_LATCH_H / 2
        zo = self.box_height - GR_RIB_CTR + yo / 2
        for pt in self.front_clasp_centres:
            name = "Latch %d" % (idx)
            pt = (pt[0], pt[1] - yo, zo)
            a.add(rf.translate(pt), color=self.latch_color, name=name)
            idx += 1
        if self.side_clasps:
            rl = rotate_z(rotate_x(self.render_latch(), -90), -90)
            rr = rotate_z(rl, 180)
            for pt in self.side_clasp_centres:
                name = "Latch %d" % (idx)
                y = -yo if pt[0] < 0 else yo
                pt = (pt[0] + y, pt[1], zo)
                if pt[0] < 0:
                    a.add(rl.translate(pt), color=self.latch_color, name=name)
                else:
                    a.add(rr.translate(pt), color=self.latch_color, name=name)
                idx += 1

        for i, section in [(a, b) for a in (0, 1) for b in ("inner", "outer")]:
            r = recentre(self.render_hinge(as_closed=True, section=section), "yz")
            r = rotate_y(r, 90)
            name = "Right " if i else "Left "
            name = name + "Hinge %s" % (section)
            a.add(
                r.translate(self.hinge_centres[i]),
                color=self.hinge_color,
                name=name,
            )

        if self.front_label:
            r = self.render_label()
            a.add(r.translate(self.label_centre), color=self.label_color, name="Label")
        self._obj_label = "assembly"
        self._cq_obj = a
        return self._cq_obj
