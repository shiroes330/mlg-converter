Param([string] $path, [bool] $skip)
if ($skip) {
    npx mlg-converter --format=csv $path
}
python preview_scatter_plot.py $path