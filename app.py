import json
import os
from typing_extensions import Annotated
import rich
import typer
from rich import print
from rich.panel import Panel

# Preload
# Ancient Chinese Credit: GitHub lwl5219/ancient_chinese
with open('ancient_chinese.json','r',encoding='utf-8') as file:
    data = json.load(file)

# Read Item
def item_read(item):
    print(item['word'])
    listOfExplain = item['explain']
    for pronun in listOfExplain:
        print(pronun)
        exp_list = listOfExplain[str(pronun)]
        for i in exp_list:
            print(i)
    openURL = typer.confirm("Do you want to open the online dictionary page directly?")
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
        word = typer.prompt("What the word you want to search for?")
    res_word = search(f"{word}")
    if debug:
        print(Panel.fit(item_json(res_word),title='Debug JSON'))
    if openUrl:
        item_open_url(res_word)
    else:
        item_read(res_word)

if __name__ == "__main__":
    typer.run(main)
