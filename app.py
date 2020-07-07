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
inputDir = data_inputDir + os.sep
createDir(inputDir, verbose)
project_list_file = inputDir + projectListFile

###############################################################################
# Get Data
#
# read project list
(projectDf, projectCol) = getProjectList(project_list_file, projectCol)

# read project entries
sageXDfs, projectConfs = getProjectEntries(inputDir)
# Calc additional stuff
sageXDfs, ashCols = calcAdditionalData(projectDf, sageXDfs, projectConfs, ashCols, projectCol, activityDf, activityCol)
aggregated1Dfs, aggregated2Dfs, aggregated3Dfs = aggregateTime(sageXDfs, projectConfs, ashCols)

# Default Dropdown Selector
selector_time_frame = 'A'
for index, row in projectDf.iterrows():
  for projectConf in projectConfs:
    if projectConf[0] == int(row[projectCol["project_number"]]):
      project_dropdown[row[projectCol["project_number"]]] = row[projectCol["title_humanreadable"]]

###############################################################################
# Select and filter data
#
selector_project, projectConf, selectedDf, aggregated1Df, aggregated2Df, aggregated3Df, ashCol = selectAnyDf(
  projectConfs, sageXDfs, aggregated1Dfs, aggregated2Dfs, aggregated3Dfs, ashCols, project_dropdown)
time_entries, start_date, end_date = filterData(selectedDf, duration_dropdown[selector_time_frame], ashCol["date"])

###############################################################################
# Create initial charts
#
# Basic stats
date_exported = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["updated"]].iloc[0]
project_begin = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["date_begin"]].iloc[
  0].strftime('%d.%m.%Y')
project_end = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["date_end"]].iloc[
  0].strftime('%d.%m.%Y')
project_budget = int(aggregated3Df[ashCol['total_budget']].iloc[0])
project_monthly_budget = int(aggregated3Df[ashCol['monthly_budget']].iloc[0])
project_budget_remaining = int(aggregated3Df[ashCol['remaining_budget']].iloc[-1])
remaining_time = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["date_end"]].iloc[
                   0] - getTodayDate()
project_monthly_budget_remaining = int(aggregated3Df[ashCol['remaining_budget']].iloc[-1]) / (
    remaining_time.total_seconds() * second2month)

# Figures
fig_1_1 = projectPieBudgetActivity(aggregated1Df, aggregated3Df, ashCol, projectDf, projectCol, projectConf)
fig_1_2 = projectPieCollaborators(aggregated2Df, ashCol, projectDf, projectCol, projectConf)
fig_2_1 = projectPlotCombined(aggregated3Df, ashCol, projectDf, projectCol, projectConf)
# fig_3_1 = projectBarBudget(aggregated3Df, ashCol, projectDf, projectCol, projectConf)
# fig_3_2 = projectLinesHours(aggregated3Df, ashCol, projectDf, projectCol, projectConf)

###############################################################################
# Initiate the App
#
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
  app,
  login_credentials
)
server = app.server
app.title = tab_title
###############################################################################
# Create Controls
#
duration_selector_options = [{'label': str(duration_dropdown[duration_selector]),
                              'value': str(duration_selector)}
                             for duration_selector in duration_dropdown]
project_selector_options = [{'label': str(project_dropdown[project_selector]),
                             'value': str(project_selector)}
                            for project_selector in project_dropdown]

###############################################################################
# App Layout
#
app.layout = html.Div([
  ###############################################################################
  # Header
  dcc.Store(id='aggregate_data'),

  html.Div([
    html.Img(
      src="assets/logo.svg",
      className='two columns',
      height="100px",
    ),
    html.Div([
      html.H2(page_title),
      html.H4(page_subtitle),
    ],
      className='eight columns'
    ),
    html.A(
      html.Button(
        "Github Repo",
        id="githubrepo"
      ),
      href=github_url,
      className="two columns"
    ),
    html.A(
      html.Button(
        "Data Source",
        id="datasource"
      ),
      href=data_url,
      className="two columns"
    )],
    id="header",
    className='row',
  ),
  ###############################################################################
  # First Row with controls
  html.Div([
    # Controls
    html.Div([
      html.P('Controls', className="control_label"),
      html.Button('Refresh Data', id='btn-refresh-data', n_clicks=0),
      html.Div(id='container-button-output'),
      dcc.Upload(
        id='upload-data',
        children=html.Div([
          'Drag and Drop or ',
          html.A('Select Files')
        ]),
        style={
          'width': '95%',
          'height': '60px',
          'lineHeight': '60px',
          'borderWidth': '1px',
          'borderStyle': 'dashed',
          'borderRadius': '5px',
          'textAlign': 'center',
          'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
      ),
      html.Div(id='output-data-upload'),
      html.P('Project Selector', className="control_label"),
      dcc.Dropdown(
        id='project_selector',
        options=project_selector_options,
        multi=False,
        value=selector_project,
        clearable=False,
        className="dcc_control"
      ),
      html.P('Duration Selector', className="control_label"),
      dcc.Dropdown(
        id='duration_selector',
        options=duration_selector_options,
        multi=False,
        value=selector_time_frame,
        clearable=False,
        className="dcc_control"
      ),
      html.P('Date Range', className="control_label"),
      dcc.DatePickerRange(
        id='date-picker-range',
        start_date=getMonth(-1)[0],
        end_date=getMonth(-1)[1],
        display_format='DD MMM YYYY'
      ),
      html.Div(id='output-container-control')
    ],
      className="pretty_container four columns"
    ),
    # KPI Row
    html.Div([
      html.Div([
        html.Div([
          html.P(
            id="kpi_title_0"
          ),
          html.H6(
            id="kpi_text_0",
            className="info_text"
          ),
        ],
          id="kpi_0",
          className="pretty_container"
        ),
        html.Div([
          html.P(
            id="kpi_title_1"
          ),
          html.H6(
            id="kpi_text_1",
            className="info_text"
          ),
          html.H6(
            id="kpi_text_1_1",
            className="info_text"
          )
        ],
          id="kpi_1",
          className="pretty_container"
        ),
        html.Div([
          html.Div([
            html.P(
              id="kpi_title_2"
            ),
            html.H6(
              id="kpi_text_2",
              className="info_text"
            ),
            html.H6(
              id="kpi_text_2_2",
              className="info_text"
            )
          ],
            id="kpi_2",
            className="pretty_container"
          ),
          html.Div([
            html.P(
              id="kpi_title_3"
            ),
            html.H6(
              id="kpi_text_3",
              className="info_text"
            ),
            html.H6(
              id="kpi_text_3_3",
              className="info_text"
            )
          ],
            id="kpi_3",
            className="pretty_container"
          ),
          html.Div([
            html.P(
              id="kpi_title_4"
            ),
            html.H6(
              id="kpi_text_4",
              className="info_text"
            ),
            html.H6(
              id="kpi_text_4_4",
              className="info_text"
            )
          ],
            id="kpi_4",
            className="pretty_container"
          ),
        ],
          id="tripleContainer",
        )
      ],
        id="infoContainer",
        className="row"
      ),
      # Table
      html.P('Projet Summary - Collaborator'),
      dash_table.DataTable(
        id='table-data',
        data=aggregated2Df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in aggregated2Df.columns],
      ),
    ],
      className="pretty_container eight columns"
    ),
  ],
    className="row"
  ),

  ###############################################################################
  # Second Row
  html.Div([
    html.Div([
      dcc.Graph(
        id='fig_1_1',
        figure=fig_1_1
      ),
    ],
      className="pretty_container six columns"
    ),
    html.Div([
      dcc.Graph(
        id='fig_1_2',
        figure=fig_1_2
      ),
    ],
      className="pretty_container six columns"
    ),
  ],
    className="row"
  ),
  ###############################################################################
  # Third Row
  html.Div([
    html.Div([
      dcc.Graph(
        id='fig_2_1',
        figure=fig_2_1
      ),
    ],
      className="pretty_container twelve columns"
    ),
  ],
    className="row"
  ),
  ###############################################################################
  # Footer
  html.Div([
    # Left
    html.Div([
      datetime.date.today().year,
      "  ",
      html.Img(
        src="assets/copyright.svg",
        height="15px",
      ),
      "  by tschinz",
    ],
      className="five columns"
    ),
    # Middle
    html.Div([
      "Made with  ",
      html.Img(
        src="assets/love.svg",
        height="25px",
      ),
    ],
      className="four columns"
    ),
    # Right
    html.Div([
      "Icon made by ",
      html.A(flaticon_author[0], href=flaticon_author[1]),
      " from ",
      html.A(flaticon[0], href=flaticon[1]),
    ],
      className="three columns"
    )

  ])
])


###############################################################################
# App Callback
#
# Refresh Button
@app.callback(
  [Output('container-button-output', 'children'), ],
  [Input('btn-refresh-data', 'n_clicks')])
def refreshData(btn_refresh_data):
  global project_list_file
  global projectCol
  global ashCols
  global selector_project
  # read project list
  (projectDf, projectCol) = getProjectList(project_list_file, projectCol)

  # read project entries
  sageXDfs, projectConfs = getProjectEntries(inputDir)
  # Calc additional stuff
  sageXDfs, ashCols = calcAdditionalData(projectDf, sageXDfs, projectConfs, ashCols, projectCol, activityDf,
                                         activityCol)
  aggregated1Dfs, aggregated2Dfs, aggregated3Dfs = aggregateTime(sageXDfs, projectConfs, ashCols)

  # Select and filter data
  projectConf, selectedDf, aggregated1Df, aggregated2Df, aggregated3Df, ashCol = selectDf(projectConfs, sageXDfs,
                                                                                          aggregated1Dfs,
                                                                                          aggregated2Dfs,
                                                                                          aggregated3Dfs, ashCols,
                                                                                          selector_project)
  time_entries, start_date, end_date = filterData(selectedDf, duration_dropdown[selector_time_frame], ashCol["date"])

  date_exported = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["updated"]].iloc[0]

  return ["SageX data exported on the " + date_exported]


# Upload
def save_file(directory, name, content):
  """Decode and store a file uploaded with Plotly Dash."""
  files = listDir(directory)
  if name in files:
    os.remove(os.path.join(directory, name))
  data = content.encode("utf8").split(b";base64,")[1]#.encode()
  with open(os.path.join(directory, name), "wb") as fp:
    fp.write(base64.decodebytes(data))


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
  i = 0
  global data_inputDir
  if list_of_names is not None and list_of_contents is not None:
    for name, data in zip(list_of_names, list_of_contents):
      save_file(data_inputDir, name, data)
    i += 1

  return "{} files read and imported".format(i)


# Selector Buttons
@app.callback(
  [Output('kpi_title_0', 'children'),
   Output('kpi_text_0', 'children'),
   Output('kpi_title_1', 'children'),
   Output('kpi_text_1', 'children'),
   Output('kpi_text_1_1', 'children'),
   Output('kpi_title_2', 'children'),
   Output('kpi_text_2', 'children'),
   Output('kpi_text_2_2', 'children'),
   Output('kpi_title_3', 'children'),
   Output('kpi_text_3', 'children'),
   Output('kpi_text_3_3', 'children'),
   Output('kpi_title_4', 'children'),
   Output('kpi_text_4', 'children'),
   Output('kpi_text_4_4', 'children'),
   Output('table-data', 'data'),
   Output('fig_1_1', 'figure'),
   Output('fig_1_2', 'figure'),
   Output('fig_2_1', 'figure')],
  [Input('duration_selector', 'value'),
   Input('project_selector', 'value'),
   Input('date-picker-range', 'start_date'),
   Input('date-picker-range', 'end_date')])
def updateDiagrams(duration_selector, project_selector, start_date, end_date):
  global projectConfs
  global sageXDfs
  global aggregated1Dfs
  global aggregated2Dfs
  global aggregated3Dfs
  projectConf, selectedDf, aggregated1Df, aggregated2Df, aggregated3Df, ashCol = selectDf(projectConfs, sageXDfs,
                                                                                          aggregated1Dfs,
                                                                                          aggregated2Dfs,
                                                                                          aggregated3Dfs, ashCols,
                                                                                          int(project_selector))
  time_entries, start_date, end_date = filterData(selectedDf, duration_dropdown[duration_selector], ashCol["date"],
                                                  start_date, end_date)
  aggregated1Dfs, aggregated2Dfs, aggregated3Dfs = aggregateTime(sageXDfs, projectConfs, ashCols)

  # Basic stats
  date_exported = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["updated"]].iloc[0]
  project_begin = \
    filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["date_begin"]].iloc[0]
  project_end = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["date_end"]].iloc[
    0]
  project_budget = int(aggregated3Df[ashCol['total_budget']].iloc[0])
  project_monthly_budget = int(aggregated3Df[ashCol['monthly_budget']].iloc[0])
  project_budget_remaining = int(aggregated3Df[ashCol['remaining_budget']].iloc[-1])
  remaining_time = filterRows(projectDf, [projectCol["project_number"], [projectConf[0]]])[projectCol["date_end"]].iloc[
                     0] - getTodayDate()
  project_monthly_budget_remaining = int(aggregated3Df[ashCol['remaining_budget']].iloc[-1]) / (
      remaining_time.total_seconds() * second2month)

  # Figures
  fig_1_1 = projectPieBudgetActivity(aggregated1Df, aggregated3Df, ashCol, projectDf, projectCol, projectConf)
  fig_1_2 = projectPieCollaborators(aggregated2Df, ashCol, projectDf, projectCol, projectConf)
  fig_2_1 = projectPlotCombined(aggregated3Df, ashCol, projectDf, projectCol, projectConf)

  kpi_title_0 = "Project Number"
  kpi_text_0 = "SageX {}".format(projectConf[0])
  kpi_title_1 = "Time Frame"
  kpi_text_1 = project_begin.strftime('%d.%m.%Y')
  kpi_text_1_1 = project_end.strftime('%d.%m.%Y')
  kpi_title_2 = "Duration (Remaining)"
  kpi_text_2 = "{}".format(strfdelta(project_end - project_begin, '{W}w {D:80}d {H:02}h{M:02}m'))
  kpi_text_2_2 = "({})".format(strfdelta(remaining_time, '{W}w {D:80}d {H:02}h{M:02}m'))
  kpi_title_3 = "Budget (Remaining)"
  kpi_text_3 = "{} CHF".format(project_budget)
  kpi_text_3_3 = "({} CHF)".format(project_budget_remaining)
  kpi_title_4 = "Monthly Budget (Remaining)"
  kpi_text_4 = "{} CHF".format(project_monthly_budget)
  kpi_text_4_4 = "({} CHF)".format(math.floor(project_monthly_budget_remaining))

  return kpi_title_0, kpi_text_0, kpi_title_1, kpi_text_1, kpi_text_1_1, kpi_title_2, kpi_text_2, kpi_text_2_2, kpi_title_3, kpi_text_3, kpi_text_3_3, kpi_title_4, kpi_text_4, kpi_text_4_4, aggregated2Df.to_dict(
    'records'), fig_1_1, fig_1_2, fig_2_1


if __name__ == '__main__':
  app.run_server()
