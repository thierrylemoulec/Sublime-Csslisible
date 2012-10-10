# Sublime CssLisible

A plugin for [Sublime Text 2](http://sublimetext.com/2), that runs your ugly CSS through the [http://csslisible.com/](http://csslisible.com/) API.

## Installation

* Recommended - Using Sublime Package Control  
  * `ctrl+shft+p` or `super+shift+p` on osx then select `Package Control: Install Package`
  * `install Csslisible`

*Using Package Control ensures Sublime Csslisible will stay up to date automatically.*

* Alternatively, download the package from GitHub into your Packages folder (on OSX):

        cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
        git clone git@github.com:thierrylemoulec/Sublime-Csslisible.git

## Usage

* Open a CSS file
* Select one or multiple block. 
* If no selection is made the plugin will run on the whole file.
* Press `ctrl+alt+l` on Windows, Linux and OS X to run Csslisible or use the command palette.


## CssLisible simplified API

'idparam' : (value,/default value/) : Explanation

### Required parameters
'api' : (1)  
'clean_css' : (css to clean) : CSS to clean

### Optional parameters

'distance_selecteurs' : (0,/1/,2) : Number of lines separating multiple selectors.  
'type_indentation' : (0,1,2,/3/,4,5,6) : Chosen type of indentation.  
'type_separateur' : (0,1,/2/,3) : Type of separator between properties and value.  
'selecteurs_multiples_separes' : (0,/1/) : Adding a carriage return after each part of a multiple selector. (Boolean)
'valeurs_multiples_separees' : (0,/1/) : Adding a carriage return after each comma in a multiple value. (Boolean)
'hex_colors_format' : (/0/,1,2) : Formatting colors (# fff to # FFF, and vice versa).  
'colors_format' : (/0/,1,2,3) : Advanced formatting of colors.
'raccourcir_valeurs' : (/0/,1) : Using CSS shortcuts on values with 4 numericals parameters. (Boolean)

### Parameters values

#### type_indentation
0 : 1 space  
1 : 2 spaces  
2 : 3 spaces  
3 : 4 spaces ( default )  
4 : 1 tab  
5 : 2 tabs  
6 : no indent.


#### type_separateur
0 : ':'  
1 : ' :'  
2 : ': '  
3 : ' : '


#### hex_colors_format

0 : 'Unchanged'  
1 : 'lower' ( #FFF -> #fff )  
2 : 'upper' ( #fff -> #FFF )


#### colors_format

0 : 'Unchanged'  
1 : 'Name' ( #000 / rgb(0,0,0) -> white [if possible])  
2 : 'Hex' : ( rgb(0,0,0) / black -> #000 )  
3 : 'RGB' : ( #000 / black -> rgb(0,0,0) )


## License
MIT