jupyverse --set frontend.collaborative=true --set kernels.require_yjs=true

rm log.txt; git checkout examples/switch.ipynb; hatch run dev:jpterm --server http://127.0.0.1:8000 --collaborative --experimental

fps_contents              0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/contents
fps_frontend              0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/frontend
fps_jupyterlab            0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/jupyterlab
fps_kernels               0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/kernels
fps_lab                   0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/lab
fps_noauth                0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/noauth
fps_terminals             0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/terminals
fps_yjs                   0.3.0        /home/david/github/davidbrochart/jupyverse/plugins/yjs
jpterm                    0.1.22       /home/david/github/davidbrochart/jpterm
jupyverse_api             0.3.0        /home/david/github/davidbrochart/jupyverse/jupyverse_api
txl                       0.1.22       /home/david/github/davidbrochart/jpterm/txl
txl_cell                  0.1.22       /home/david/github/davidbrochart/jpterm/plugins/cell
txl_console               0.1.22       /home/david/github/davidbrochart/jpterm/plugins/console
txl_editors               0.1.22       /home/david/github/davidbrochart/jpterm/plugins/editors
txl_file_browser          0.1.22       /home/david/github/davidbrochart/jpterm/plugins/file_browser
txl_image_viewer          0.1.22       /home/david/github/davidbrochart/jpterm/plugins/image_viewer
txl_jpterm                0.1.22       /home/david/github/davidbrochart/jpterm/plugins/jpterm
txl_kernel                0.1.22       /home/david/github/davidbrochart/jpterm/plugins/kernel
txl_launcher              0.1.22       /home/david/github/davidbrochart/jpterm/plugins/launcher
txl_local_contents        0.1.22       /home/david/github/davidbrochart/jpterm/plugins/local_contents
txl_local_kernels         0.1.22       /home/david/github/davidbrochart/jpterm/plugins/local_kernels
txl_local_terminals       0.1.22       /home/david/github/davidbrochart/jpterm/plugins/local_terminals
txl_markdown_viewer       0.1.22       /home/david/github/davidbrochart/jpterm/plugins/markdown_viewer
txl_notebook_editor       0.1.22       /home/david/github/davidbrochart/jpterm/plugins/notebook_editor
txl_remote_contents       0.1.22       /home/david/github/davidbrochart/jpterm/plugins/remote_contents
txl_remote_kernels        0.1.22       /home/david/github/davidbrochart/jpterm/plugins/remote_kernels
txl_remote_terminals      0.1.22       /home/david/github/davidbrochart/jpterm/plugins/remote_terminals
txl_terminal              0.1.22       /home/david/github/davidbrochart/jpterm/plugins/terminal
txl_text_editor           0.1.22       /home/david/github/davidbrochart/jpterm/plugins/text_editor
txl_widgets               0.1.22       /home/david/github/davidbrochart/jpterm/plugins/widgets
ypy-websocket             0.12.4       /home/david/github/davidbrochart/ypy-websocket
ypywidgets                0.5.0        /home/david/github/davidbrochart/ypywidgets
ypywidgets-textual        0.1.5        /home/david/github/davidbrochart/ypywidgets-textual
