import os
import time
from datetime import datetime

import pytest

from astropy.coordinates import SkyCoord
from astropy import units as u

from qtpy.QtWidgets import QApplication
from qtpy.QtWebEngineWidgets import WEBENGINE

from matplotlib.testing.compare import compare_images

from ..qt_widget import WWTQtWidget

M42 = SkyCoord.from_name('M42')

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

REFERENCE_TIME = datetime(2017, 1, 1, 0, 0, 0, 0)


def wait(seconds):

    app = QApplication.instance()

    time1 = time.time()
    while time.time() - time1 < seconds:
        app.processEvents()


def wait_and_check_output(seconds, capsys):

    # TODO: would be nice to find a way to do this that doesn't
    # rely on waiting a fixed number of seconds

    wait(seconds)

    out, err = capsys.readouterr()
    assert out.strip() == ""
    assert err.strip() == ""


def test_init(capsys):
    WWTQtWidget(block_until_ready=True)
    wait_and_check_output(1, capsys)


class TestWWTWidget:

    def setup_class(self):
        self.widget = WWTQtWidget(block_until_ready=True)

    def test_settings(self, capsys):
        self.widget.constellation_figures = True
        self.widget.constellation_figures = False
        wait_and_check_output(1, capsys)

    def test_methods(self, capsys):
        self.widget.center_on_coordinates(M42, fov=10 * u.deg)
        wait_and_check_output(1, capsys)

    def test_coordinates(self, capsys):
        self.widget.center_on_coordinates(M42, fov=10 * u.deg)
        assert M42.separation(self.widget.get_center()).arcsec < 1.e-6
        wait_and_check_output(1, capsys)

    def test_annotations(self, capsys):
        circle = self.widget.add_circle()
        circle.opacity = 0.8
        circle.set_center(M42)
        wait_and_check_output(1, capsys)


def assert_widget_image(tmpdir, widget, filename):
    tmp_image = tmpdir.join(filename).strpath
    widget.render(tmp_image)
    framework = 'webengine' if WEBENGINE else 'webkit'
    msg = compare_images(os.path.join(DATA, framework, filename), tmp_image, tol=1.5)
    if msg is not None:
        pytest.fail(msg, pytrace=False)


def test_full(tmpdir, capsys):

    # Test a whole session, with image comparison along the way.

    wwt = WWTQtWidget(block_until_ready=True, size=(400, 400))
    wwt.set_current_time(REFERENCE_TIME)
    wwt.foreground_opacity = 1.

    wait(4)

    assert_widget_image(tmpdir, wwt, 'test_full_step0.png')

    gc = SkyCoord(0, 0, unit=('deg', 'deg'), frame='galactic')
    wwt.center_on_coordinates(gc, 60 * u.deg)

    wait(4)

    assert_widget_image(tmpdir, wwt, 'test_full_step1.png')

    wwt.constellation_boundary_color = 'red'
    wwt.constellation_figure_color = 'green'
    wwt.constellation_selection_color = 'blue'

    wwt.constellation_boundaries = True
    wwt.constellation_figures = True

    wait(4)

    assert_widget_image(tmpdir, wwt, 'test_full_step2.png')

    wwt.constellation_selection = True

    wwt.crosshairs = False
    wwt.ecliptic = True
    wwt.grid = True

    wait(4)

    assert_widget_image(tmpdir, wwt, 'test_full_step3.png')

    wwt.foreground = 'SFD Dust Map (Infrared)'

    wait(4)

    assert_widget_image(tmpdir, wwt, 'test_full_step4.png')

    wwt.foreground = "Black Sky Background"
    wwt.background = "Black Sky Background"
    wwt.foreground_opacity = 0

    wwt.center_on_coordinates(gc, 30 * u.deg)

    coord = SkyCoord(5, 0.5, unit=('deg', 'deg'), frame='galactic')

    circle1 = wwt.add_circle()
    circle1.set_center(coord)
    circle1.radius = 10 * u.deg
    circle1.line_width = 5 * u.pixel
    circle1.line_color = 'green'
    circle1.fill = False
    circle1.opacity = 0.5

    coord = SkyCoord(-5, -0.5, unit=('deg', 'deg'), frame='galactic')

    circle2 = wwt.add_circle()
    circle2.set_center(coord)
    circle2.radius = 2 * u.pixel
    circle2.line_width = 5 * u.pixel
    circle2.line_color = 'green'
    circle2.fill = True
    circle2.fill_color = 'orange'
    circle2.opacity = 1

    coord = SkyCoord([0, 4, 1], [-5, 0, 0], unit=('deg', 'deg'), frame='galactic')

    poly = wwt.add_polygon()
    poly.add_point(coord[0])
    poly.add_point(coord[1])
    poly.add_point(coord[2])
    poly.fill = True
    poly.line_color = 'red'
    poly.fill_color = 'yellow'
    poly.line_width = 2 * u.pixel

    coord = SkyCoord([10, 5, 2], [5, 2, 2], unit=('deg', 'deg'), frame='galactic')

    polyline = wwt.add_line()
    polyline.add_point(coord[0])
    polyline.add_point(coord[1])
    polyline.add_point(coord[2])
    polyline.color = 'green'
    polyline.width = 3 * u.pixel

    wait(4)

    assert_widget_image(tmpdir, wwt, 'test_full_step5.png')
