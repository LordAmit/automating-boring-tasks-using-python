import click
import library.hotspot_wrapper as wrapper


def hotspot_exists():
    return wrapper.hotspot_exists()


def autoconnect_status():
    return wrapper.status_hotspot_autoconnect()


def autoconnect_set(value: bool):
    wrapper.set_autoconnect(value)


CONTEXT_SETTINGS = dict(help_option_names=[' ', '--help', '-h'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--status", help="Shows Autoconnection Status", is_flag=True,
              default=None)
@click.option("--set", help="Set Hotspot autoconnection to True/False",
              type=bool)
def main(status, set):
    """wifi_hotspot_autoconnect helps enable/disable hotspot
    autoconnect feature """
    if(status):
        click.echo("Hotspot Auto connection status is: " +
                   str(autoconnect_status()))
        return
    if isinstance(set, bool):
        wrapper.set_autoconnect(set)
    if status is None and set is None:
        print("No configuration detected. Please use --help for instructions")
    # autoconnect_set(set)


if __name__ == '__main__':
    main()
