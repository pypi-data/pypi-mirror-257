# -*- coding: utf-8 -*-
from __future__ import annotations

import weakref
from typing import Any, TypeVar

from guidata.configtools import get_icon
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from plotpy.constants import SHAPE_Z_OFFSET
from plotpy.events import RectangularSelectionHandler, setup_standard_tool_filter
from plotpy.items.shape.rectangle import RectangleShape


class DefaultToolbarID:
    pass


GuiToolT = TypeVar("GuiToolT", bound="GuiTool")


class GuiTool(QC.QObject):
    """Base class for interactive tool applying on a plot"""

    def __init__(self, manager, toolbar_id=DefaultToolbarID):
        """Constructor"""
        super().__init__()
        self.manager = manager
        self.parent_tool = None
        self.plots = set()

        # pylint: disable=assignment-from-none
        self.action = self.create_action(manager)
        self.menu: QW.QMenu | None = self.create_action_menu(manager)

        if self.menu is not None:
            self.action.setMenu(self.menu)
        if toolbar_id is DefaultToolbarID:
            toolbar = manager.get_default_toolbar()
        else:
            toolbar = manager.get_toolbar(toolbar_id)
        if toolbar is not None:
            self.setup_toolbar(toolbar)

    def create_action(self, manager):
        """Create and return tool's action"""
        return None

    def setup_toolbar(self, toolbar):
        """Setup tool's toolbar"""
        toolbar.addAction(self.action)
        if self.menu is not None:
            widget = toolbar.widgetForAction(self.action)
            widget.setPopupMode(QW.QToolButton.InstantPopup)

    def create_action_menu(self, manager):
        """Create and return menu for the tool's action"""
        return None

    def set_parent_tool(self, tool):
        """Used to organize tools automatically in menu items"""
        self.parent_tool = tool

    def register_plot(self, baseplot):
        """Every BasePlot using this tool should call register_plot
        to notify the tool about this widget using it
        """
        self.plots.add(baseplot)

    def get_active_plot(self):
        """

        :return:
        """
        for plot in self.plots:
            canvas = plot.canvas()
            if canvas.hasFocus():
                return plot
        if len(self.plots) == 1:
            return list(self.plots)[0]
        return None

    def update_status(self, plot):
        """called by to allow derived
        classes to update the states of actions based on the currently
        active BasePlot

        can also be called after an action modifying the BasePlot
        (e.g. in order to update action states when an item is deselected)
        """
        pass

    def setup_context_menu(self, menu, plot):
        """If the tool supports it, this method should install an action
        in the context menu"""
        pass


class InteractiveTool(GuiTool):
    """Interactive tool base class"""

    TITLE = None
    ICON = None
    TIP = None
    CURSOR = QC.Qt.CursorShape.CrossCursor
    SWITCH_TO_DEFAULT_TOOL = False  # switch to default tool when finished

    #: Signal emitted by InteractiveTool when validating tool action
    SIG_VALIDATE_TOOL = QC.Signal(object)

    #: Signal emitted by InteractiveTool when tool job is finished
    SIG_TOOL_JOB_FINISHED = QC.Signal()

    def __init__(
        self,
        manager,
        toolbar_id=DefaultToolbarID,
        title=None,
        icon=None,
        tip=None,
        switch_to_default_tool=None,
    ):
        if title is not None:
            self.TITLE = title
        if icon is not None:
            self.ICON = icon
        if tip is not None:
            self.TIP = tip
        super().__init__(manager, toolbar_id)
        # Starting state for every plotwidget we can act upon
        self.start_state = {}

        if switch_to_default_tool is None:
            switch_to_default_tool = self.SWITCH_TO_DEFAULT_TOOL
        if switch_to_default_tool:
            self.SIG_TOOL_JOB_FINISHED.connect(self.manager.activate_default_tool)

    def create_action(self, manager):
        """Create and return tool's action"""
        action = manager.create_action(
            self.TITLE, icon=get_icon(self.ICON), tip=self.TIP, triggered=self.activate
        )
        action.setCheckable(True)
        group = self.manager.get_tool_group("interactive")
        group.addAction(action)
        group.triggered.connect(self.interactive_triggered)
        return action

    def cursor(self):
        """Return tool mouse cursor"""
        return self.CURSOR

    def register_plot(self, baseplot):
        """

        :param baseplot:
        """
        # TODO: With the introduction of PlotManager it should
        # be possible to remove the per tool dictionary start_state
        # since all plots from a manager share the same set of tools
        # the State Machine generated by the calls to tool.setup_filter
        # should be the same for all plots. Thus it should be done only once
        # and not once per plot managed by the plot manager
        super().register_plot(baseplot)
        filter = baseplot.filter
        start_state = self.setup_filter(baseplot)
        self.start_state[baseplot] = start_state
        curs = self.cursor()
        if curs is not None:
            filter.set_cursor(curs, start_state)

    def interactive_triggered(self, action):
        """

        :param action:
        """
        if action is self.action:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        """Activate tool"""
        for baseplot, start_state in list(self.start_state.items()):
            baseplot.filter.set_state(start_state, None)
        self.action.setChecked(True)
        self.manager.set_active_tool(self)

    def deactivate(self):
        """Deactivate tool"""
        self.action.setChecked(False)

    def validate(self, filter, event):
        """

        :param filter:
        :param event:
        """
        self.SIG_VALIDATE_TOOL.emit(filter)
        self.SIG_TOOL_JOB_FINISHED.emit()


class CommandTool(GuiTool):
    """Base class for command tools: action, context menu entry"""

    CHECKABLE = False

    def __init__(
        self,
        manager,
        title,
        icon=None,
        tip=None,
        toolbar_id: Any | type[DefaultToolbarID] | None = DefaultToolbarID,
    ):
        self.title = title
        if icon and isinstance(icon, str):
            self.icon = get_icon(icon)
        else:
            self.icon = icon
        self.tip = tip
        super().__init__(manager, toolbar_id)

    def create_action(self, manager):
        """Create and return tool's action"""
        return manager.create_action(
            self.title,
            icon=self.icon,
            tip=self.tip,
            triggered=self.activate,
            checkable=self.CHECKABLE,
        )

    def setup_context_menu(self, menu, plot):
        """

        :param menu:
        :param plot:
        """
        menu.addAction(self.action)

    def activate(self, checked=True):
        """

        :param checked:
        """
        plot = self.get_active_plot()
        if plot is not None:
            self.activate_command(plot, checked)

    def activate_command(self, plot, checked):
        """Activate tool"""
        pass

    def set_status_active_item(self, plot):
        """

        :param plot:
        """
        item = plot.get_active_item()
        if item:
            self.action.setEnabled(True)
        else:
            self.action.setEnabled(False)


class ActionTool(CommandTool):
    """Tool that simply associate an action to a tool"""

    def __init__(
        self,
        manager,
        action,
        item_types=None,
        toolbar_id=DefaultToolbarID,
    ):
        self.associated_action = action
        self.item_types = item_types
        super().__init__(
            manager,
            action.text(),
            action.icon(),
            action.toolTip(),
            toolbar_id=toolbar_id,
        )

    def update_status(self, plot):
        """Update tool status"""
        if self.item_types is None:
            self.action.setEnabled(True)
        else:
            items = plot.get_selected_items()
            self.action.setEnabled(
                any(isinstance(item, self.item_types) for item in items)
            )

    def create_action(self, manager):
        """Create and return tool's action"""
        return self.associated_action


class ToggleTool(CommandTool):
    """ """

    CHECKABLE = True

    def __init__(self, manager, title, icon=None, tip=None, toolbar_id=None):
        super().__init__(manager, title, icon, tip, toolbar_id)


class PanelTool(ToggleTool):
    """ """

    panel_id = None
    panel_name = None

    def __init__(self, manager):
        super().__init__(manager, self.panel_name)
        manager.get_panel(self.panel_id).SIG_VISIBILITY_CHANGED.connect(
            self.action.setChecked
        )

    def activate_command(self, plot, checked):
        """Activate tool"""
        panel = self.manager.get_panel(self.panel_id)
        panel.setVisible(checked)

    def update_status(self, plot):
        """

        :param plot:
        """
        panel = self.manager.get_panel(self.panel_id)
        self.action.setChecked(panel.isVisible())


class RectangularActionTool(InteractiveTool):
    """ """

    SHAPE_STYLE_SECT = "plot"
    SHAPE_STYLE_KEY = "shape/drag"
    AVOID_NULL_SHAPE = False

    def __init__(
        self,
        manager,
        func,
        shape_style=None,
        toolbar_id=DefaultToolbarID,
        title=None,
        icon=None,
        tip=None,
        fix_orientation=False,
        switch_to_default_tool=None,
    ):
        self.action_func = func
        self.fix_orientation = fix_orientation
        super().__init__(
            manager,
            toolbar_id,
            title=title,
            icon=icon,
            tip=tip,
            switch_to_default_tool=switch_to_default_tool,
        )
        if shape_style is not None:
            self.shape_style_sect = shape_style[0]
            self.shape_style_key = shape_style[1]
        else:
            self.shape_style_sect = self.SHAPE_STYLE_SECT
            self.shape_style_key = self.SHAPE_STYLE_KEY
        self.last_final_shape = None
        self.switch_to_default_tool = switch_to_default_tool

    def get_last_final_shape(self):
        """

        :return:
        """
        if self.last_final_shape is not None:
            return self.last_final_shape()

    def set_shape_style(self, shape):
        """

        :param shape:
        """
        shape.set_style(self.shape_style_sect, self.shape_style_key)

    def create_shape(self):
        """

        :return:
        """
        shape = RectangleShape(0, 0, 1, 1)
        self.set_shape_style(shape)
        return shape, 0, 2

    def setup_shape(self, shape):
        """

        :param shape:
        """
        pass

    def get_shape(self):
        """Reimplemented RectangularActionTool method"""
        shape, h0, h1 = self.create_shape()
        self.setup_shape(shape)
        return shape, h0, h1

    def get_final_shape(self, plot, p0, p1):
        """

        :param plot:
        :param p0:
        :param p1:
        :return:
        """
        shape, h0, h1 = self.create_shape()
        self.setup_shape(shape)
        plot.add_item_with_z_offset(shape, SHAPE_Z_OFFSET)
        shape.move_local_point_to(h0, p0)
        shape.move_local_point_to(h1, p1)
        self.last_final_shape = weakref.ref(shape)
        return shape

    def get_selection_handler(self, filter, start_state):
        return RectangularSelectionHandler(
            filter, QC.Qt.LeftButton, start_state=start_state
        )

    def setup_filter(self, baseplot):
        filter = baseplot.filter
        start_state = filter.new_state()
        handler = self.get_selection_handler(filter, start_state)
        shape, h0, h1 = self.get_shape()
        handler.set_shape(
            shape, h0, h1, self.setup_shape, avoid_null_shape=self.AVOID_NULL_SHAPE
        )
        handler.SIG_END_RECT.connect(self.end_rect)
        return setup_standard_tool_filter(filter, start_state)

    def end_rect(self, filter, p0, p1):
        """

        :param filter:
        :param p0:
        :param p1:
        """
        plot = filter.plot
        if self.fix_orientation:
            left, right = min(p0.x(), p1.x()), max(p0.x(), p1.x())
            top, bottom = min(p0.y(), p1.y()), max(p0.y(), p1.y())
            self.action_func(plot, QC.QPointF(left, top), QC.QPointF(right, bottom))
        else:
            self.action_func(plot, p0, p1)
        self.SIG_TOOL_JOB_FINISHED.emit()
        if self.switch_to_default_tool:
            shape = self.get_last_final_shape()
            plot.set_active_item(shape)
