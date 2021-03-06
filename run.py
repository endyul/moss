from app import app
from app.tasks import Temperature
from app.models import Settings

def load_settings():
    settings = {}

    fire_value = None
    try:
        fire_value = Settings.get_fire_value()
    except:
        pass
    settings['fire_value'] = fire_value

    should_alarm = False
    try:
        should_alarm = Settings.get_alert_switch_value()
    except:
        pass
    settings['should_alarm'] = should_alarm

    dev_port = app.config.get('DEV_PORT')
    if dev_port:
        settings['dev_port'] = dev_port

    app.logger.info(settings)
    return settings

if __name__ == '__main__':
    settings = load_settings()
    moss = Temperature(**settings)
    Settings.on_change(lambda: moss.set_settings(**load_settings()))
    moss.setDaemon(True)
    moss.start()
    app.run(host='0.0.0.0', port=9527, use_reloader=False)
