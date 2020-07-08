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

###############################################################################
# Get Data
#
df_orig = getData(data_dir, csv_file)

###############################################################################
# Create initial charts
#

###############################################################################
# Sidebar
#
st.sidebar.title(sidebar_title)
st.sidebar.subheader("Checkbox")

show_control_code = st.sidebar.checkbox("Show Control Code", True)
st.subheader("Selection")

st.sidebar.subheader("Button")

if st.sidebar.button('Click Me'):
  progress = 100
else:
  progress = 50

st.sidebar.subheader("Radiobutton")
radio_selection = st.sidebar.radio(
  "What data do you want to see?",
  ('All', 'Human Readable'))
if radio_selection == 'All':
  df = df_orig
elif radio_selection == 'Human Readable':
  df = df_orig[['tunnelname', 'tunnelsystem', 'inbetrieb_nahmejahr', 'kanton']]

st.sidebar.subheader("Select")
options = []
options.append('All')
for kanton in list(df.kanton.unique()):
  options.append(kanton)
option = st.sidebar.selectbox(
  'What region do you want',
  options)
if not option == 'All':
  df = df.loc[df['kanton'] == option]

st.sidebar.subheader("Multiselect")
options = st.sidebar.multiselect(
  'What columns you want?',
  list(df.columns.values),
  list(df.columns.values))

st.sidebar.subheader("Slider")
min_value = int(df['inbetrieb_nahmejahr'].min())
max_value = int(df['inbetrieb_nahmejahr'].max())
slider_values = st.sidebar.slider(
  'Select year range',
  min_value,
  max_value,
  (min_value, max_value))
df = df.loc[(df['inbetrieb_nahmejahr'] >= slider_values[0]) & (df['inbetrieb_nahmejahr'] <= slider_values[1])]

st.sidebar.subheader("Inputs")
title = st.sidebar.text_input('Text input', 'Life of Brian')

number = st.sidebar.number_input('Number input')

txt = st.sidebar.text_area('Text area input', '''It was the best of times, it was the worst of times, it was
the age of wisdom, it was the age of foolishness, it was
the epoch of belief, it was the epoch of incredulity, it
was the season of Light, it was the season of Darkness, it
was the spring of hope, it was the winter of despair, (...)''')

d = st.sidebar.date_input("When's your birthday", datetime.date(2019, 7, 6))

t = st.sidebar.time_input('Set an alarm for', datetime.time(8, 45))

st.sidebar.subheader("File Uploader")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
  data = pd.read_csv(uploaded_file)

st.sidebar.subheader("Color Picker")
color = st.sidebar.beta_color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)

###############################################################################
# Filter Data
#


###############################################################################
# Page
#
st.title(page_title)
st.markdown("[Streamlit Docs](https://docs.streamlit.io/en/stable/)")

st.subheader("Progress Bar")
with st.echo("below"):
  progressbar = st.progress(progress)

st.subheader("Spinner")
with st.echo("below"):
  with st.spinner('Wait for it...'):
    time.sleep(1)
  st.success('Done!')

st.header("Data")
st.subheader("Dataframe")
with st.echo("below"):
  st.dataframe(df)
  st.dataframe(df.style.highlight_max(axis=0))

st.subheader("Table")
with st.echo("below"):
  st.table(df[['tunnelname', 'tunnelsystem', 'inbetrieb_nahmejahr']].tail(3))

st.subheader("JSON")
with st.echo("below"):
  st.json(open(data_dir + os.sep + json_file, 'r').read())

st.header("Graphs")
st.subheader("Native Charts")
st.markdown(r'''
* Linexyfvydvydfg Chart
* Area Chart
* Bar Chart
''')
with st.echo('below'):
  chart_data = df[['inbetrieb_nahmejahr', 'linie', 'km_go']]
  chart_data.set_index('inbetrieb_nahmejahr', inplace=True)
  st.line_chart(chart_data)
  st.area_chart(chart_data)
  st.bar_chart(chart_data)

st.header("Media")
st.subheader("Images")
with st.echo("below"):
  st.image(Image.open(asset_dir + os.sep + 'automation.png'), caption='Image column width', use_column_width=True)
  st.image(Image.open(asset_dir + os.sep + 'automation.png'), caption='Image width 250px', width=250)

st.subheader("Graphviz")
with st.echo("below"):
  st.graphviz_chart('''
      digraph {
          run -> intr
          intr -> runbl
          runbl -> run
          run -> kernel
          kernel -> zombie
          kernel -> sleep
          kernel -> runmem
      }
  ''')

st.subheader("Audio")
with st.echo("below"):
  st.audio(open(asset_dir + os.sep + "the_monkeys_are_listening.mp3", 'rb').read())

st.subheader("Video")
with st.echo("below"):
  st.video(open(asset_dir + os.sep + "timelapse.mp4", 'rb').read())

st.header("Text")

with st.echo("below"):
  st.header("Header")
  st.subheader("Subheader")

st.subheader("`st.text()`")

with st.echo("below"):
  st.text("Normal Text")

st.subheader("`st.latex()`")

with st.echo("below"):
  st.latex("x^n + y^n = z^n")

st.subheader("`st.markdown()`")

st.markdown(r'''
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

st.markdown(r'''
  ```markdown
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
  
  Inline `code` has `back-ticks around` it.
  
   ```python
   s = "Python syntax highlighting"
   print s
   \```
   
  | Tables        | Are           | Cool  |
  | ------------- |:-------------:| -----:|
  | col 3 is      | right-aligned | $1600 |
  | col 2 is      | centered      |   $12 |
  | zebra stripes | are neat      |    $1 |
  
  > Blockquotes are very handy in email to emulate reply text.
  > This line is part of the same quote.
  
  ---
  ```
''')

with st.echo("below"):
  st.markdown(
    "[Emoij's](https://tschinz.github.io/zawiki/multimedia/pictures/emoji/all.html) are also supported :see_no_evil: :hear_no_evil: :speak_no_evil:")

st.subheader("`st.write()`")
st.markdown("`st.write()` is the magic command supporting many input types")

st.subheader("Feedback")
with st.echo("below"):
  st.success("Success of some sorts")
  st.info("Info of some sorts")
  st.warning("Warning of some sorts")
  st.error("Error of some sorts")
  st.exception("Exception of some sorts")

###############################################################################
# Footer
#
st.markdown("---")
st.markdown("Made with :heart: by [{}]({})".format(author, author_url))
st.markdown("Source on [{}]({}) deployed at [{}]({})".format(repo, repo_url, deploy, deploy_url))
st.markdown("Datasource from [{}]({})".format(data, data_url))
