import datetime
import logging

from nomad.datamodel import EntryArchive

from nomad_camels_plugin.parsers.parser import CamelsParser


def test_parse_CAMELS_file_exact_values():
    parser = CamelsParser()
    archive = EntryArchive()
    data = parser.parse(
        'tests/data/raw/test_CAMELS_file.nxs',
        archive,
        logging.getLogger(),
        testing=True,
    )

    # Assert basic attributes
    assert data.name == 'test_CAMELS_file'
    assert data.datetime.isoformat() == '2025-03-04T17:14:44.175182+00:00'
    assert (
        data.measurement_description
        == 'Measurement&nbsp;Description&nbsp;Test&nbsp;Entry<br>New&nbsp;Line'
    )
    assert (
        data.protocol_description
        == 'This&nbsp;is&nbsp;the&nbsp;protocol&nbsp;description.<br>New&nbsp;Line.'
    )
    assert data.protocol_overview == (
        "Sweep&nbsp;'Simple_Sweep'&nbsp;demo_motorX:<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Read:&nbsp;['demo_detectorX',&nbsp;'demo_motorX']<br>"
        '&nbsp;&nbsp;&nbsp;&nbsp;Values:&nbsp;(start:&nbsp;-1,&nbsp;stop:&nbsp;1,&nbsp;points:&nbsp;11):'
    )
    assert isinstance(data.protocol_json, dict)
    assert data.protocol_json == {
        'description': 'This is the protocol description.\nNew Line.',
        'export_csv': False,
        'export_json': False,
        'session_name': 'Session Name',
        'skip_config': False,
        'h5_during_run': True,
        'use_end_protocol': False,
        'end_protocol': '',
        'live_variable_update': False,
        'allow_live_comments': True,
        'loop_steps': [
            {
                'step_type': 'Simple Sweep',
                'has_children': False,
                'children': [],
                'name': 'Simple_Sweep',
                'full_name': 'Simple Sweep (Simple_Sweep)',
                'parent_step': 'None',
                'time_weight': 1,
                'used_devices': ['demo'],
                'description': 'This is the Simple Sweep Step description.\nNew Line',
                'is_active': True,
                'loop_type': 'start - stop',
                'start_val': '-1',
                'stop_val': '1',
                'min_val': '',
                'max_val': '',
                'n_points': '11',
                'sweep_mode': 'linear',
                'n_iterations': 11,
                'val_list': [],
                'file_path': '',
                'include_end_points': True,
                'use_distance': False,
                'point_distance': 'nan',
                'sweep_channel': 'demo_motorX',
                'data_output': 'sub-stream',
                'plots': [
                    {
                        'plt_type': 'X-Y plot',
                        'x_axis': 'demo_motorX',
                        'y_axes': {'formula': ['demo_detectorX'], 'axis': ['left']},
                        'z_axis': '',
                        'title': '',
                        'xlabel': '',
                        'ylabel': '',
                        'ylabel2': '',
                        'logX': False,
                        'logY': False,
                        'logY2': False,
                        'zlabel': '',
                        'do_plot': True,
                        'same_fit': False,
                        'fits': [
                            {
                                'do_fit': False,
                                'predef_func': '',
                                'custom_func': '',
                                'use_custom_func': False,
                                'guess_params': True,
                                'name': '',
                                'display_values': False,
                                'initial_params': {
                                    'name': [],
                                    'initial value': [],
                                    'lower bound': [],
                                    'upper bound': [],
                                },
                                'additional_data': [],
                                'y': 'demo_detectorX',
                                'x': 'demo_motorX',
                            }
                        ],
                        'plot_all_available': True,
                        'all_fit': {
                            'do_fit': False,
                            'predef_func': '',
                            'custom_func': '',
                            'use_custom_func': False,
                            'guess_params': True,
                            'name': '',
                            'display_values': False,
                            'initial_params': {
                                'name': [],
                                'initial value': [],
                                'lower bound': [],
                                'upper bound': [],
                            },
                            'additional_data': [],
                            'y': '',
                            'x': 'demo_motorX',
                        },
                        'name': 'demo_detectorX vs. demo_motorX',
                        'maxlen': None,
                        'top_left_x': '',
                        'top_left_y': '',
                        'plot_width': '',
                        'plot_height': '',
                        'checkbox_manual_plot_position': False,
                        'checkbox_show_in_browser': False,
                        'browser_port': 8050,
                    }
                ],
                'read_channels': ['demo_detectorX', 'demo_motorX'],
                'skip_failed': [False, False],
            }
        ],
        'loop_step_dict': {
            'Simple Sweep (Simple_Sweep)': {
                'step_type': 'Simple Sweep',
                'has_children': False,
                'children': [],
                'name': 'Simple_Sweep',
                'full_name': 'Simple Sweep (Simple_Sweep)',
                'parent_step': 'None',
                'time_weight': 1,
                'used_devices': ['demo'],
                'description': 'This is the Simple Sweep Step description.\nNew Line',
                'is_active': True,
                'loop_type': 'start - stop',
                'start_val': '-1',
                'stop_val': '1',
                'min_val': '',
                'max_val': '',
                'n_points': '11',
                'sweep_mode': 'linear',
                'n_iterations': 11,
                'val_list': [],
                'file_path': '',
                'include_end_points': True,
                'use_distance': False,
                'point_distance': 'nan',
                'sweep_channel': 'demo_motorX',
                'data_output': 'sub-stream',
                'plots': [
                    {
                        'plt_type': 'X-Y plot',
                        'x_axis': 'demo_motorX',
                        'y_axes': {'formula': ['demo_detectorX'], 'axis': ['left']},
                        'z_axis': '',
                        'title': '',
                        'xlabel': '',
                        'ylabel': '',
                        'ylabel2': '',
                        'logX': False,
                        'logY': False,
                        'logY2': False,
                        'zlabel': '',
                        'do_plot': True,
                        'same_fit': False,
                        'fits': [
                            {
                                'do_fit': False,
                                'predef_func': '',
                                'custom_func': '',
                                'use_custom_func': False,
                                'guess_params': True,
                                'name': '',
                                'display_values': False,
                                'initial_params': {
                                    'name': [],
                                    'initial value': [],
                                    'lower bound': [],
                                    'upper bound': [],
                                },
                                'additional_data': [],
                                'y': 'demo_detectorX',
                                'x': 'demo_motorX',
                            }
                        ],
                        'plot_all_available': True,
                        'all_fit': {
                            'do_fit': False,
                            'predef_func': '',
                            'custom_func': '',
                            'use_custom_func': False,
                            'guess_params': True,
                            'name': '',
                            'display_values': False,
                            'initial_params': {
                                'name': [],
                                'initial value': [],
                                'lower bound': [],
                                'upper bound': [],
                            },
                            'additional_data': [],
                            'y': '',
                            'x': 'demo_motorX',
                        },
                        'name': 'demo_detectorX vs. demo_motorX',
                        'maxlen': None,
                        'top_left_x': '',
                        'top_left_y': '',
                        'plot_width': '',
                        'plot_height': '',
                        'checkbox_manual_plot_position': False,
                        'checkbox_show_in_browser': False,
                        'browser_port': 8050,
                    }
                ],
                'read_channels': ['demo_detectorX', 'demo_motorX'],
                'skip_failed': [False, False],
            }
        },
        'plots': [],
        'filename': 'test_CAMELS_file',
        'variables': {},
        'loop_step_variables': {'Simple_Sweep_Count': 0, 'Simple_Sweep_Value': 0},
        'channels': {},
        'name': 'Protocol',
        'use_nexus': True,
        'measurement_description': 'Measurement Description Test Entry\nNew Line',
        'tags': ['Tag 1', 'Tag 2'],
    }

    assert data.measurement_comments == '2025-03-04T18:14:46&nbsp;Live&nbsp;Comment'
    assert data.measurement_tags == ['Tag 1', 'Tag 2']
    assert data.protocol_name == 'Protocol'
    assert data.end_time.isoformat() == '2025-03-04T17:14:55.439912+00:00'
    assert data.session_name == 'Session Name'
    assert data.camels_file == 'test_CAMELS_file.nxs'

    # Assert the exact python script content
    expected_python_script = 'import sys\nsys.path.append(r"/Users/alexfuchs/Documents/.camelsenv/lib/python3.11/site-packages")\nsys.path.append(r"/Users/alexfuchs/Documents/.camelsenv/lib/python3.11/site-packages/nomad_camels")\nsys.path.append(r"/Users/alexfuchs/Documents/devices/devices_drivers")\n\nimport numpy as np\nimport importlib\nimport bluesky\nimport ophyd\nimport requests\nfrom nomad_camels.bluesky_handling.run_engine_overwrite import RunEngineOverwrite\nfrom bluesky.callbacks.best_effort import BestEffortCallback\nimport bluesky.plan_stubs as bps\nimport databroker\nfrom PySide6.QtWidgets import QApplication, QMessageBox\nfrom PySide6.QtCore import QCoreApplication, QThread\nimport datetime\nimport subprocess\nfrom nomad_camels.utility import theme_changing\nfrom nomad_camels.bluesky_handling.evaluation_helper import Evaluator\nfrom nomad_camels.bluesky_handling import helper_functions, variable_reading\nfrom event_model import RunRouter\ndarkmode = False\ntheme = "default"\nprotocol_step_information = {"protocol_step_counter": 0, "total_protocol_steps": 1, "protocol_stepper_signal": None}\n\nnamespace = {}\nall_fits = {}\nplots = []\nplots_plotly = []\nboxes = {}\nlive_windows = []\napp = None\nsave_path = "/Users/alexfuchs/Library/Application Support/nomad_camels_data/default_user/default_sample/Session Name/test_CAMELS_file.nxs"\nsession_name = "Session Name"\nexport_to_csv = False\nexport_to_json = False\nnew_file_each_run = True\ndo_nexus_output = True\nSimple_Sweep_Count = 0\nnamespace["Simple_Sweep_Count"] = Simple_Sweep_Count\nSimple_Sweep_Value = 0\nnamespace["Simple_Sweep_Value"] = Simple_Sweep_Value\n\nProtocol_variable_signal = variable_reading.Variable_Signal(name="Protocol_variable_signal", variables_dict=namespace)\neva = Evaluator(namespace=namespace)\n\n\n\nfrom nomad_camels_driver_demo_instrument.demo_instrument_ophyd import Demo_Device\n\n\ndef create_plots_Simple_Sweep(RE, stream="primary"):\n    global app\n    app = QCoreApplication.instance()\n    if app is None:\n        app = QApplication(sys.argv)\n    from nomad_camels.main_classes import plot_pyqtgraph, list_plot\n    if darkmode:\n        plot_pyqtgraph.activate_dark_mode()\n    plot_evaluator=eva\n    subs = []\n    fits = []\n    plot_info = dict(x_name="demo_motorX", y_names=[\'demo_detectorX\'], ylabel="demo_detectorX", xlabel="demo_motorX", title="", stream_name=stream, evaluator=plot_evaluator, fits=fits, multi_stream=False, y_axes={\'demo_detectorX\': 1}, ylabel2="", logX=False, logY=False, logY2=False, maxlen="inf", manual_plot_position=False, top_left_x="", top_left_y="", plot_width="", plot_height="", show_in_browser="False", web_port=8050)\n    plot_0 = plot_pyqtgraph.PlotWidget(**plot_info)\n    plots.append(plot_0)\n    plot_0.show()\n    subs.append(RE.subscribe(plot_0.livePlot))\n    for fit in plot_0.liveFits:\n        all_fits[fit.name] = fit\n    return plots, subs, app, plots_plotly\n\n\n\n\ndef Protocol_plan_inner(devs, stream_name="primary", runEngine=None):\n    channels = [devs["demo"].detectorX, devs["demo"].motorX]\n    helper_functions.clear_plots(plots, "Simple_Sweep")\n    """This is the Simple Sweep Step description.\n    New Line """\n    protocol_step_information["protocol_stepper_signal"].emit(protocol_step_information["protocol_step_counter"] / protocol_step_information["total_protocol_steps"] * 100)\n    protocol_step_information["protocol_step_counter"] += 1\n    yield from bps.checkpoint()\n    for Simple_Sweep_Count, Simple_Sweep_Value in enumerate(helper_functions.get_range(eva, "-1", "1", "11", "nan", "nan", "start - stop", "linear", "True", "nan", False)):\n        namespace.update({"Simple_Sweep_Count": Simple_Sweep_Count, "Simple_Sweep_Value": Simple_Sweep_Value})\n        yield from bps.abs_set(devs["demo"].motorX, Simple_Sweep_Value, group="A")\n        yield from bps.wait("A")\n        yield from helper_functions.trigger_and_read(channels, name="Simple_Sweep")\n    yield from helper_functions.get_fit_results(all_fits, namespace, True, "Simple_Sweep")\n\n\n\ndef Protocol_plan(devs, md=None, runEngine=None, stream_name="primary"):\n    sub_eva = runEngine.subscribe(eva)\n    yield from bps.open_run(md=md)\n    yield from Protocol_plan_inner(devs, stream_name, runEngine)\n    yield from helper_functions.get_fit_results(all_fits, namespace, True)\n    finished = False\n    while not finished:\n        finished = True\n        for window in live_windows:\n            if hasattr(window, \'_is_finished\') and not window._is_finished:\n                finished = False\n    live_metadata = {}\n    for window in live_windows:\n        if hasattr(window, \'get_metadata\'):\n            live_metadata.update(window.get_metadata())\n    live_metadata_signal = variable_reading.Variable_Signal(name=\'live_metadata\', variables_dict=live_metadata)\n    yield from bps.trigger_and_read([live_metadata_signal], name="_live_metadata_reading_")\n    yield from bps.close_run()\n    runEngine.unsubscribe(sub_eva)\n\ndef create_plots(RE, stream="primary"):\n    return [], [], None, None\n\ndef steps_add_main(RE, devs):\n    returner = {}\n    if "subs" not in returner:\n        returner["subs"] = []\n    if "plots" not in returner:\n        returner["plots"] = []\n    plots, subs, _, _ = create_plots_Simple_Sweep(RE, "Simple_Sweep")\n    returner["subs"] += subs\n    returner["plots"] += plots\n    return returner\n\n\ndef create_live_windows():\n    global live_windows\n    commenting_box = helper_functions.Commenting_Box()\n    live_windows.append(commenting_box)\n    return live_windows\n\n\nuids = []\ndef uid_collector(name, doc):\n    uids.append(doc["uid"])\n\n\ndef run_protocol_main(RE, dark=False, used_theme="default", catalog=None, devices=None, md=None):\n    devs = devices or {}\n    md = md or {}\n    global darkmode, theme, protocol_step_information\n    darkmode, theme = dark, used_theme\n    protocol_step_information["total_protocol_steps"] = 1\n    md["user"] = {\'name\': \'default_user\'}\n    md["sample"] = {\'name\': \'default_sample\'}\n    md["session_name"] = session_name\n    md["protocol_overview"] = """Sweep \'Simple_Sweep\' demo_motorX:\\n\\tRead: [\'demo_detectorX\', \'demo_motorX\']\\n\\tValues: (start: -1, stop: 1, points: 11):"""\n    md["description"] = \'This is the protocol description.\\nNew Line.\'\n    md["measurement_tags"] = [\'Tag 1\', \'Tag 2\']\n    md["measurement_description"] = \'Measurement Description Test Entry\\nNew Line\'\n    try:\n        with open("/Users/alexfuchs/Library/Application Support/nomad_camels/python_files/Protocol.cprot", "r", encoding="utf-8") as f:\n            md["protocol_json"] = f.read()\n    except FileNotFoundError:\n        print(\'Could not find protocol configuration file, information will be missing in data.\')\n    with open(__file__, "r", encoding="utf-8") as f:\n        md["python_script"] = f.read()\n    md = helper_functions.get_opyd_and_py_file_contents(Demo_Device, md, \'demo\')\n    md["variables"] = namespace\n    subscription_uid = RE.subscribe(uid_collector, "start")\n    try:\n        RE(Protocol_plan(devs, md=md, runEngine=RE))\n    finally:\n        RE.unsubscribe(subscription_uid)\n        for window in live_windows:\n            window.close()\n\n\ndef ending_steps(runEngine, devs):\n    yield from bps.checkpoint()\n\n\n\ndef main():\n    RE = RunEngineOverwrite()\n    bec = BestEffortCallback()\n    RE.subscribe(bec)\n    try:\n        catalog = databroker.catalog["CAMELS_CATALOG"]\n    except KeyError:\n        import warnings\n        warnings.warn("Could not find databroker catalog, using temporary catalog. If data is not transferred, it might get lost.")\n        catalog = databroker.temp().v2\n    RE.subscribe(catalog.v1.insert)\n\n    from nomad_camels.utility import tqdm_progress_bar\n    tqdm_bar = tqdm_progress_bar.ProgressBar(1)\n\n    protocol_step_information["protocol_stepper_signal"] = tqdm_bar\n    devs = {}\n    device_config = {}\n    try:\n        """demo (Demo_Device):\n        demo instrument description"""\n        settings = {\'mus\': [0.0, 3.0, -4.0], \'amps\': [1.0, 2.0, 27.0], \'sigmas\': [5.0, 7.0, 0.1], \'motor_noises\': [0.0, 0.0, 0.0], \'detector_noises\': [0.0, 0.0, 0.0], \'set_delays\': [0.0, 0.0, 0.0], \'system_delays\': [0.0, 0.0, 0.0]}\n        additional_info = {\'config_channel_metadata\': {}, \'description\': \'demo instrument description\', \'ELN-instrument-id\': \'id_123\', \'ELN-service\': \'\', \'ELN-metadata\': {}, \'device_class_name\': \'Demo_Device\'}\n        demo = Demo_Device("demo:", name="demo", **settings)\n        print("connecting demo")\n        demo.wait_for_connection()\n        config = {}\n        configs = demo.configure(config)[1]\n        device_config["demo"] = {"settings": {}}\n        device_config["demo"]["settings"].update(helper_functions.simplify_configs_dict(configs))\n        device_config["demo"]["settings"].update(settings)\n        device_config["demo"].update(additional_info)\n        devs.update({"demo": demo})\n        print("devices connected")\n        md = {"devices": device_config}\n        rr = RunRouter([lambda x, y: helper_functions.saving_function(x, y, save_path, new_file_each_run, plots, do_nexus_output)])\n        subscription_rr = RE.subscribe(rr)\n        plot_etc = create_plots(RE)\n        additional_step_data = steps_add_main(RE, devs)\n        create_live_windows()\n        run_protocol_main(RE=RE, catalog=catalog, devices=devs, md=md)\n    finally:\n        while RE.state not in ["idle", "panicked"]:\n            import time\n            time.sleep(0.5)\n        for name, device in devs.items():\n            if hasattr(device, "finalize_steps") and callable(device.finalize_steps):\n                device.finalize_steps()\n        if uids:\n            runs = catalog[tuple(uids)]\n            helper_functions.export_function(runs, save_path, False, new_file_each=new_file_each_run, plot_data=plots, do_nexus_output=do_nexus_output)\n        RE.unsubscribe(subscription_rr)\n\n\n\nif __name__ == "__main__":\n    main()\n    print("protocol finished!")\n    if app is not None:\n        sys.exit(app.exec())\n'
    assert data.camels_python_script == expected_python_script

    # Assert instrument settings (load JSON and compare dict)
    expected_settings = {
        'demo': {
            'amps': [1.0, 2.0, 27.0],
            'detector_noises': [0.0, 0.0, 0.0],
            'motor_noises': [0.0, 0.0, 0.0],
            'mus': [0.0, 3.0, -4.0],
            'set_delays': [0.0, 0.0, 0.0],
            'sigmas': [5.0, 7.0, 0.1],
            'system_delays': [0.0, 0.0, 0.0],
        }
    }
    settings = data.camels_instrument_settings
    assert settings == expected_settings

    # Assert instrument list: expect one instrument with name "demo"
    assert isinstance(data.instruments, list)
    assert len(data.instruments) == 1
    instrument = data.instruments[0]
    assert instrument.name == 'demo'

    # Assert that the start time was parsed into a datetime object
    assert isinstance(data.datetime, datetime.datetime)

    # Assert that the protocol description was converted to HTML (replacing newlines and spaces)
    assert '<br>' in data.protocol_description
    assert '&nbsp;' in data.protocol_description

    # Assert that the measurement description was processed similarly
    assert '<br>' in data.measurement_description
    assert '&nbsp;' in data.measurement_description

    # Assert that measurement tags is a non-empty list of strings
    assert isinstance(data.measurement_tags, list)
    assert len(data.measurement_tags) > 0
    for tag in data.measurement_tags:
        assert isinstance(tag, str)

    # Assert that measurement comments is set (even if empty)
    assert data.measurement_comments is not None

    # Assert that the protocol overview is processed with HTML encoding
    assert '<br>' in data.protocol_overview
    assert '&nbsp;' in data.protocol_overview

    # Assert that the plan name is a non-empty string
    assert isinstance(data.protocol_name, str)
    assert data.protocol_name != ''

    # Assert that the end time is parsed into a datetime object
    assert isinstance(data.end_time, datetime.datetime)

    # Assert that the session name is a non-empty string
    assert isinstance(data.session_name, str)
    assert data.session_name != ''

    # Assert that a sample reference exists and has a name attribute
    assert isinstance(data.samples, list)
    assert len(data.samples) > 0
    assert hasattr(data.samples[0], 'name')
    # Optionally, check that the reference URL is correctly formatted if it exists
    if hasattr(data.samples[0], 'reference') and data.samples[0].reference is not None:
        assert '../uploads/' in data.samples[0].reference

    # Assert that instruments list is not empty and that each instrument has a name
    assert isinstance(data.instruments, list)
    for instrument in data.instruments:
        assert hasattr(instrument, 'name')
        # Optionally, verify the reference URL for instruments if available
        if hasattr(instrument, 'reference') and instrument.reference is not None:
            assert '../uploads/' in instrument.reference

    # Assert that the CAMELS instrument settings are valid JSON and convert to a dict
    settings = data.camels_instrument_settings
    assert isinstance(settings, dict)

    # Assert that the CAMELS user is a non-empty string
    assert isinstance(data.camels_user, str)
    assert data.camels_user == 'default_user'
