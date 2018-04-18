import click
import library.hotspot_wrapper as wrapper


CONTEXT_SETTINGS = dict(help_option_names=[' ', '--help', '-h'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--status", help="Shows Autoconnection Status", is_flag=True, default=None)
@click.option("--on/--off", help="Set Hotspot autoconnection to On/Off", default=None)
def main(status, on):
    """wifi_hotspot_autoconnect helps enable/disable hotspot
    autoconnect feature """
    if status:
        click.echo("Hotspot Auto connection status is: " + str(wrapper.status_hotspot_autoconnect()))
    elif on != None:
        wrapper.set_autoconnect(on)
    else:
        print("No configuration detected. Please use --help for instructions")


if __name__ == '__main__':
    main()
