rm -Rf ./build
rm -Rf ./dist
rm ./*.c
mkdir ./dist
mkdir ./dist/images
mkdir ./dist/langs
mkdir ./dist/profiles

python3 setup.py build_ext --inplace
mv *.so ./dist

cp start.py ./dist
cp starter.py ./dist
cp autostart.py ./dist
cp readme ./dist

cp langs/* ./dist/langs
cp images/* ./dist/images
cp readme.txt ./dist/
cp requirements.txt ./dist/

cp config.json ./dist/
python3 img_hide.py

# cp -Rf profiles/ dist/