import main
import pytest
type = 'TCS Trust'
path = r'C:\Users\MB2705851\OneDrive - Surbana Jurong Private Limited\Manuals & Guidelines\Traffic\Manual count import templates'
p= main.Count(type,path)
print(len(p.src))