from pygrabber.dshow_graph import FilterGraph

def get_connected_cameras():
    graph = FilterGraph()
    cameras = []
    devices = graph.get_input_devices()
    for index, device in enumerate(devices):
        cameras.append({
            "deviceId": index,
            "label": device
        })
    return cameras