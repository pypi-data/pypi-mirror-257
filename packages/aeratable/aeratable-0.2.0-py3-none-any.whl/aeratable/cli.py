import click
import pyperclip
from tabulate import tabulate

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def parse_data(raw_data: str):
    raw_data = pyperclip.paste()
    raw_data = raw_data.replace("\r", "").split("\n")
    header = raw_data[0].split()
    columns = raw_data[1:]

    n_cols = len(header)
    col_data = []

    for row in chunks(columns, n_cols):
        col_data.append(row)
    return header, col_data

@click.command()
@click.option('-f', '--fmt', default='ascii', help='Output format: ascii or csv. Default is ascii.')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Verbose output.')
@click.option('-i', '--interactive', is_flag=True, default=False, help='Interactive mode. concatenate multiple Interface outputs in one table.')
@click.option('--csv-seperator', default=';', help='seperator to use for CSV output. default is ;')
@click.option('--ascii-style', default='presto', help='Style of the ascii table. Default is presto.')
def main(fmt, verbose, interactive, csv_seperator, ascii_style):
    if interactive:

        existing_header = ""
        existing_col_data = []

        while True:

            answer = click.prompt('Can we take the next interface output from your clipboard? [y/n/f]', type=str)
            if answer.lower() == 'f':
                header = existing_header
                col_data = existing_col_data
                break

            elif answer.lower() == 'y':
                raw_data = pyperclip.paste()
                header, col_data = parse_data(raw_data)
                if existing_header:
                    if existing_header != header:
                        click.echo("Different headers! Please make sure you maintain the same table structure")
                    else:
                        existing_col_data += col_data
                else:
                    existing_header = header
                    existing_col_data = col_data

            elif answer.lower() == 'n':
                click.echo("Please copy your next piece of Interface output to your clipboard")

            else:
                click.echo('Unclear command. Please input f when Finished')

    else:
        raw_data = pyperclip.paste()
        header, col_data = parse_data(raw_data)

    if fmt == "ascii":
        ascii_output = tabulate(col_data, header, tablefmt=ascii_style)
        pyperclip.copy(ascii_output)
        if verbose:
            click.echo(ascii_output)
    elif fmt == "csv":
        csv_output = f"{csv_seperator} ".join(header) + "\n"
        for row in col_data:
            csv_output += f"{csv_seperator} ".join(row)
            csv_output += "\n"
        pyperclip.copy(csv_output)
        if verbose:
            click.echo(csv_output)
    return
 
 