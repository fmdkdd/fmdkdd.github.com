# Solarized style for Pygments based on the Vim version of the 'Solarized'
# theme at http://ethanschoonover.com/solarized and on the Monokai
# Pygments style template.
#
# To export as CSS, put into the 'styles' directory of Pygments, and
# run `pygmentize -S solarized -f html > solarized.css`.

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Text, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal

# Switch BASEX with BASE0X to toggle between light/dark color schemes.
BASE3 = '#002b36'
BASE2 = '#073642'
BASE1 = '#586e75'
BASE0 = '#657b83'
BASE00 = '#839496'
BASE01 = '#93a1a1'
BASE02 = '#eee8d5'
BASE03 = '#fdf6e3'

YELLOW = '#b58900'
ORANGE = '#cb4b16'
RED = '#dc322f'
MAGENTA = '#d33682'
VIOLET = '#6c71c4'
BLUE = '#268bd2'
CYAN = '#2aa198'
# GREEN = '#859900'
GREEN = '#719e07'

class SolarizedStyle(Style):

    background_color = BASE03 # BASE02 for low contrast
    highlight_color = ORANGE

    styles = {
        # No corresponding class for the following:
        Text:                      BASE0, # class:  ''
        Whitespace:                "",        # class: 'w'
        Error:                     RED + " bold", # class: 'err'
        Other:                     "",        # class 'x'

        Comment:                   BASE01 + " italic", # class: 'c'
        Comment.Multiline:         "",        # class: 'cm'
        Comment.Preproc:           "",        # class: 'cp'
        Comment.Single:            "",        # class: 'c1'
        Comment.Special:           RED,        # class: 'cs'

        Keyword:                   BASE0 + " bold", # class: 'k'
        Keyword.Constant:          CYAN + " nobold",        # class: 'kc'
        Keyword.Declaration:       "nobold",        # class: 'kd'
        Keyword.Namespace:         "nobold", # class: 'kn'
        Keyword.Pseudo:            CYAN + " nobold",        # class: 'kp'
        Keyword.Reserved:          "nobold",        # class: 'kr'
        Keyword.Type:              YELLOW + " nobold",        # class: 'kt'

        Operator:                  GREEN, # class: 'o'
        Operator.Word:             "",        # class: 'ow' - like keywords

        Punctuation:               BASE0, # class: 'p'

        Name:                      BASE0, # class: 'n'
        Name.Attribute:            "", # class: 'na' - to be revised
        Name.Builtin:              GREEN,        # class: 'nb'
        Name.Builtin.Pseudo:       "",        # class: 'bp'
        Name.Class:                YELLOW, # class: 'nc' - to be revised
        Name.Constant:             YELLOW, # class: 'no' - to be revised
        Name.Decorator:            "", # class: 'nd' - to be revised
        Name.Entity:               "",        # class: 'ni'
        Name.Exception:            GREEN, # class: 'ne'
        Name.Function:             BLUE, # class: 'nf'
        Name.Property:             "",        # class: 'py'
        Name.Label:                "",        # class: 'nl'
        Name.Namespace:            YELLOW,        # class: 'nn' - to be revised
        Name.Other:                "", # class: 'nx'
        Name.Tag:                  RED, # class: 'nt' - like a keyword
        Name.Variable:             BLUE,        # class: 'nv' - to be revised
        Name.Variable.Class:       BLUE,        # class: 'vc' - to be revised
        Name.Variable.Global:      BLUE,        # class: 'vg' - to be revised
        Name.Variable.Instance:    BLUE,        # class: 'vi' - to be revised

        Number:                    CYAN, # class: 'm'
        Number.Float:              "",        # class: 'mf'
        Number.Hex:                "",        # class: 'mh'
        Number.Integer:            "",        # class: 'mi'
        Number.Integer.Long:       "",        # class: 'il'
        Number.Oct:                "",        # class: 'mo'

        Literal:                   CYAN, # class: 'l'
        Literal.Date:              "", # class: 'ld'

        String:                    CYAN, # class: 's'
        String.Backtick:           "",        # class: 'sb'
        String.Char:               "",        # class: 'sc'
        String.Doc:                "",        # class: 'sd' - like a comment
        String.Double:             "",        # class: 's2'
        String.Escape:             "", # class: 'se'
        String.Heredoc:            "",        # class: 'sh'
        String.Interpol:           "",        # class: 'si'
        String.Other:              "",        # class: 'sx'
        String.Regex:              "",        # class: 'sr'
        String.Single:             "",        # class: 's1'
        String.Symbol:             "",        # class: 'ss'

        Generic:                   BASE0,        # class: 'g'
        Generic.Deleted:           "",        # class: 'gd',
        Generic.Emph:              "italic",  # class: 'ge'
        Generic.Error:             RED + " bold",        # class: 'gr'
        Generic.Heading:           "",        # class: 'gh'
        Generic.Inserted:          "",        # class: 'gi'
        Generic.Output:            "",        # class: 'go'
        Generic.Prompt:            "",        # class: 'gp'
        Generic.Strong:            "bold",    # class: 'gs'
        Generic.Subheading:        "",        # class: 'gu'
        Generic.Traceback:         "",        # class: 'gt'
    }
