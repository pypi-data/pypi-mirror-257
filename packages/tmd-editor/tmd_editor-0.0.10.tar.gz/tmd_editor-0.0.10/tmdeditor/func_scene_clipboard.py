# -*- coding: utf-8 -*-
"""
A module containing all code for working with Clipboard
"""
from collections import OrderedDict
from tmdeditor.graphical_edge import DrawGraphicalEdge
from tmdeditor.func_edge import AllEdgeFunctions


DEBUG = False
DEBUG_PASTING = False


class AllSceneClipboardFunctions():
    """
    Class contains all the code for serialization/deserialization from Clipboard
    """
    def __init__(self, scene: 'Scene'):
        """
        :param scene: Reference to the :class:`~tmdeditor.node_scene.Scene`
        :type scene: :class:`~tmdeditor.func_scene.Scene`

        :Instance Attributes:

        - **scene** - reference to the :class:`~tmdeditor.node_scene.Scene`
        """
        self.scene = scene

    def serializeSelected(self, delete: bool=False) -> OrderedDict:
        """
        Serializes selected items in the Scene into ``OrderedDict``

        :param delete: True if you want to delete selected items after serialization. Useful for Cut operation
        :type delete: ``bool``
        :return: Serialized data of current selection in NodeEditor :class:`~tmdeditor.node_scene.Scene`
        """
        if DEBUG: print("-- COPY TO CLIPBOARD ---")

        selected_nodes, selected_edges, selected_sockets = [], [], {}

        # sort edges and nodes
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'):
                selected_nodes.append(item.node.serialize())
                for socket in (item.node.inputs + item.node.outputs):
                    selected_sockets[socket.id] = socket
            elif isinstance(item, DrawGraphicalEdge):
                selected_edges.append(item.edge)


        # debug
        if DEBUG:
            print("  NODES\n      ", selected_nodes)
            print("  EDGES\n      ", selected_edges)
            print("  SOCKETS\n     ", selected_sockets)


        # remove all edges which are not connected to a tmdeditor in our list
        edges_to_remove = []
        for edge in selected_edges:
            if edge.start_socket.id in selected_sockets and edge.end_socket.id in selected_sockets:
                # if DEBUG: print(" edge is ok, connected with both sides")
                pass
            else:
                if DEBUG: print("edge", edge, "is not connected with both sides")
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            selected_edges.remove(edge)

        # make final list of edges
        edges_final = []
        for edge in selected_edges:
            edges_final.append(edge.serialize())

        if DEBUG: print("our final edge list:", edges_final)


        data = OrderedDict([
            ('nodes', selected_nodes),
            ('edges', edges_final),
        ])


        # if CUT (aka delete) remove selected items
        if delete:
            self.scene.getView().deleteSelected()
            # store our history
            self.scene.history.storeHistory("Cut out elements from scene", setModified=True)

        return data

    def deserializeFromClipboard(self, data: dict, *args, **kwargs):
        """
        Deserializes data from Clipboard.

        :param data: ``dict`` data for deserialization to the :class:`tmdeditor.node_scene.Scene`.
        :type data: ``dict``
        """

        hashmap = {}

        # calculate mouse pointer - scene position
        view = self.scene.getView()
        mouse_scene_pos = view.last_scene_mouse_position

        # calculate selected objects bbox and center
        minx, maxx, miny, maxy = 10000000,-10000000, 10000000,-10000000
        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y

        # add width and height of a node
        maxx -= 180
        maxy += 100

        relbboxcenterx = (minx + maxx) / 2 - minx
        relbboxcentery = (miny + maxy) / 2 - miny

        if DEBUG_PASTING:
            print (" *** PASTA:")
            print("Copied boudaries:\n\tX:", minx, maxx, "   Y:", miny, maxy)
            print("\tbbox_center:", relbboxcenterx, relbboxcentery)

        # calculate the offset of the newly creating nodes
        mousex, mousey = mouse_scene_pos.x(), mouse_scene_pos.y()

        # create each node
        created_nodes = []

        self.scene.setSilentSelectionEvents()

        self.scene.doDeselectItems()

        for node_data in data['nodes']:
            new_node = self.scene.getNodeClassFromData(node_data)(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False, *args, **kwargs)
            created_nodes.append(new_node)

            # readjust the new tmdeditor's position

            # new node's current position
            posx, posy = new_node.pos.x(), new_node.pos.y()
            newx, newy = mousex + posx - minx, mousey + posy - miny

            new_node.setPos(newx, newy)

            new_node.doSelect()

            if DEBUG_PASTING:
                print("** PASTA SUM:")
                print("\tMouse pos:", mousex, mousey)
                print("\tnew node pos:", posx, posy)
                print("\tFINAL:", newx, newy)

        # create each edge
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = AllEdgeFunctions(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False, *args, **kwargs)


        self.scene.setSilentSelectionEvents(False)

        # store history
        self.scene.history.storeHistory("Pasted elements in scene", setModified=True)

        return created_nodes