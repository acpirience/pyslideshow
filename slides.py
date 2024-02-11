import typer
from slideshow.slideshow import Slideshow


def main(
    directory: str = typer.Option(
        "",
        help="Directory where the images are",
    ),
    include_sub_folders: bool = typer.Option(
        True,
        help="traverse sub folders",
    ),
    delay: int = typer.Option(
        0,
        help="Delay in second between images, zéro for keypress between images",
    ),
    rollover: bool = typer.Option(
        True,
        help="Restart at the beginning of the folder when the end is reached",
    ),
) -> None:
    Slideshow(directory, include_sub_folders, delay, rollover).run()


if __name__ == "__main__":
    typer.run(main)
