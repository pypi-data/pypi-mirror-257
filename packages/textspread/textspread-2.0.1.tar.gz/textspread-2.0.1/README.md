# textspread
TextSpread is your go-to buddy for text to spreadsheet conversion. Just throw a bunch of text files at it and it'll spit out a neat spreadsheet for you. You can tell it how many columns you want and even choose the format (xls, xlsx, or ods). And if you've got an existing spreadsheet, you can add to it instead of starting from scratch. It's like a friendly robot that does your data organization for you!

**Powered by: [openpyxl](https://github.com/theorchard/openpyxl)**

## Example
```sh 
[tomri@arch textspread]$ source .venv/bin/activate 
(.venv) [tomri@arch textspread]$ cat test.txt
This is the first question?
option a
option b
option c
option d
a
The answer can be 'a' for now
This is the second question?
option a
option b
option c
option d
b
The answer can be 'b' for now
(.venv) [tomri@arch textspread]$ ./testspread.py test.txt -c 7
(.venv) [tomri@arch textspread]$ 
```
###### output
![example image](example/eg.png) 
