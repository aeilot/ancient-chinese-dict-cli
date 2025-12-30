import json
import os
from typing_extensions import Annotated
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box

# Initialize Rich Console
console = Console()

# Preload
# Ancient Chinese Credit: GitHub lwl5219/ancient_chinese
with open('ancient_chinese.json','r',encoding='utf-8') as file:
    data = json.load(file)

# Read Item
def item_read(item):
    # Create a title panel for the word
    title = Text(item['word'], style="bold magenta", justify="center")
    
    console.print()
    console.print(Panel(title, title="[bold yellow]汉字 / Character[/bold yellow]", 
                       border_style="cyan", box=box.DOUBLE))
    
    # Create a table for pronunciations and definitions
    listOfExplain = item['explain']
    
    for pronun in listOfExplain:
        # Create a table for each pronunciation
        table = Table(show_header=True, header_style="bold magenta", 
                     border_style="blue", box=box.ROUNDED, 
                     title=f"[bold green]读音 / Pronunciation: {pronun}[/bold green]",
                     title_style="bold green")
        table.add_column("序号 / No.", style="cyan", width=8, justify="center")
        table.add_column("释义 / Definition", style="white")
        
        exp_list = listOfExplain[pronun]
        for idx, definition in enumerate(exp_list, 1):
            if definition.strip():  # Only add non-empty definitions
                # Add some styling to the definition
                table.add_row(str(idx), definition)
        
        console.print()
        console.print(table)
    
    # Add URL info panel
    console.print()
    url_text = Text(item['url'], style="blue underline")
    console.print(Panel(url_text, title="[bold yellow]在线词典链接 / Online Dictionary URL[/bold yellow]", 
                       border_style="green", box=box.ROUNDED))
    
    console.print()
    openURL = Confirm.ask("[bold cyan]是否打开在线词典页面？ / Do you want to open the online dictionary page?[/bold cyan]")
    if openURL:
        typer.launch(item['url'])

def item_json(item):
    return json.dumps(item)

def item_open_url(item):
    typer.launch(item['url'])

# Search for entries
def search(word):
    for i in data:
        if i['word'] == word:
            return i
    return None

def main(word: Annotated[str, typer.Option(help="The word you would like to make a query for.")] = '', openUrl: Annotated[bool, typer.Option(help="Directly open the word URL.")] = False, debug: Annotated[bool, typer.Option(help="Whether to print the JSON content.")] = False):
    if word == '':
        console.print("[bold cyan]欢迎使用古汉语词典 / Welcome to Ancient Chinese Dictionary[/bold cyan]")
        word = Prompt.ask("[bold yellow]请输入要查询的字词 / What word do you want to search for?[/bold yellow]")
    
    res_word = search(f"{word}")
    
    if res_word is None:
        console.print(f"[bold red]错误：未找到「{word}」/ Error: Word '{word}' not found[/bold red]")
        return
    
    if debug:
        console.print()
        console.print(Panel.fit(item_json(res_word), title='[bold magenta]Debug JSON[/bold magenta]', 
                               border_style="magenta"))
    
    if openUrl:
        item_open_url(res_word)
    else:
        item_read(res_word)

if __name__ == "__main__":
    typer.run(main)
