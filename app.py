#!/usr/bin/env python3
###############################################################################
# dash-health - app
# **Copyright (C) 2019 tschinz - All Rights Reserved**
###############################################################################

from functions import *
from config import *

###############################################################################
# Setup
#
# Setup local input directories
#input_dir = data_inputDir + os.sep
#createDir(input_dir, verbose)
#data_path = input_dir + data_file

###############################################################################
# Get Data
#
#df = pd.read_csv(data_path)

###############################################################################
# Create initial charts
#
# Sidebar
st.sidebar.title(sidebar_title)
# Page
st.title(page_title)

st.header("Headers")
st.header("Headers")
st.subheader("Subheader")

st.header("Text")
st.subheader("`st.text()`")
st.text("Normal Text")

st.subheader("`st.markdown()`")
st.markdown("Some markdown text with a [link](https://tschinz.github.io/zawiki/) and an image ![asset/streamlit.svg](streamlit.svg)")
st.markdown(r'''
            ---

            # H1
            ## H2
            ### H3
            #### H4
            ##### H5
            ###### H6
            
            Emphasis, aka italics, with *asterisks* or _underscores_.

            Strong emphasis, aka bold, with **asterisks** or __underscores__.

            Combined emphasis with **asterisks and _underscores_**.

            Strikethrough uses two tildes. ~~Scratch this.~~
            
            1. First ordered list item
            2. Another item
              * Unordered sub-list.

           * Unordered list can use asterisks
           - Or minuses
           + Or pluses
            
            [link](https://tschinz.github.io/zawiki/writing/md/md_github.html)
            ![image](asset/streamlit.svg)

            Inline `code` has `back-ticks around` it.

            ```python
            s = "Python syntax highlighting"
            print s
            ```
            
            | Tables        | Are           | Cool  |
            | ------------- |:-------------:| -----:|
            | col 3 is      | right-aligned | $1600 |
            | col 2 is      | centered      |   $12 |
            | zebra stripes | are neat      |    $1 |

            > Blockquotes are very handy in email to emulate reply text.
            > This line is part of the same quote.

            ---

            ''')

st.subheader("`st.latex()`")
st.latex(r'''
         a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
         \sum_{k=0}^{n-1} ar^k =
         a \left(\frac{1-r^{n}}{1-r}\right)
         ''')



st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')

st.markdown("`st.write()` is the magic command supporting many input types")
st.write("[Smileys](https://tschinz.github.io/zawiki/multimedia/pictures/emoji/all.html) ar ealso supported : :see_no_evil: :hear_no_evil: :speak_no_evil:")

st.write("Made with :heart: by ".format(author))
st.write("Made with :heart: by ".format(author))