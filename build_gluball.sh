cd '/Users/stephen/Development/Current/gluball/'
python setup.py py2app
mv dist gluball
echo "Copying files..."
cp -r dist_extra_files/* gluball

#zip -r Splatterboard.zip *