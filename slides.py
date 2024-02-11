import typer


def main(
    directory: str = typer.Option(
        "",
        help="Directory where the images are",
    ),
    delay: int = typer.Option(
        "",
        help="Delay in second between images, zéro for keypress between images",
    ),
) -> None:
    print(f"Hello {directory}, {delay}")


if __name__ == "__main__":
    typer.run(main)
