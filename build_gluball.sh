cd '/Users/stephen/Development/Current/gluball/'
python setup.py py2app
rm -r gluball
mv dist gluball
echo "Copying files..."
cp -r dist_extra_files/* gluball
cd gluball
zip -r gluball.zip *